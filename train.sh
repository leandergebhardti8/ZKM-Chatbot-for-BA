#!/bin/bash

echo "Running training script"
sudo docker exec -i rasa-worker python3 < train.py

echo "Training is done, services are gonna be restarted"
sudo sh restart_server.sh
