#!/usr/bin/bash

git clone https://github.com/va0r/diploma.git ; \
cd diploma ; \
sudo docker compose -f docker-compose.yml up --build
