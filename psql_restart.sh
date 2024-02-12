#!/usr/bin/zsh

sudo systemctl stop postgresql ; \
sudo systemctl start postgresql ; \
sudo pg_isready ; \
