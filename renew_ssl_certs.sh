#!/bin/bash

sudo docker-compose down
sudo certbot renew
sudo cp /etc/letsencrypt/live/chatbot8.zkm.de/privkey.pem /etc/zkm-chatbot/certs
sudo cp /etc/letsencrypt/live/chatbot8.zkm.de/fullchain.pem /etc/zkm-chatbot/certs
sudo docker-compose up -d
sudo echo "renew certs was executed" >> cronjobs.txt
