#!/bin/bash
cd /e1/backend-project
sudo docker-compose -f docker-compose.test.yml down
sudo docker stop $(docker ps -a -q)
