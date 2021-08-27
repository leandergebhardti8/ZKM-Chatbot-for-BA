#!/bin/bash

typeset -a allowed_cors=(https://webqa.zkm.de http://chatbot8.zkm.de https://zkm.de https://zkm-chatbot.s3.eu-central-1.amazonaws.com http://localhost)

rasa run actions --actions actions.actions --debug & 
rasa run -m models --enable-api --debug  --endpoints endpoints.yml --credentials credentials.yml --log-file out.log --cors allowed_cors --debug --auth-token secretsalt 

