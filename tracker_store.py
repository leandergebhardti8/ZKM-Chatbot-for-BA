import contextlib
import itertools
import json
import logging
import os
import pickle
from datetime import datetime, timezone
from rasa.core.tracker_store import TrackerStore
from time import sleep
from typing import (
    Callable,
    Dict,
    Iterable,
    Iterator,
    List,
    Optional,
    Text,
    Union,
    TYPE_CHECKING,
)

from boto3.dynamodb.conditions import Key
import rasa.core.utils as core_utils
from rasa.core.actions.action import ACTION_LISTEN_NAME
from rasa.core.brokers.broker import EventBroker
from rasa.core.constants import (
    POSTGRESQL_SCHEMA,
    POSTGRESQL_MAX_OVERFLOW,
    POSTGRESQL_POOL_SIZE,
)
from rasa.core.conversation import Dialogue
from rasa.core.domain import Domain
from rasa.core.events import SessionStarted
from rasa.core.trackers import ActionExecuted, DialogueStateTracker, EventVerbosity
import rasa.cli.utils as rasa_cli_utils
from rasa.utils.common import class_from_module_path, raise_warning, arguments_of
from rasa.utils.endpoints import EndpointConfig
import sqlalchemy as sa

if TYPE_CHECKING:
    import boto3.resources.factory.dynamodb.Table
    from sqlalchemy.engine.url import URL
    from sqlalchemy.engine.base import Engine
    from sqlalchemy.orm.session import Session
    from sqlalchemy import Sequence
    from sqlalchemy.orm.query import Query

logger = logging.getLogger(__name__)

# default values of PostgreSQL pool size and max overflow
POSTGRESQL_DEFAULT_MAX_OVERFLOW = 100
POSTGRESQL_DEFAULT_POOL_SIZE = 5

def _create_sequence(table_name: Text) -> "Sequence":
    """Creates a sequence object for a specific table name.

    If using Oracle you will need to create a sequence in your database,
    as described here: https://rasa.com/docs/rasa/api/tracker-stores/#sqltrackerstore
    Args:
        table_name: The name of the table, which gets a Sequence assigned

    Returns: A `Sequence` object
    """

    from sqlalchemy.ext.declarative import declarative_base

    sequence_name = f"{table_name}_seq"
    Base = declarative_base()
    return sa.Sequence(sequence_name, metadata=Base.metadata, optional=True)


def is_postgresql_url(url: Union[Text, "URL"]) -> bool:
    """Determine whether `url` configures a PostgreSQL connection.

    Args:
        url: SQL connection URL.

    Returns:
        `True` if `url` is a PostgreSQL connection URL.
    """
    if isinstance(url, str):
        return "postgresql" in url

    return url.drivername == "postgresql"


def create_engine_kwargs(url: Union[Text, "URL"]) -> Dict[Text, Union[Text, int]]:
    """Get `sqlalchemy.create_engine()` kwargs.

    Args:
        url: SQL connection URL.

    Returns:
        kwargs to be passed into `sqlalchemy.create_engine()`.
    """
    if not is_postgresql_url(url):
        return {}

    kwargs = {}

    schema_name = os.environ.get(POSTGRESQL_SCHEMA)

    if schema_name:
        logger.debug(f"Using PostgreSQL schema '{schema_name}'.")
        kwargs["connect_args"] = {"options": f"-csearch_path={schema_name}"}

    # pool_size and max_overflow can be set to control the number of
    # connections that are kept in the connection pool. Not available
    # for SQLite, and only  tested for PostgreSQL. See
    # https://docs.sqlalchemy.org/en/13/core/pooling.html#sqlalchemy.pool.QueuePool
    kwargs["pool_size"] = int(
        os.environ.get(POSTGRESQL_POOL_SIZE, POSTGRESQL_DEFAULT_POOL_SIZE)
    )
    kwargs["max_overflow"] = int(
        os.environ.get(POSTGRESQL_MAX_OVERFLOW, POSTGRESQL_DEFAULT_MAX_OVERFLOW)
    )

    return kwargs


def ensure_schema_exists(session: "Session") -> None:
    """Ensure that the requested PostgreSQL schema exists in the database.

    Args:
        session: Session used to inspect the database.

    Raises:
        `ValueError` if the requested schema does not exist.
    """
    schema_name = os.environ.get(POSTGRESQL_SCHEMA)

    if not schema_name:
        return

    engine = session.get_bind()

    if is_postgresql_url(engine.url):
        query = sa.exists(
            sa.select([(sa.text("schema_name"))])
            .select_from(sa.text("information_schema.schemata"))
            .where(sa.text(f"schema_name = '{schema_name}'"))
        )
        if not session.query(query).scalar():
            raise ValueError(schema_name)

