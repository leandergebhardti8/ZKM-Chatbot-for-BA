from typing import Text, Dict, Any, List, Union
import logging
from datetime import datetime 
from datetime import timedelta
import requests
from rasa_sdk.events import SlotSet, BotUttered
from rasa_sdk import Action, Tracker
from graph_db import InMemoryGraph as db, ATTR_MAP, ENT_MAP, ATTR_KEY_MAP, MEN_MAP, equalComp, compareDates, containsComp
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from datetime import date
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import html
import time
import io
import base64
# import locale
from fuzzywuzzy import fuzz
# import cProfile
# import pstats
# from pstats import SortKey

rasa_env = os.environ.get("rasa_env", None) 
# if (rasa_env!= None): 
#     locale.setlocale(locale.LC_ALL, 'de_DE.utf-8') 
# else:
#     locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')

mailserver_user = os.environ.get("email_user", "data")
mailserver_password = os.environ.get("email_password", "bl341xbAUxLvq+")

fuehrung_email = os.environ.get("FUEHRUNG_EMAIL", "e.ersada@integr8.com")
werk_fragen_email = os.environ.get("WERK_FRAGEN_EMAIL", "e.ersada@integr8.com")
publikation_bestellen_email = os.environ.get("PUBLIKATION_BESTELLEN_EMAIL", "e.ersada@integr8.com")
publikation_fragen_email = os.environ.get("PUBLIKATION_FRAGEN_EMAIL", "e.ersada@integr8.com")
allgemeine_fragen_email = os.environ.get("ALLGEMEINE_FRAGEN_EMAIL", "e.ersada@integr8.com")
fotografie_genehmigung_email = os.environ.get("FOTOGRAFIE_GENEHMIGUNG_EMAIL", "e.ersada@integr8.com")
# fuehrung_email = os.environ.get("FUEHRUNG_EMAIL", "chatbot_intern@zkm.de")
# werk_fragen_email = os.environ.get("WERK_FRAGEN_EMAIL", "chatbot_intern@zkm.de")
# publikation_bestellen_email = os.environ.get("PUBLIKATION_BESTELLEN_EMAIL", "chatbot_intern@zkm.de")
# publikation_fragen_email = os.environ.get("PUBLIKATION_FRAGEN_EMAIL", "chatbot_intern@zkm.de")
# allgemeine_fragen_email = os.environ.get("ALLGEMEINE_FRAGEN_EMAIL", "chatbot_intern@zkm.de")
# fotografie_genehmigung_email = os.environ.get("FOTOGRAFIE_GENEHMIGUNG_EMAIL", "chatbot_intern@zkm.de")
# fotografie_genehmigung_email = os.environ.get("FOTOGRAFIE_GENEHMIGUNG_EMAIL", "chatbot_intern@zkm.de")
##########################
#    Constants Section
##########################

logger = logging.getLogger(__name__)
logger.debug("fuehrung email = {}".format(fuehrung_email))
logger.debug("werk fragen = {}".format(werk_fragen_email))
logger.debug("publ best= {}".format(publikation_bestellen_email))
logger.debug("publ frag = {}".format(publikation_fragen_email))
logger.debug("allgemeine_fragen_email {}".format(allgemeine_fragen_email))
logger.debug("fotografie_genehmigung {}".format(fotografie_genehmigung_email))
schema = {
    "person": {
        "attributes": ["nationality", "name", "nid"],
        "representation": ["name", "nid"],
        "key": "name"
    },
    "event": {
        "attributes": ["title", "location_name", "date", "time","corr_person", "nid", "subcategory", "link", "targetgroup"],
        "representation": ["title", "date", "subtitle", "image_url", "corr_person", "nid", "link"],
        "key": "title"
    },
    "creation": {
        "attributes": ["creator_id", "corr_event", "creation_date", "title", "creator_name", "creator", "image_url", "link"],
        "representation": ["creator_id", "corr_event","creation_date", "image_url",  "title", "creator_name", "link"],
        "key": "title"
    },
    "publication": {
        "attributes": ["title", "date" ],
        "representation": ["title", "date", "shop_link", "cover_image_url"],
        "key": "title"
    }
}
calender = {
    0: "Montag",
    1: "Dienstag",
    2: "Mittwoch",
    3: "Donnerstag",
    4: "Freitag",
    5: "Samstag",
    6: "Sonntag",
}

#######################
#    Interfaces
#######################

class Zdate():
    value: date

    def __init__(self, value):
        if (value == None):
            raise ValueError
        self.value = value
    
    def toGermanDate(self) -> Text:
        return datetime.strftime(self.value, '%d.%m.%Y')
    def toEnglishDate(self) -> Text:
        return datetime.strftime(self.value, '%Y-%m-%d')
    def getWeekDay(self) -> Text:
        return calender[self.value.weekday()]

class DbQueryResult():
    """
    Result object of querying the knowledge database
    fields error and result are required,
    other fields are: entity type, slots
    """
    error: str
    result: Any
    entity_type: str
    attribute: str
    entity_name: str
    slots: List

    def __init__(self, error, result, slots=[], entity_type="", entity_name="", attribute=""):
        self.error = error
        self.result = result
        self.slots = slots
        self.entity_type = entity_type
        self.entity_name = entity_name
        self.attribute = attribute

class EmailInfo():
    message_text: str
    message_html: str
    subject: str
    email_receiver: str

    def __init__(self, message_text, message_html, subject, email_receiver):
        self.message_text = message_text
        self.message_html = message_html
        self.subject = subject
        self.email_receiver = email_receiver


##########################
#    Utility functions
##########################

def get_attributes_of_entity(dbInstance, entity_type, tracker) -> List[Dict[any, any]]:
    attributes = []

    if entity_type in schema:
        for attr in schema[entity_type]["attributes"]:

            value = str(tracker.get_slot(attr))
            value = value if attr == "time" and value != 'None' else dbInstance.map(
                ATTR_MAP, value.lower(), attr)
            attr = "date" if attr == "time" else attr
            compareFunction = get_compare_function_of_attribute(attr)

            if value != None:
                attributes.append(
                    {'key': attr, 'value': value, 'comp': compareFunction})
    return attributes


def get_compare_function_of_attribute(attr):
    if (attr == "date"):
        return compareDates
    return equalComp


def get_attribute(dbInstance, tracker):
    attr = str(tracker.get_slot('attribute'))
    attribute = dbInstance.map(ATTR_KEY_MAP, attr.lower())
    return attribute


def get_entity_name(tracker, entity_type):
    name = tracker.get_slot(entity_type)
    if name != None:
        return name
    name = resolve_mention(tracker)
    if name != None:
        return name
    return None


def get_entity_key(dbInstance, tracker):
    for entity in schema:
        value = tracker.get_slot(entity)
        if value is None:
            continue
        return entity

    entityKey = tracker.get_slot('entity_type')
    if entityKey != None:
        value = dbInstance.map(ENT_MAP, entityKey)
        if value != None:
            return value

    return None


def reset_attribute_slots(slots, entity_type, tracker):
    """
    Reset all slots corresponding to the attributes of a given entity as per the schema.
    parameters:
    slots = slots that you want to keep
    entity_type
    tracker
    """
    slots.append(SlotSet("time", None))
    if entity_type in schema:
        for attr in schema[entity_type]["attributes"]:
            attr_val = tracker.get_slot(attr)
            if attr_val is not None:
                slots.append(SlotSet(attr, None))
    return slots


def resolve_mention(tracker: Tracker) -> Text:
    """
    Resolves a mention of an entity, such as first, to the actual entity.
    If multiple entities are listed during the conversation, the entities
    are stored in the slot 'listed_items' as a list. We resolve the mention,
    such as first, to the list index and retrieve the actual entity.
    :param tracker: tracker
    :return: name of the actually entity
    """
    graph_database = db()

    mention = tracker.get_slot("mention")
    listed_items = tracker.get_slot("listed_items")

    if mention is not None and listed_items is not None:
        idx = int(graph_database.map(MEN_MAP, mention))

        if type(idx) is int and idx < len(listed_items):
            return listed_items[idx]


