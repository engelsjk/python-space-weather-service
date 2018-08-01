#!/bin/sh

sudo apt update 
sudo apt install python3-pip 
sudo -H pip3 install -U pipenv
sudo apt-get install python3-tk

pipenv install

pipenv run flask run -h 0.0.0.0