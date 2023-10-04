#!/bin/bash
## install the all necessary dependencies using requirement.text

sudo apt update

sudo apt install python3-pip python3-venv

pip install -r requirements.txt


### install flask and gunicorn for application dependencies  

pip install flask gunicorn


#### run the gunicorn for application on 8000 port

gunicorn api:app --bind=0.0.0.0:8000 --workers=4 --timeout=400
