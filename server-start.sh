#!/bin/bash
sudo apt update
cd e1
cd backend-project
sudo docker-compose -f docker-compose.test.yml down --remove-orphans
sudo docker-compose -f docker-compose.test.yml build
sudo docker-compose -f docker-compose.test.yml up -d


