#!/usr/bin/bash

git clone https://github.com/va0r/diploma.git ; \
cd diploma ; \
python3 -m venv env ; \
. ./env/bin/activate ; \
sudo docker compose -f docker-compose.yml up --build ; \
