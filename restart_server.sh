#!/bin/bash

echo "Shutting down server"
sudo docker-compose down
echo "Starting server"
sudo docker-compose up -d
echo "Done"