def to_str(entity: Dict[Text, Any], entity_keys: Union[Text, List[Text]]) -> Text:
    """
    Converts an entity to a string by concatenating the values of the provided
    entity keys.
    :param entity: the entity with all its attributes
    :param entity_keys: the name of the representation attributes
    :return: a string that represents the entity
    """
    if isinstance(entity_keys, str):
        entity_keys = [entity_keys]

    result_list = ['{} : {}'.format(attr, entity[attr])
                   for attr in entity_keys]
    return ", ".join(result_list)

def string_to_german_date(date_value) -> Text:
    """
    Converts an date (String) into german date (String).
    :param date_value: date as a string
    :return: a string that represents a german date
    """
    obj = datetime.strptime(date_value,'%Y-%m-%d %H:%M:%S') #2014-01-06 10:00:00
    date = datetime.strftime(obj, '%d.%m.%Y')
    return date

def to_dict(entity: Dict[Text, Any], entity_keys: Union[Text, List[Text]]) -> Dict:
    """
    Converts an entity to a dic by concatenating the values of the provided
    entity keys.
    :param entity: the entity with all its attributes
    :param entity_keys: the name of the representation attributes
    :return: a dic that represents the entity
    """
    if isinstance(entity_keys, str):
        entity_keys = [entity_keys]
    result_dic = {}
    for attr in entity_keys:
        result_dic[attr] = entity[attr]
    return result_dic

def get_entity_type(tracker) -> Text:
    entity = tracker.get_slot("entity_type")
    if entity is None:
        entity = "person" if tracker.get_slot("PER") is not None else None
    return entity
        
def get_date(tracker) -> Zdate:
    """
    get_date Looks for the date object in the slots time (filled by duckling)
    or Date (filled by our own entities)
    return a Zdate object, or None.
    """
    dates = tracker.get_slot("time") or tracker.get_slot("date")
    if (dates == None or dates=='heute'):
        return Zdate(value=date.today())
    try:
        if(rasa_env == 'production'):
            dateObject = datetime.strptime(dates[:10], '%Y-%m-%d').date()
        else:
            dateObject = datetime.strptime(dates[:10], '%d.%m.%Y').date()
        return Zdate(value=dateObject) 
    except ValueError:
        return None
        # dateObject = datetime.strptime(dates[:10], '%Y-%m-%d').date()
        # return Zdate(value=dateObject)

def query_attribute(tracker, attr: Text = "", entity: Text = None) -> DbQueryResult:
    graph_database = db()

    attribute = attr
    entity_type = entity or get_entity_key(graph_database, tracker)

    if entity_type is None:
        return DbQueryResult(error="Entity type nicht gefunden", result=None)

    name = get_entity_name(tracker, entity_type)

    if (len(attribute) <= 0):
        attribute = get_attribute(graph_database, tracker)

    logger.debug(
        "name of entity {}, attribute requested {}".format(name, attribute))

    if name is None or attribute is None:
        return DbQueryResult(error="Slot entity type was None", result=None)

    key_attribute = schema[entity_type]["key"]
    value = graph_database.get_attribute_of(
        entity_type, key_attribute, name, attribute
    )

    slots = [SlotSet("mention", None), SlotSet(entity_type, name)]
    slots = reset_attribute_slots(slots, entity_type, tracker)
    return DbQueryResult(error=None, result=value,
                         slots=slots, entity_type=entity_type,
                         attribute=attribute, entity_name=name
                         )


def query_entities(tracker, attr: List[Dict[any, any]] = [], entity_type_param: Text = None, limit= int, useIndex=False) -> DbQueryResult:
    """
    query_entities will search for every entity of a determine entity type(event, person, etc)
    and given attributes
    :Param tracker: required, attr: attributes with wich the entities will be filtered, if not 
    given any, it will search on the attribute slot.
    :Returns a DbQueryResult wich is an object with (error, result, entity_type, slots) fields
    """

    graph_database = db()
    attributes = attr 
    entity_type = entity_type_param if entity_type_param != None else get_entity_type(tracker=tracker)
    # if (entity_type == 'Workshops'):
    #         entity_type = 'workshop'
    if entity_type is None:
        entity_type='event'
    logger.debug(entity_type)
    logger.debug("query_entities")
    if entity_type is None:
        return DbQueryResult(error="Entity type nicht gefunden", result=None)

    if (len(attributes) <= 0):
        attributes = get_attributes_of_entity(
            graph_database, entity_type, tracker)

    if useIndex:
        entities = graph_database.get_entities_op(entity_type, attributes)
    else:
        entities = graph_database.get_entities(entity_type, attributes)

    if not entities:
        return DbQueryResult(error=None, result=[])

    entity_representation: List[str] = schema[entity_type]["representation"]

    sorted_entities = [to_dict(e, entity_representation) for e in entities]

    entity_key = schema[entity_type]["key"]

    slots = [
        SlotSet("entity_type", entity_type),
        SlotSet("listed_items", list(
                map(lambda entity: str(entity[entity_key]), entities))),
    ]

    return DbQueryResult(
        error=None, result=sorted_entities,
        slots=slots, entity_type=entity_type
    )

