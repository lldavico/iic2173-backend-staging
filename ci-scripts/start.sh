#!/bin/bash
sudo apt update
cd ..
sudo docker-compose -f /home/ubuntu/e1/backend-project/docker-compose.test.yml up -d