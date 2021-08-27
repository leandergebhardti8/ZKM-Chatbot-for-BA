
# Extend the official Rasa image
FROM ubuntu:18.04

ENV FLASK_APP=start_worker.py
WORKDIR app
RUN \
    apt-get update && \
    apt-get install -y python3.7 python3-pip && \
    pip3 install --upgrade pip && \
    pip3 install rasa==1.10.2 && \
    pip3 install spacy==2.1.9 && \
    pip3 install requests && \
    pip3 install flask && \
    pip3 install fuzzywuzzy[speedup] && \
    python3 -m spacy download de_core_news_sm && \
    python3 -m spacy link de_core_news_sm de_core_news_sm

COPY . .
RUN ["chmod", "+x", "start_worker.py"]


ENTRYPOINT []
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]