def prepareEmailInfo(tracker)-> EmailInfo:

    email_type = tracker.get_slot("email_type") or "book_guide"
    if email_type == "book_guide":

        subject = "Führung buchen"
        name = tracker.get_slot('name')
        email = tracker.get_slot('email')
        num_people = tracker.get_slot('num_people')
        phone_number = ""
        visit_date = tracker.get_slot('date')
        visit_time = tracker.get_slot('visit_time')
        guide_event = tracker.get_slot('guide_event')
        kind_of_event = tracker.get_slot('kind_of_event')

        message_html = """
        <html>
            <body>
                <h3>{}</h3>
                <p>
                Email von: {}
                </p>
                <p>Nachricht lautet: </p>
                <p>-----------------------</p>
                <p> {}
                    {}
                    {}
                    {} 
                    {}
                    {}
                    {}
                </p>
                <p>-----------------------</p>
            </body>
        </html>
            """.format(subject, email, name, phone_number, guide_event, kind_of_event, num_people, visit_date, visit_time)

        message_text = """
        Telefonnummer: {}
        Bitte gib eine gültige Telefonnummer für Rückfragen an

        Betreff: Anfrage {}

        {} möchte gerne eine Führung buchen für {} Personen.

        Am {} {}.

        Durch die Ausstellung {}.
        
        Die Art der Führung soll eine {} sein.
        
        ---
        Vom ZKM Bot gesendet
        """.format(phone_number, subject, name, num_people, visit_date, visit_time, guide_event, kind_of_event )
        # .format(subject, name, phone_number, guide_event, kind_of_event, num_people, visit_date, visit_time)

        return EmailInfo(message_text=message_text, message_html= message_html, subject=subject, email_receiver=fuehrung_email)

    if email_type == "question_creation":

        creation = tracker.get_slot('creation')
        name = tracker.get_slot('name')
        email = tracker.get_slot('email')
        subject = "Anfrage zu Werk {}".format(creation)

        message_html = """
        <html>
            <body>
                <h3>{}</h3>
                <p>
                Email von: {}
                </p>
                <p>Nachricht lautet: </p>
                <p>-----------------------</p>
                <p> 
                    Liebes ZKM,
                    ich würde gerne mehr über Werk {} wissen. Euer Chatbot meinte, ich sollte Euch fragen.
                    Herzliche Grüße, {}
                </p>
                <p>-----------------------</p>
            </body>
        </html>
            """.format(subject, email, creation, name)

        message_text = """
        Liebes ZKM,
        ich würde gerne mehr über Werk {} wissen. Euer Chatbot meinte, ich sollte Euch fragen.
        Herzliche Grüße, {}
        """.format(creation, name)

        return EmailInfo(message_text=message_text, message_html=message_html,
         subject=subject, email_receiver=werk_fragen_email)

    if email_type == "buy_publication":

        publication = tracker.get_slot('publication')
        name = tracker.get_slot('name')
        email = tracker.get_slot('email')
        subject = publication

        message_html = """
        <html>
            <body>
                <h3>{}</h3>
                <p>
                Email von: {}
                </p>
                <p>Nachricht lautet: </p>
                <p>-----------------------</p>
                <p> 
                    Sehr geehrte Damen und Herren, ich würde gerne Publikation {} bestellen.
                    Bitten teilen Sie mir doch mit, ob die Publikation verfügbar ist und zu welchen Konditionen sie verschickt werden kann.
                    Mit freundlichen Grüßen, {}
                </p>
                <p>-----------------------</p>
            </body>
        </html>
            """.format(subject, email, publication, name)

        message_text = """
Liebes ZKM-Team, 
ich würde gerne die Publikation {} bestellen.
Bitten teilen Sie mir doch mit, ob die Publikation verfügbar ist und zu welchen Konditionen sie verschickt werden kann.
Mit freundlichen Grüßen, {}
        """.format(publication, name)

        return EmailInfo(message_text=message_text, message_html=message_html,
         subject=subject, email_receiver=publikation_bestellen_email)

    if email_type == "ask_for_publication":

        publication = tracker.get_slot('publication') or "{*}"
        name = tracker.get_slot('name')
        email = tracker.get_slot('email')
        subject = publication

        message_html = """
        <html>
            <body>
                <h3>{}</h3>
                <p>
                Email von: {}
                </p>
                <p>Nachricht lautet: </p>
                <p>-----------------------</p>
                <p> 
                    Liebes ZKM, ich interessiere mich für den Katalog zu  {}.
                    Ist diese Publikation eventuell noch in Arbeit?
                    Mit besten Grüßen, {}
                </p>
                <p>-----------------------</p>
            </body>
        </html>
            """.format(subject, email, publication, name)

        message_text = """
        Liebes ZKM, ich interessiere mich für den Katalog zu {}. 
        Ist diese Publikation eventuell noch in Arbeit? 
        Mit besten Grüßen, {}
        """.format(publication, name)

        return EmailInfo(message_text=message_text, message_html=message_html,
         subject=subject, email_receiver=publikation_fragen_email)

    if email_type == "custom_message":

        message = ""
        name = tracker.get_slot('name')
        email = tracker.get_slot('email')
        subject = "Frage"
        context = tracker.get_slot('current_context')

        message_html = """
        <html>
            <body>
                <h3>{}</h3>
                <p>
                Email von: {}
                </p>
                <p>{}</p>
                <p>Nachricht lautet: </p>
                <p>-----------------------</p>
                <p> 
                    {},
                    Mit besten Grüßen, {}
                </p>
                <p>-----------------------</p>
            </body>
        </html>
            """.format(subject, email, context, message, name)

        message_text = """
    {}
    Mit besten Grüßen, {}
        """.format(message, name)

        logger.debug("message_html")
        logger.debug(message_html)
        return EmailInfo(message_text=message_text, message_html=message_html,
         subject=subject, email_receiver=allgemeine_fragen_email)

    if email_type == "approval":

        message = ""
        name = tracker.get_slot('name')
        email = tracker.get_slot('email')
        subject = "Fotografie - Genehmigung"

        message_html = """
        <html>
            <body>
                <h3>{}</h3>
                <p>
                Email von: {}
                </p>
                <p>Nachricht lautet: </p>
                <p>-----------------------</p>
                <p> 
                    {},
                    Mit besten Grüßen,{}
                </p>
                <p>-----------------------</p>
            </body>
        </html>
            """.format(subject, email, message, name)

        message_text = """
        {}
    Mit besten Grüßen, {}
        """.format(message, name)

        return EmailInfo(message_text=message_text, message_html=message_html,
         subject=subject, email_receiver=fotografie_genehmigung_email)

def build_html_message(subject: Text, email: Text, message: Text, context: Text):

    if not context:
        message_html = """
            <html>
                <body>
                    <h3>{}</h3>
                    <p>
                    Email von: {}
                    </p>
                    <p>Nachricht lautet: </p>
                    <p>-----------------------</p>
                    <p> {}
                    </p>
                    <p>-----------------------</p>
                </body>
            </html>
                """.format(subject, email, message)
    else:
        message_html = """
            <html>
                <body>
                    <h3>{}</h3>
                    <p>
                    Email von: {}
                    </p>
                    <p>{}</p>
                    <p>Nachricht lautet: </p>
                    <p>-----------------------</p>
                    <p> {}
                    </p>
                    <p>-----------------------</p>
                </body>
            </html>
                """.format(subject, email, context, message)
    return message_html
    # return html.escape(message_html)

#######################
#    Profile
#######################

#cProfile.runctx("""query_entities(tracker=None, entity_type_param="event",attr=[{'key': "title", 'value': "Wittgenstein in Coen Country", 'comp': equalComp}], useIndex=True)""", filename="profile", globals=globals(), locals=locals())
# cProfile.runctx("""query_entities(tracker=None, entity_type_param="event",attr=[{'key': "title", 'value': "mihara", 'comp': equalComp}], useIndex=True)""", filename="profile", globals=globals(), locals=locals())
# with io.open("profile_result", mode="w") as file:
#     p = pstats.Stats("profile", stream=file)
#     p.sort_stats(SortKey.CUMULATIVE).print_stats()

#######################
#    Rasa Actions
#######################
    
class ExhibitionFromArtist(Action):
    """Action for listing entities.
    The entities might be filtered by specific attributes."""

    def name(self):
        return "action_query_exhibition_artist"
    
    def run(self, dispatcher, tracker, domain):
        artist_name = tracker.get_slot("PER")
        event_name = tracker.get_slot("event")

        query_person = query_entities(tracker=tracker, entity_type_param="person",
        attr=[{'key': "name", 'value': artist_name, 'comp': equalComp}])

        if query_person.error is not None or len(query_person.result) <= 0:
            dispatcher.utter_message("Das habe ich nicht verstanden")
            return []

        person_nid = query_person.result[0]["nid"]

        query_event = query_entities(tracker=tracker, entity_type_param="event",
        attr=[{'key': "title", 'value': event_name, 'comp': equalComp}], useIndex=True)
       
        if query_event.error is not None and len(query_event.result) <= 0:
            dispatcher.utter_message("Das habe ich nicht verstanden")
            return []

        event_nid = query_event.result[0]["nid"]
        event_corr_person = query_event.result[0]["corr_person"]

        if "Writing the History of the Future" in event_name and person_nid in event_corr_person:

            query_creation = query_entities(tracker=tracker, entity_type_param="creation", 
            attr=[{'key': "creator_id", 'value': person_nid, 'comp': containsComp},
            {'key': "corr_event", 'value': event_nid, 'comp': containsComp}])

            dispatcher.utter_message(
                f"In Writing the History of the Future zeigen wir folgende Arbeiten von {artist_name}"
                )
            creations = query_creation.result

            message_to_send = {
                "type": query_creation.entity_type,
                "items": creations
            }

            dispatcher.utter_message(
                json_message=message_to_send
            )
            return []

        if not person_nid in event_corr_person:
            dispatcher.utter_message(
                "Leider nein. Künstler {} ist nicht Teil der Ausstellung {}".format(artist_name, event_name)
            )
            return []
        
        dispatcher.utter_message(
                "Ja, wir zeigen {} ist nicht Teil der Ausstellung {}".format(artist_name, event_name)
            )
        return []

