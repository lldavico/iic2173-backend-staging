#!/bin/bash
sudo apt update
cd /e1/backend-project
sudo docker-compose -f docker-compose.test.yml down --remove-orphans
sudo docker-compose -f docker-compose.test.yml build