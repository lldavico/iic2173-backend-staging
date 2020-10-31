#!/bin/bash
sudo docker-compose -f docker-compose.test.yml down
sudo docker stop $(docker ps -a -q)