class ActionChildrenRecommendation(Action):
    def name(self):
        return "action_beliebt_bei_kindern"

    def run(self, dispatcher, tracker, domain):
        date_object = get_date(tracker)
        if (date_object is None):
            dispatcher.utter_message("Bitte geben Sie das Datum im folgenden Format an tt.mm.jjjj")
            return []
        date_value = date_object.value
        format_date = date_object.toGermanDate()

        message_text = "Hier das Programm für {}, den {}.".format(date_object.getWeekDay(), format_date)
        attr = []
        attr.append({"key": "targetgroup", "value": "children", "comp": containsComp})

        event_type = tracker.get_slot("entity_type") or None
        if event_type == 'Veranstaltungen':
            event_type = 'event'
        if event_type is None:
            event_type = 'event'

        if (fuzz.ratio(event_type, "Workshop") >80 or fuzz.ratio(event_type, "Workshops") >80):
            attr.append({"key": "subcategory", "value": "workshop", "comp": equalComp})
            message_text = "Am {}, den {} finden folgende Workshops für Kinder statt".format(date_object.getWeekDay(), format_date)
        
        query_result = query_entities(tracker=tracker, entity_type_param=event_type, attr=attr)

        end_date = date_value + timedelta(days=7)
        entities = query_result.result
        filtered_entites = []
        for entity in entities:
            if (datetime.strptime(entity["date"]["end"][:10], '%Y-%m-%d').date() >= date_value and
                datetime.strptime(entity["date"]["start"][:10], '%Y-%m-%d').date() <= end_date):
                filtered_entites.append(entity)
        logger.debug(filtered_entites)

        if query_result.error is not None:
            dispatcher.utter_message("Das habe ich nicht verstanden")
            return []

        elif not query_result.result or len(query_result.result) <= 0:
            dispatcher.utter_message(
                "Ich habe keine passende Info gefunden"
            )
            return []
        elif len(filtered_entites) <=0:
            dispatcher.utter_message("Für {}, den {} finden keine Veranstaltungen für Kinder statt".format(date_object.getWeekDay(), format_date))
            return []
        else:
            dispatcher.utter_message(text="Unser Programm ist vielfältig: Kunstausstellungen, Konzerte, Vorträge und vieles mehr! Bitte beachte, dass unser Museum Montags und Dienstags in der Regel geschlossen ist.")
            dispatcher.utter_message(text=message_text)
        message_to_send = {
            "type": query_result.entity_type,
            "items": filtered_entites,
        }

        dispatcher.utter_message(json_message=message_to_send)
        slots = [*query_result.slots , SlotSet("date", format_date)]
        return slots

class ActionCreationGeneral(Action):

    def name(self):
         return "action_werke_allgemein"

    def run(self, dispatcher, tracker, domain):
   
        creation_title = tracker.get_slot("creation")
        query_creation = query_entities(tracker=tracker, entity_type_param="creation",
        attr=[{'key': "title", 'value': creation_title, 'comp': equalComp}]) 
    
        if query_creation.error is not None:
            dispatcher.utter_message("Das habe ich nicht verstanden")
            return [SlotSet("email_type", "question_creation")]

        if not query_creation.result or len(query_creation.result) <= 0:
            message_to_send = {
                "text": "Leider habe ich keine Informationen zu diesem Werk. Möchtest Du eine Frage an meine Kolleginnen senden?",
                "buttons": [{"title": "Ja", "payload": "/affirm"},{"title": "Nein", "payload": "/deny"}]
            }
            dispatcher.utter_message(
                json_message=message_to_send
            )
            return [SlotSet("email_type", "question_creation")]

        creation_title = query_creation.result[0]["title"]
        creator_name = query_creation.result[0]["creator_name"]
        creation_date = query_creation.result[0]["creation_date"]
        

        message_to_send = {
            "links": [{
                "payload": query_creation.result[0]["link"],
                "title": query_creation.result[0]["title"]}],
            "text": ""
        }
        dispatcher.utter_message(text= f"""{creation_title} ist ein Kunstwerk von {creator_name} aus dem Jahr {creation_date}.
Hier findest Du weitere Informationen:""",json_message=message_to_send)


        slots = reset_attribute_slots([], query_creation.entity_type, tracker)
        dispatcher.utter_message(template="utter_antwort_hilfreich_frage")
        return  slots


class CreationYear(Action):
    def name(self):
        return "action_jahresuebersicht"

    def run(self, dispatcher, tracker, domain): 
        search_year = tracker.get_slot("year") or "1994"
        attr = [{"key": "creation_date", "value": search_year, "comp": equalComp}]
        query_year = query_entities(tracker=tracker,entity_type_param="creation", limit=200,
         attr=attr)

        message_to_send = {
        "type": query_year.entity_type,
        "items": query_year.result
         }

        dispatcher.utter_message(text= f"""Komm, wir gehen auf Zeitreise! Folgende Werke entstanden im Jahr {search_year}.""", json_message=message_to_send)
        slots = [SlotSet("creation_date", search_year)]
        return slots

class ProgrammTagesspezifisch(Action):
    """Action for querying events or workshops base on a date
        Returns a list of items.
    """

    def name(self):
        return "action_query_programm_tagesspezifisch"

    def run(self, dispatcher, tracker, domain):

        date_object = get_date(tracker)
        if (date_object is None):
            dispatcher.utter_message("Bitte geben Sie das Datum im folgenden Format an tt.mm.jjjj")
            return []
        date_value = date_object.value
        format_date = date_object.toGermanDate()

        message_text = "Hier das Programm für {}, den {}.".format(date_object.getWeekDay(), format_date)
        attr = [{"key": "date", "value": date_object.toEnglishDate(), "comp": compareDates}]

        event_type = tracker.get_slot("entity_type") or None
        if event_type is None:
            event_type = 'event'
        if event_type == 'event':
            event_type = 'ausstellungen'
        if (fuzz.ratio(event_type, "Ausstellungen") >80 or fuzz.ratio(event_type, "Ausstellung") >80):
            attr.append({"key": "category", "value": "exhibition", "comp": equalComp})
            message_text = "Am {}, den {} finden folgende Ausstellungen statt".format(date_object.getWeekDay(), format_date)
        
        # if event_type == 'Veranstaltungen':
        #     event_type = 'event'
        if (fuzz.ratio(event_type, "Workshop") >80 or fuzz.ratio(event_type, "Workshops") >80):
            attr.append({"key": "subcategory", "value": "workshop", "comp": equalComp})
            message_text = "Am {}, den {} finden folgende Workshops statt".format(date_object.getWeekDay(), format_date)
        # event_type = 'event'
        logger.debug(event_type)
        logger.debug(fuzz.ratio(event_type, "workshop"))
        # event_type = 'event'
        # query_result = query_entities(tracker=tracker, entity_type_param=event_type, attr=attr)
        query_result = query_entities(tracker=tracker, entity_type_param="event", attr=attr)

        end_date = date_value + timedelta(days=7)

        if query_result.error is not None:
            dispatcher.utter_message("Das habe ich nicht verstanden")
            return []

        elif not query_result.result or len(query_result.result) <= 0:
            dispatcher.utter_message(
                "Ich habe keine passende Info gefunden"
            )
            return []
        else:
            dispatcher.utter_message(text="Unser Programm ist vielfältig: Kunstausstellungen, Konzerte, Vorträge und vieles mehr! Bitte beachte, dass unser Museum Montags und Dienstags in der Regel geschlossen ist.")
            dispatcher.utter_message(text=message_text)

        entities = query_result.result
        filtered_entites = []
        for entity in entities:
            if (datetime.strptime(entity["date"]["end"][:10], '%Y-%m-%d').date() >= date_value and
                datetime.strptime(entity["date"]["start"][:10], '%Y-%m-%d').date() <= end_date):
                filtered_entites.append(entity)

        message_to_send = {
            "type": query_result.entity_type,
            "items": filtered_entites,
        }

        dispatcher.utter_message(json_message=message_to_send)
        slots = [*query_result.slots , SlotSet("date", format_date)]
        return slots

