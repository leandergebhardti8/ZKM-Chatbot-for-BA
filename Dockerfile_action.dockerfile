FROM rasa/rasa-sdk:2.4.1
WORKDIR /app
USER root
RUN \
    apt-get update && \
    apt-get install -y default-libmysqlclient-dev build-essential && \
    apt-get install -y locales && \
    locale-gen "de_DE.UTF-8" && \
    pip3 install --upgrade pip && \
    pip3 install wheel && \
    pip3 install rasa==2.4.3 && \
    pip3 install spacy==3.0.5 && \
    pip3 install fuzzywuzzy==0.18.0 && \
    python3 -m spacy download de_core_news_md
ENV LC_CTYPE="C.UTF-8" \
    LC_ALL="C.UTF-8" \
    LANG="C.UTF-8" \
    rasa_env="production"
COPY ./actions /app/actions
COPY ./graph_db.py /app/graph_db.py
COPY ./export.json /app/export.json
USER 1001