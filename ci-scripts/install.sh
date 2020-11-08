#!/bin/bash
sudo apt update
sudo docker-compose -f ../docker-compose.test.yml down --remove-orphans
sudo docker-compose -f ../docker-compose.test.yml build