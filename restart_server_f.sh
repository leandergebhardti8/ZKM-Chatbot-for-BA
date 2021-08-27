
#!/bin/bash

echo "Shutting down server"
sudo docker-compose down --rmi=all
echo "Starting server"
sudo docker-compose up -d
echo "Done"