class ProgrammWochenende(Action):
    """Action for querying events or workshops based on the upcoming weekend
        Returns a list of items.
    """

    def name(self):
        return "action_query_programm_wochenende"

    def run(self, dispatcher, tracker, domain):

        date_object = Zdate(value=date.today())
        date_value = date_object.value
        format_date = date_object.toGermanDate()

        
        attr = [{"key": "date", "value": date_object.toEnglishDate(), "comp": compareDates}]

        query_result = query_entities(tracker=tracker, entity_type_param="event", attr=attr)

        weekno = datetime.today().weekday()
        start_date = None

        if(weekno == 5):
            start_date = date_value
        else:
            diff = 5 - weekno  
            start_date = date_value + timedelta(days=diff)

        end_date = start_date + timedelta(days=1)
        

        event_type = tracker.get_slot("entity_type") or None
        if fuzz.ratio(event_type, "workshop") >80:
            attr.append({"key": "subcategory", "value": "workshop", "comp": equalComp})
            message_text = "Am Wochenende, {} - {} finden folgende Workshops statt".format(start_date, end_date)

        message_text = "Hier das Programm für dieses Wochenende, {} - {}.".format(datetime.strftime(start_date, '%d.%m.%Y'), datetime.strftime(end_date, '%d.%m.%Y'))

        if query_result.error is not None:
            dispatcher.utter_message("Das habe ich nicht verstanden")
            return []

        elif not query_result.result or len(query_result.result) <= 0:
            dispatcher.utter_message(
                "Ich habe keine passende Info gefunden"
            )
            return []
        else:
            dispatcher.utter_message(text="Unser Programm ist vielfältig: Kunstausstellungen, Konzerte, Vorträge und vieles mehr! Bitte beachte, dass unser Museum Montags und Dienstags in der Regel geschlossen ist.")
            dispatcher.utter_message(text=message_text)

        entities = query_result.result
        filtered_entites = []
        for entity in entities:
            if (datetime.strptime(entity["date"]["end"][:10], '%Y-%m-%d').date() >= start_date and
                datetime.strptime(entity["date"]["start"][:10], '%Y-%m-%d').date() <= end_date):
                filtered_entites.append(entity)

        message_to_send = {
            "type": query_result.entity_type,
            "items": filtered_entites,
        }

        dispatcher.utter_message(json_message=message_to_send)
        slots = [*query_result.slots , SlotSet("date", format_date)]
        return slots

class ActionQueryAttribute(Action):
    """Action for querying a specific attribute of an entity."""

    def name(self):
        return "action_query_attribute"

    def run(self, dispatcher, tracker, domain):
        graph_database = db()
        entity_type = get_entity_key(graph_database, tracker)
        attribute = None
        if entity_type is None:
            return []

        # get name of entity and attribute of interest
        name = get_entity_name(tracker, entity_type)
        # date = get_attribute(tracker, attribute)

        attribute = get_attribute(graph_database, tracker)

        if name is None or attribute is None:
            return DbQueryResult(error="Slot entity type was None", result=None)
        else:
            slots = [SlotSet("mention", None)]
            reset_attribute_slots(slots, entity_type, tracker)
            return slots
        # query knowledge base
        key_attribute = schema[entity_type]["key"]
        value = graph_database.get_attribute_of(
            entity_type, key_attribute, name, attribute
        )

        slots = [SlotSet("mention", None), SlotSet(
            entity_type, name), SlotSet("eintritt", value)]
        reset_attribute_slots(slots, entity_type, tracker)
        return slots


class ActionQueryEventDate (Action):
    """Action for querying a specific attribute of an entity."""

    def name(self):
        return "action_query_event_date"

    def run(self, dispatcher, tracker, domain):

        # query_result = query_attribute(tracker=tracker, attr="date")
#______________________________________________________________________________________
#______________________________________________________________________________________
#______________________________________________________________________________________
        event_title = tracker.get_slot("event") or tracker.get_slot("PER")
        attr = [{"key": "title", "value": event_title, "comp": equalComp}]
        query_result = query_entities(tracker=tracker, attr=attr, entity_type_param="event")

        start_value = None
        end_value = None

        if query_result.error is not None:
            slots = [SlotSet("mention", None)]
            dispatcher.utter_message("Das habe ich nicht verstanden")
            return slots

        if (query_result.result is None or len(query_result.result) <= 0):
            dispatcher.utter_message("Nichts gefunden")
            return []

        value = query_result.result
        start_value = value[0]["date"]["start"]
        start_date = string_to_german_date(start_value)
        end_value = value[0]["date"]["end"]
        end_date = string_to_german_date(end_value)

        message_to_send = {
            "links": [{
                "payload": value[0]["link"],
                "title": value[0]["title"]}],
            "text": ""
        }

        dispatcher.utter_message(text= f"""Hier findest du einige Informationen zum Event: \n{event_title}. Geöffnet von {start_date} bis {end_date}""",json_message=message_to_send)
      
        slots = [SlotSet("date_start", start_value),
             SlotSet("date_end", end_value)]
        return slots

class SendCustomEmail (Action):
    """Action for querying a specific attribute of an entity."""

    def name(self):
        return "action_send_custom_email"

    def run(self, dispatcher, tracker, domain):

        prepare
        return slots


class ActionResolveEntity(Action):
    """Action for resolving a mention."""

    def name(self):
        return "action_resolve_entity"

    def run(self, dispatcher, tracker, domain):
        entity_type = tracker.get_slot("entity_type")
        listed_items = tracker.get_slot("listed_items")

        if entity_type is None:
            dispatcher.utter_template("utter_rephrase", tracker)
            return []

        # Check if entity was mentioned as 'first', 'second', etc.
        mention = tracker.get_slot("mention")
        if mention is not None:
            value = resolve_mention(tracker)
            if value is not None:
                return [SlotSet(entity_type, value), SlotSet("mention", None)]

        # Check if NER recognized entity directly
        # (e.g. bank name was mentioned and recognized as 'bank')
        value = tracker.get_slot(entity_type)
        if value is not None and value in listed_items:
            return [SlotSet(entity_type, value), SlotSet("mention", None)]

        dispatcher.utter_template("utter_rephrase", tracker)
        return [SlotSet(entity_type, None), SlotSet("mention", None)]


class EntranceFee (Action):
    """Action for querying a specific attribute of an entity."""

    def name(self):
        return "action_query_entrance"

    def run(self, dispatcher, tracker, domain):

        query_result = query_attribute(tracker=tracker, attr="entrancefee")
        entrance = query_result.result

        general_message = {
                "links": [{"title": "Eintrittspreise","payload": "https://zkm.de/de/ausstellungen-veranstaltungen/eintrittspreise"}],
                "text": """Eine Übersicht aller Ticketpreise findest Du auf unserer Homepage."""
        }
        
        if query_result.error is not None:
            dispatcher.utter_message(json_message= general_message)

            return query_result.slots

        if (query_result.result is None or len(query_result.result) <= 0):
            dispatcher.utter_message("Preise nicht gefunden")
            dispatcher.utter_message(json_message= general_message)
            return []
        
        value = query_result.result
        str_value = "".join(value)

        message_to_send = {
            "text": """Der Eintritt für die Ausstellung {} beträgt: 
            {}""".format(query_result.entity_name,str_value)
        }

        dispatcher.utter_message(json_message= message_to_send)
        dispatcher.utter_message(json_message= general_message)
        

        slots = query_result.slots + [SlotSet("eintritt", str_value)]
        return slots



class ActionUserValidation(FormAction):

    def name(self) -> Text:

        return "user_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        return ["num_people", "email", "phone_number", "visit_time", "subject", "kind_of_event"]

    def submit(self, dispatcher: CollectingDispatcher,
               tracker: Tracker,
               domain: Dict[Text, Any]) -> List[Dict]:

        dispatcher.utter_message(template="utter_submit")
        return []


