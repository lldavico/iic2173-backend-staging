#!/bin/bash
cd e1
cd backend-project
sudo docker-compose -f docker-compose.test.yml down
sudo docker stop $(docker ps -a -q)
