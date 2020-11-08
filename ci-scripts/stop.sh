#!/bin/bash
cd ..
sudo docker-compose -f /home/ubuntu/e1/backend-project/docker-compose.test.yml down
sudo docker stop $(docker ps -aq)