class ActionNameValidation(FormAction):

    def name(self) -> Text:


        return "valid_name_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        return["name"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {
            "name": [
                self.from_entity(entity="PER"),
                self.from_text(),
            ],
        }

    def submit(self, dispatcher: CollectingDispatcher,
               tracker: Tracker,
               domain: Dict[Text, Any]) -> List[Dict]:
        name = tracker.get_slot("name")
        if name is None:
            dispatcher.utter_message(template="utter_ask_name")
        else:
            dispatcher.utter_message(f"Herzlich willkommen, " + name + "!" )
            dispatcher.utter_message(json_message={
                "name_provided": True
            })
        return []


class ActionSlotValues(Action):
    """Action for resolving a mention."""

    def name(self):
        return "action_slot_values"

    def run(self, dispatcher, tracker, domain):
        email_info = prepareEmailInfo(tracker)

        dispatcher.utter_message(json_message={
            "allowTyping": True,
            "inputContact": True,
            "text": email_info.message_text
        })
        return []


class ActionSlotValuesGuides(Action):
    """Action for resolving a mention."""

    def name(self):
        return "action_slot_values_guides"

    def run(self, dispatcher, tracker, domain):
        email_info = prepareEmailInfo(tracker)

        dispatcher.utter_message(json_message={
            "allowTyping": True,
            "inputContact": True,
            "isGuideContext": True,
            "text": email_info.message_text
        })
        return []

class ActionShopOpening(Action):
    """Action for showing opening times"""

    def name(self):
        return "action_shop_opening"

    def run(self, dispatcher, tracker, domain):
        URL = "https://data.zkm.de/api/open/shop"
        start_date = date.today()
        end_date = start_date + timedelta(days=10)
        PARAMS = {'date': start_date, 'date2': end_date}
        r = requests.get(url=URL, params=PARAMS)
        if (r.status_code != 200):
            dispatcher.utter_message(text="Es ist ein Fehler aufgetreten")
            return []
        data = r.json()
        print(data)
        message = [None] * 11
        for i in range(len(data)):
            if data[i]['open'] == True:
                message[i] = datetime.strptime(data[i]['date'], '%Y-%m-%d').strftime("%a, %d.%m.%Y") + ': ' + data[i]['start'] + ' - ' + data[i]['end'] + ' Uhr'
            else:
                message[i] = datetime.strptime(data[i]['date'], '%Y-%m-%d').strftime("%a, %d.%m.%Y") + ': Geschlossen'
            print(message[i])
        dispatcher.utter_message(json_message={
            "allowTyping": True,
            "text": '\n'.join(message)
        })
        # TO DO: Array als Liste / Text anzeigen, 1 funktion je endpoint (exhibition, library, infopoint)
        return []

class ActionUhrzeit(Action):
    """Action for showing opening times"""

    def name(self):
        return "action_uhrzeit"

    def run(self, dispatcher, tracker, domain):
        uhrzeit = datetime.strptime(str(datetime.now()), "%Y-%m-%d %H:%M:%S.%f").strftime("%H:%M")

        print("Uhrzeit: " + uhrzeit)
        slots = [SlotSet("uhrzeit", uhrzeit)]
        return slots


class ActionInfoPointOpening(Action):
    """Action for showing opening times"""

    def name(self):
        return "action_infopoint_opening"

    def run(self, dispatcher, tracker, domain):
        URL = "https://data.zkm.de/api/open/infopoint"
        start_date = date.today()
        end_date = start_date + timedelta(days=10)
        PARAMS = {'date': start_date, 'date2': end_date}
        r = requests.get(url=URL, params=PARAMS)
        data = r.json()
        print(data)
        if (r.status_code != 200):
            dispatcher.utter_message(text="Es ist ein Fehler aufgetreten")
            return []
        message = [None] * 11
        for i in range(len(data)):
            if data[i]['open'] == True:
                message[i] = datetime.strptime(data[i]['date'], '%Y-%m-%d').strftime("%a, %d.%m.%Y") + ': ' + \
                    data[i]['start'] + ' - ' + data[i]['end'] + ' Uhr'
            else:
                message[i] = datetime.strptime(data[i]['date'], '%Y-%m-%d').strftime("%a, %d.%m.%Y") + ': Geschlossen'
            print(message[i])
        dispatcher.utter_message(json_message={
            "allowTyping": True,
            "text": '\n'.join(message)
        })
        # TO DO: Array als Liste / Text anzeigen, 1 funktion je endpoint (exhibition, library, infopoint)
        return []


class ActionLibaryOpening(Action):
    """Action for showing opening times"""

    def name(self):
        return "action_library_opening"

    def run(self, dispatcher, tracker, domain):
        URL = "https://data.zkm.de/api/open/library"
        start_date = date.today()
        end_date = start_date + timedelta(days=10)
        PARAMS = {'date': start_date, 'date2': end_date}
        r = requests.get(url=URL, params=PARAMS)
        data = r.json()
        print(data)
        message = [None] * 11
        for i in range(len(data)):
            if data[i]['open'] == True:
                message[i] = datetime.strptime(data[i]['date'], '%Y-%m-%d').strftime("%a, %d.%m.%Y") + ': ' + \
                    data[i]['start'] + ' - ' + data[i]['end'] + ' Uhr'
            else:
                message[i] = datetime.strptime(data[i]['date'], '%Y-%m-%d').strftime("%a, %d.%m.%Y") + ': Geschlossen'
            print(message[i])
        dispatcher.utter_message(json_message={
            "allowTyping": True,
            "text": '\n'.join(message)
        })
        # TO DO: Array als Liste / Text anzeigen, 1 funktion je endpoint (exhibition, library, infopoint)
        return []


class ActionExhibitionOpening(Action):
    """Action for showing opening times"""

    def name(self):
        return "action_exhibition_opening"

    def run(self, dispatcher, tracker, domain):
        URL = "https://data.zkm.de/api/open/exhibition"
        start_date = date.today()
        end_date = start_date + timedelta(days=10)
        PARAMS = {'date': start_date, 'date2': end_date}
        r = requests.get(url=URL, params=PARAMS)
        data = r.json()
        print(data)
        message = [None] * 11
        for i in range(len(data)):
            if data[i]['open'] == True:
                message[i] = datetime.strptime(data[i]['date'], '%Y-%m-%d').strftime("%a, %d.%m.%Y") + ': ' + \
                    data[i]['start'] + ' - ' + data[i]['end'] + ' Uhr'
            else:
                message[i] = datetime.strptime(data[i]['date'], '%Y-%m-%d').strftime("%a, %d.%m.%Y") + ': Geschlossen'
            print(message[i])
        dispatcher.utter_message(json_message={
            "allowTyping": True,
            "text": '\n'.join(message)
        })
        # TO DO: Array als Liste / Text anzeigen, 1 funktion je endpoint (exhibition, library, infopoint)
        return []

        # Email senden


