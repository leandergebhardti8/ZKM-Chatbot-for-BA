
# Extend the official Rasa image
FROM ubuntu:18.04

WORKDIR app
RUN \
    apt-get update && \
    apt-get install -y python3.7 python3-pip default-libmysqlclient-dev build-essential && \
    apt-get install -y locales && \
    locale-gen "de_DE.UTF-8" && \
    pip3 install --upgrade pip && \
    pip3 install rasa==1.10.2 && \
    pip3 install spacy==2.1.9 && \
    pip3 install mysqlclient==2.0.2 && \
    pip3 install fuzzywuzzy[speedup] && \
    python3 -m spacy download de_core_news_sm && \
    python3 -m spacy link de_core_news_sm de_core_news_sm

ENV LC_CTYPE="de_DE.UTF-8" \
    LC_ALL="de_DE.UTF-8" \
    LANG=de_DE.UTF-8 \
    rasa_env="production"

COPY . .
RUN ["chmod", "+x", "start.sh"]


ENTRYPOINT []
CMD ["./start.sh"]