class CustomSQLTrackerStore(TrackerStore):
    """Store which can save and retrieve trackers from an SQL database."""

    from sqlalchemy.ext.declarative import declarative_base

    Base = declarative_base()

    class SQLEvent(Base):
        """Represents an event in the SQL Tracker Store"""

        __tablename__ = "events"

        # `create_sequence` is needed to create a sequence for databases that
        # don't autoincrement Integer primary keys (e.g. Oracle)
        id = sa.Column(sa.Integer, _create_sequence(__tablename__), primary_key=True)
        sender_id = sa.Column(sa.String(255), nullable=False, index=True)
        type_name = sa.Column(sa.String(255), nullable=False)
        timestamp = sa.Column(sa.Float)
        intent_name = sa.Column(sa.String(255))
        action_name = sa.Column(sa.String(255))
        data = sa.Column(sa.Text)

    def __init__(
        self,
        domain: Optional[Domain] = None,
        dialect: Text = "sqlite",
        host: Optional[Text] = None,
        port: Optional[int] = None,
        db: Text = "rasa.db",
        username: Text = None,
        password: Text = None,
        event_broker: Optional[EventBroker] = None,
        login_db: Optional[Text] = None,
        query: Optional[Dict] = None,
    ) -> None:
        import sqlalchemy.exc

        engine_url = self.get_db_url(
            dialect, host, port, db, username, password, login_db, query
        )
        logger.debug(f"Attempting to connect to database via '{engine_url}'.")

        # Database might take a while to come up
        while True:
            try:
                self.engine = sa.engine.create_engine(
                    engine_url, **create_engine_kwargs(engine_url)
                )
                # if `login_db` has been provided, use current channel with
                # that database to create working database `db`
                if login_db:
                    self._create_database_and_update_engine(db, engine_url)

                try:
                    self.Base.metadata.create_all(self.engine)
                except (
                    sqlalchemy.exc.OperationalError,
                    sqlalchemy.exc.ProgrammingError,
                ) as e:
                    # Several Rasa services started in parallel may attempt to
                    # create tables at the same time. That is okay so long as
                    # the first services finishes the table creation.
                    logger.error(f"Could not create tables: {e}")

                self.sessionmaker = sa.orm.session.sessionmaker(bind=self.engine)
                break
            except (
                sqlalchemy.exc.OperationalError,
                sqlalchemy.exc.IntegrityError,
            ) as error:

                logger.warning(error)
                sleep(5)

        logger.debug(f"Connection to SQL database '{db}' successful.")

        super().__init__(domain, event_broker)

    @staticmethod
    def get_db_url(
        dialect: Text = "sqlite",
        host: Optional[Text] = None,
        port: Optional[int] = None,
        db: Text = "rasa.db",
        username: Text = None,
        password: Text = None,
        login_db: Optional[Text] = None,
        query: Optional[Dict] = None,
    ) -> Union[Text, "URL"]:
        """Build an SQLAlchemy `URL` object representing the parameters needed
        to connect to an SQL database.

        Args:
            dialect: SQL database type.
            host: Database network host.
            port: Database network port.
            db: Database name.
            username: User name to use when connecting to the database.
            password: Password for database user.
            login_db: Alternative database name to which initially connect, and create
                the database specified by `db` (PostgreSQL only).
            query: Dictionary of options to be passed to the dialect and/or the
                DBAPI upon connect.

        Returns:
            URL ready to be used with an SQLAlchemy `Engine` object.
        """
        from urllib import parse

        # Users might specify a url in the host
        if host and "://" in host:
            # assumes this is a complete database host name including
            # e.g. `postgres://...`
            return host
        elif host:
            # add fake scheme to properly parse components
            parsed = parse.urlsplit(f"scheme://{host}")

            # users might include the port in the url
            port = parsed.port or port
            host = parsed.hostname or host

        return sa.engine.url.URL(
            dialect,
            username,
            password,
            host,
            port,
            database=login_db if login_db else db,
            query=query,
        )

    def _create_database_and_update_engine(self, db: Text, engine_url: "URL"):
        """Create databse `db` and update engine to reflect the updated `engine_url`."""

        from sqlalchemy import create_engine

        self._create_database(self.engine, db)
        engine_url.database = db
        self.engine = create_engine(engine_url)

    @staticmethod
    def _create_database(engine: "Engine", db: Text):
        """Create database `db` on `engine` if it does not exist."""

        import psycopg2

        conn = engine.connect()

        cursor = conn.connection.cursor()
        cursor.execute("COMMIT")
        cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{db}'")
        exists = cursor.fetchone()
        if not exists:
            try:
                cursor.execute(f"CREATE DATABASE {db}")
            except psycopg2.IntegrityError as e:
                logger.error(f"Could not create database '{db}': {e}")

        cursor.close()
        conn.close()

    @contextlib.contextmanager
    def session_scope(self):
        """Provide a transactional scope around a series of operations."""
        session = self.sessionmaker()
        try:
            ensure_schema_exists(session)
            yield session
        except ValueError as e:
            rasa_cli_utils.print_error_and_exit(
                f"Requested PostgreSQL schema '{e}' was not found in the database. To "
                f"continue, please create the schema by running 'CREATE DATABASE {e};' "
                f"or unset the '{POSTGRESQL_SCHEMA}' environment variable in order to "
                f"use the default schema. Exiting application."
            )
        finally:
            session.close()

    def keys(self) -> Iterable[Text]:
        """Returns sender_ids of the SQLTrackerStore"""
        with self.session_scope() as session:
            sender_ids = session.query(self.SQLEvent.sender_id).distinct().all()
            return [sender_id for (sender_id,) in sender_ids]

    def retrieve(self, sender_id: Text) -> Optional[DialogueStateTracker]:
        """Create a tracker from all previously stored events."""

        with self.session_scope() as session:

            serialised_events = self._event_query(session, sender_id).all()
            events = [json.loads(event.data) for event in serialised_events]
            logger.debug(
                    f"Retrived events from tracker {events}"
                    )

            if self.domain and len(events) > 0:
                logger.debug(f"Recreating tracker from sender id '{sender_id}'")
                return DialogueStateTracker.from_dict(
                    sender_id, events, self.domain.slots
                )
            else:
                logger.debug(
                    f"Can't retrieve tracker matching "
                    f"sender id '{sender_id}' from SQL storage. "
                    f"Returning `None` instead."
                )
                return None

    def _event_query(self, session: "Session", sender_id: Text) -> "Query":
        """Provide the query to retrieve the conversation events for a specific sender.

        Args:
            session: Current database session.
            sender_id: Sender id whose conversation events should be retrieved.

        Returns:
            Query to get the conversation events.
        """
        # Subquery to find the timestamp of the latest `SessionStarted` event
        session_start_sub_query = (
            session.query(sa.func.max(self.SQLEvent.timestamp).label("session_start"))
            .filter(
                self.SQLEvent.sender_id == sender_id,
                self.SQLEvent.type_name == SessionStarted.type_name,
            )
            .subquery()
        )

        event_query = session.query(self.SQLEvent).filter(
            self.SQLEvent.sender_id == sender_id
        )
        if not self.load_events_from_previous_conversation_sessions:
            event_query = event_query.filter(
                # Find events after the latest `SessionStarted` event or return all
                # events
                sa.or_(
                    self.SQLEvent.timestamp >= session_start_sub_query.c.session_start,
                    session_start_sub_query.c.session_start.is_(None),
                )
            )

        return event_query.order_by(self.SQLEvent.timestamp)

    def save(self, tracker: DialogueStateTracker) -> None:
        """Update database with events from the current conversation."""

        if self.event_broker:
            self.stream_events(tracker)

        with self.session_scope() as session:
            # only store recent events
            events = self._additional_events(session, tracker)

            for event in events:
                data = event.as_dict()
                intent = data.get("parse_data", {}).get("intent", {}).get("name")
                action = data.get("name")
                timestamp = data.get("timestamp")

                # noinspection PyArgumentList
                session.add(
                    self.SQLEvent(
                        sender_id=tracker.sender_id,
                        type_name=event.type_name,
                        timestamp=timestamp,
                        intent_name=intent,
                        action_name=action,
                        data=json.dumps(data),
                    )
                )
            session.commit()

        logger.debug(f"Tracker with sender_id '{tracker.sender_id}' stored to database")

    def _additional_events(
        self, session: "Session", tracker: DialogueStateTracker
    ) -> Iterator:
        """Return events from the tracker which aren't currently stored."""

        number_of_events_since_last_session = self._event_query(
            session, tracker.sender_id
        ).count()
        return itertools.islice(
            tracker.events, number_of_events_since_last_session, len(tracker.events)
        )