class Sendmail(Action):

    def name(self) -> Text:
        return "action_send_mail"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        email_content = tracker.get_slot("email_content")
        email_user = tracker.get_slot("email")
        email_info = prepareEmailInfo(tracker)
        guide = tracker.get_slot("guide_title")
        logger.debug("guide sending email")
        logger.debug(guide)
        logger.debug(email_content)
        logger.debug(email_user)
        logger.debug(email_info)

        email_context = tracker.get_slot("current_context")
        html_message = build_html_message(subject=email_info.subject, email=email_user, message=email_content, context=email_context)
        # html_message = email_info.message_html
        try:
            # set up the SMTP server
            email_server = smtplib.SMTP_SSL(host='mail.zkm.de', port=465)
            email_server.set_debuglevel(1)
            email_server.login(mailserver_user, mailserver_password)

            sender_email = "data@zkm.de"

            mail_to_send = MIMEMultipart('alternative')
            mail_to_send["subject"] = email_info.subject
            mail_to_send["from"] = sender_email
            # mail_to_send["to"] = "e.ersada@integr8.com"
            mail_to_send["to"] = email_info.email_receiver

            email_text = MIMEText(email_info.message_text, 'plain')
            email = MIMEText(html_message, 'html')
            
            mail_to_send.attach(email_text)
            mail_to_send.attach(email)

            email_server.sendmail(mail_to_send["from"], mail_to_send["to"], mail_to_send.as_string())

            email_server.quit()

            dispatcher.utter_message(text="Deine E-Mail wurde erfolgreich gesendet.")
            if(guide == 'labyrinth'):
                dispatcher.utter_message(buttons = [
                    {"payload":"/weiter_labyrinth", "title":"Weiter"}
                ])
            elif (guide == 'wipe'):
                dispatcher.utter_message(buttons = [
                    {"payload":"/weiter_wipe", "title":"Weiter"}
                ])
            elif (guide == 'texte'):
                dispatcher.utter_message(buttons = [
                    {"payload":"/weiter_texte", "title":"Weiter"}
                ])
            elif (guide == 'fuehrung'):
                dispatcher.utter_message(buttons = [
                    {"payload":"/weiter_fuehrung", "title":"Weiter"}
                ])
            # elif (guide == 'direkt'):
            #     dispatcher.utter_message(buttons = [
            #         {"payload":"/weiter_direkt", "title":"Weiter"}
            #     ])
            else:
                dispatcher.utter_message(buttons = [
                    {"payload":"/weiter_direkt", "title":"Weiter"}
                    # {"payload":"/weiter_hilfreich", "title":"Weiter"}
                ])

            return []
        except Exception as err:
            print(err)
            dispatcher.utter_message(text="Die E-mail konnte leider nicht gesendet werden.")
            return []

class GuideSendMail(Action):

    def name(self) -> Text:
        return "action_guide_send_mail"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        logger.debug("inside action_send_mail_guide")
        email_content_test = tracker.get_slot("email_content")
        email_user_test = tracker.get_slot("email")
        email_info_test = prepareEmailInfo(tracker)

        html_message = build_html_message(subject=email_info_test.subject, email=email_user_test, message=email_content_test)

        try:
            # set up the SMTP server
            email_server = smtplib.SMTP_SSL(host='mail.zkm.de', port=465)
            email_server.set_debuglevel(1)
            email_server.login(mailserver_user, mailserver_password)

            sender_email = "data@zkm.de"

            mail_to_send = MIMEMultipart('alternative')
            mail_to_send["subject"] = email_info_test.subject
            mail_to_send["from"] = sender_email
            # mail_to_send["to"] = "e.ersada@integr8.com"
            mail_to_send["to"] = email_info_test.email_receiver

            email_text = MIMEText(email_info_test.message_text, 'plain')
            email = MIMEText(html_message, 'html')
            
            mail_to_send.attach(email_text)
            mail_to_send.attach(email)

            email_server.sendmail(mail_to_send["from"], mail_to_send["to"], mail_to_send.as_string())

            email_server.quit()

            dispatcher.utter_message(text="Deine E-Mail wurde erfolgreich gesendet.")
            
            return []
        except Exception as err:
            print(err)
            dispatcher.utter_message(text="Die E-mail konnte leider nicht gesendet werden.")
            return []
        


class EventCategoryExibition(Action):
    """Action for querying a specific attribute of an entity."""

    def name(self):
        return "action_category_exibition"

    def run(self, dispatcher, tracker, domain):

        query_result = query_attribute(tracker=tracker, attr="category")

       
        if query_result.error is not None:
            dispatcher.utter_message("Das habe ich nicht verstanden")
            

        if (query_result.result is None or len(query_result.result) <= 0):
            dispatcher.utter_message("Nichts gefunden")
            return []

        value = query_result.result
      
        dispatcher.utter_message("TEST")

        slots = query_result.slots + [SlotSet("category", value)]
        return slots  

class EventCategoryLecture(Action):
    """Action for querying a specific attribute of an entity."""

    def name(self):
        return "action_category_lecture"

    def run(self, dispatcher, tracker, domain):
        graph_database = db()

        last_intent = tracker.latest_message['intent']['name']

        # first need to know the entity type we are looking for
        entity_type = get_entity_key(graph_database, tracker)
        attribute = None
        if entity_type is None:
            return []

        # get name of entity and attribute of interest
        name = get_entity_name(tracker, entity_type)
        # date = get_attribute(tracker, attribute)

        if (last_intent == "kategorie_vortrag"):
            attribute = "category"

        # attribute = get_attribute(graph_database, tracker)
        # logger.debug(
        #     "name of entity {}, attribute requested {}".format(name, attribute))

        if name is None or attribute is None:
            dispatcher.utter_message("Das habe ich nicht verstanden")
            # dispatcher.utter_template("utter_rephrase", tracker)
            slots = [SlotSet("mention", None)]
            reset_attribute_slots(slots, entity_type, tracker)
            return slots
        # query knowledge base
        key_attribute = schema[entity_type]["key"]
        value = graph_database.get_attribute_of(
            entity_type, key_attribute, name, attribute
        )

        if value is not None and date is not None:
            dispatcher.utter_message(
                f"Am Tag {date} finden folgende Vorträge statt: {value}")
        else:
            dispatcher.utter_message(
                f"Tut mir Leid! An diesem Tag gibt es leider keine {value}"
            )

        slots = [SlotSet("mention", None), SlotSet(
            entity_type, name), SlotSet("category", value)]
        reset_attribute_slots(slots, entity_type, tracker)
        return slots


class EventCategoryConcert(Action):
    """Action for querying a specific attribute of an entity."""

    def name(self):
        return "action_category_concert"

    def run(self, dispatcher, tracker, domain):
        graph_database = db()

        last_intent = tracker.latest_message['intent']['name']

        # first need to know the entity type we are looking for
        entity_type = get_entity_key(graph_database, tracker)
        attribute = None
        if entity_type is None:
            return []

        # get name of entity and attribute of interest
        name = get_entity_name(tracker, entity_type)
        # date = get_attribute(tracker, attribute)

        if (last_intent == "kategorie_konzert"):
            attribute = "subcategory"

        # attribute = get_attribute(graph_database, tracker)
        # logger.debug(
        #     "name of entity {}, attribute requested {}".format(name, attribute))

        if name is None or attribute is None:
            dispatcher.utter_message("Das habe ich nicht verstanden")
            # dispatcher.utter_template("utter_rephrase", tracker)
            slots = [SlotSet("mention", None)]
            reset_attribute_slots(slots, entity_type, tracker)
            return slots
        # query knowledge base
        key_attribute = schema[entity_type]["key"]
        value = graph_database.get_attribute_of(
            entity_type, key_attribute, name, attribute
        )

        if value is not None and date is not None:
            dispatcher.utter_message(f"Am Tag {date} finden Konzerte statt")
        else:
            dispatcher.utter_message(
                f"Tut mir Leid! An diesem Tag gibt es leider keine Konzerte"
            )

        slots = [SlotSet("mention", None), SlotSet(
            entity_type, name), SlotSet("category", value)]
        reset_attribute_slots(slots, entity_type, tracker)
        return slots


class EventCategoryWorkshop(Action):
    """Action for querying a specific attribute of an entity."""

    def name(self):
        return "action_category_workshop"

    def run(self, dispatcher, tracker, domain):
        graph_database = db()

        last_intent = tracker.latest_message['intent']['name']

        # first need to know the entity type we are looking for
        entity_type = get_entity_key(graph_database, tracker)
        attribute = None
        if entity_type is None:
            return []

        # get name of entity and attribute of interest
        name = get_entity_name(tracker, entity_type)
        # date = get_attribute(tracker, attribute)

        if (last_intent == "kategorie_workshop"):
            attribute = "category"

        # attribute = get_attribute(graph_database, tracker)
        # logger.debug(
        #     "name of entity {}, attribute requested {}".format(name, attribute))

        if name is None or attribute is None:
            dispatcher.utter_message("Das habe ich nicht verstanden")
            # dispatcher.utter_template("utter_rephrase", tracker)
            slots = [SlotSet("mention", None)]
            reset_attribute_slots(slots, entity_type, tracker)
            return slots
        # query knowledge base
        key_attribute = schema[entity_type]["key"]
        value = graph_database.get_attribute_of(
            entity_type, key_attribute, name, attribute
        )

        if value is not None and date is not None:
            dispatcher.utter_message(f"Am Tag {date} finden Workshops statt")
        else:
            dispatcher.utter_message(
                f"Tut mir Leid! An diesem Tag gibt es leider keine Workshops"
            )

        slots = [SlotSet("mention", None), SlotSet(
            entity_type, name), SlotSet("category", value)]
        reset_attribute_slots(slots, entity_type, tracker)
        return slots

class ActionWerkeKuenstler(Action):
    """Action for querying a specific attribute of an entity."""

    def name(self):
        return "action_werke_kuenstler"

    def run(self, dispatcher, tracker, domain):
        artist_name = tracker.get_slot("person") or tracker.get_slot("PER")
        attr = [{"key": "creator_name", "value": artist_name, "comp": equalComp}]
        query_result = query_entities(tracker=tracker, attr=attr, entity_type_param="creation")

        if query_result.error is not None:
            dispatcher.utter_message("Das habe ich nicht verstanden")
            

        if (query_result.result is None or len(query_result.result) <= 0):
            dispatcher.utter_message("Leider konnte ich von {} keine Werke in der Sammlung finden.".format(artist_name))
            return []

        entities = query_result.result

        message_to_send = {
            "type": query_result.entity_type,
            "items": entities,
        }
        dispatcher.utter_message(text="Von {} haben wir folgende Werke in der Sammlung.".format(artist_name))
        dispatcher.utter_message(json_message=message_to_send)
        slots = reset_attribute_slots(query_result.slots, query_result.entity_type, tracker)
        return slots

class ActionAustellungKatalog(Action):
    """Action for querying a specific attribute of an entity."""

    def name(self):
        return "action_ausstellung_katalog"

    def run(self, dispatcher, tracker, domain):
        publication_name = tracker.get_slot("event")
        # publication_name = "MultiMediale" #tracker.get_slot("event")
        attr = [{"key": "title", "value": publication_name, "comp": equalComp}]
        query_result = query_entities(tracker=tracker, attr=attr, entity_type_param="publication")

        if query_result.error is not None:
            dispatcher.utter_message("Das habe ich nicht verstanden")
            
        if (query_result.result is None or len(query_result.result) <= 0):
            message_to_send = {
                "text": "Leider gibt es zu dieser Ausstellung keine Publikation. Soll ich bei meinen Kolleginnen nachfragen, ob sie gerade noch daran arbeiten?",
                "buttons": [{"title": "Ja", "payload": "/affirm"},{"title": "Nein", "payload": "/deny"}]
            }
            dispatcher.utter_message(json_message=message_to_send)
            return [SlotSet("email_type", "ask_for_publication"), SlotSet("publication", publication_name)]

        publication = query_result.result[0]

        message_to_send = {
            "links": [{
                "payload": "{}".format(publication["shop_link"]),
                "title": publication_name
                }],
            "text": "Ja, es gibt eine Publikation. Unter dem folgenden Link findest du weitere Informationen."
        }

        dispatcher.utter_message(json_message=message_to_send)

        ask_want_to_buy_message = {
                "text": "Du kannst die Publikation gerne direkt per Mail bei uns bestellen. ",
                "buttons": [{"title": "Publikation bestellen", "payload": "/affirm"},{"title": "Nein, danke", "payload": "/deny"}]
        }

        dispatcher.utter_message(json_message=ask_want_to_buy_message)
        return [*query_result.slots, SlotSet("email_type", "buy_publication"), SlotSet("publication", publication_name)]

class ActionWerke(Action):
    """ Action werke"""

    def name(self):
        return "action_werke"

    def run(self, dispatcher, tracker, domain):
        event_name = tracker.get_slot("event") or ""

        if "Writing the History" in event_name or "Gameplay" in event_name:
            message_to_send = {
            "links": [{"payload": "https://zkm.de/de/sammlung-archive/sammlung/die-sammlung-des-zkm", "title": "Werke des ZKMs"}],
            "text": "In unserer Computerspiele-Ausstellung {} findest Du folgende Werke".format(event_name),
            "img": "https://zkm.de/media/bild/2018_zkm_gameplay_ausstellungsansicht_003.jpg"
            }
            dispatcher.utter_message(json_message=message_to_send)
            return []

        message_to_send = {
            "links": [{"payload": "https://zkm.de/de/sammlung-archive/sammlung/die-sammlung-des-zkm", "title": "Werke des ZKMs"}],
            "text": "Das weiß ich leider nicht genau. Möchtest Du selbst auf der Website zur Ausstellung nachsehen?"
        }

        dispatcher.utter_message(json_message=message_to_send)
        return []

class GetGuideInfo(Action):
    """GetGuideInfo"""

    def name(self):
        return "action_get_guide_info"

    def run(self, dispatcher, tracker, domain):
        guide = tracker.get_slot("guide_title")
        dispatcher.utter_message(f"Test Guide {guide}")
        # dispatcher.utter_message(json_message=[{
        #     "allowTyping": False,
        #     "text": guide_name
        # }])
        return []


class ActionTerminWorkshops(Action):
    """
    ActionTerminWorkshops will perform the following:
    check if a name was provided, then query the date of a workshop with it.
    check if a date was provided, then query a list of workshops base on it.
    if no name or date provided, then query a list of workshops based on todays date
    """

    def name(self):
        return "action_termin_workshops"

    def run(self, dispatcher, tracker, domain):

        query_result = query_attribute(tracker=tracker, attr="date")

        if query_result.error is not None or query_result.result is None or len(query_result.result) <= 0:

            date_object = Zdate(value=date.today())
            date_value = date_object.value
            end_date = date_value + timedelta(days=7)
            format_date = date_object.toGermanDate()

            attr = [{"key": "date", "value": date_object.toEnglishDate(), "comp": compareDates},
                    {"key": "subcategory", "value": "workshop", "comp": equalComp}]
            query_workshop_list = query_entities(tracker=tracker, entity_type_param="event", attr=attr)

            if query_workshop_list.error is not None:
                dispatcher.utter_message("Das habe ich nicht verstanden")
                return []

            if not query_workshop_list.result or len(query_workshop_list.result) <= 0:
                dispatcher.utter_message(
                    "Am %s, %s bieten wir leider keine workshops an" % (date_object.getWeekDay(), format_date)
                )

            entities = query_workshop_list.result
            filtered_entites = []
            for entity in entities:
                if (datetime.strptime(entity["date"]["end"][:10], '%Y-%m-%d').date() >= date_value and datetime.strptime(entity["date"]["start"][:10], '%Y-%m-%d').date() <= end_date):
                    filtered_entites.append(entity)

            message_to_send = {
                "type": query_workshop_list.entity_type,
                "items": filtered_entites,
            }

            dispatcher.utter_message(json_message=message_to_send)
            slots = [*query_workshop_list.slots , SlotSet("date", format_date)]
            slots = reset_attribute_slots(slots, query_workshop_list.entity_type, tracker)
            return slots

        value = query_result.result
        start_value = value[0]["start"]
        end_value = value[0]["end"]

        dispatcher.utter_message(text="Der Workshop {} findet am {} bis {} statt. Weitere Informationen findest Du auf unserer Website.".format(query_result.entity_name, start_value, end_value))
      
        slots = [SlotSet("date_start", start_value), SlotSet("date_end", end_value)]
        slots = reset_attribute_slots(slots, query_result.entity_type, tracker)
        return slots

