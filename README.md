Google Analytics 
========================

Welcome to Google Analytics

Installation
--------------
* pip install pipenv
* pipenv install
* mv .env_example .env
* mv yoyo_example.ini yoyo.ini
* update .env and yoyo.ini
* source .env 
* pipenv run yoyo apply ./migrations


Command list
--------------
pipenv run python application.py


Useful commands
--------------
* commands that beginning from *ga:* - load data from google analytics
* commands that beginning from *csv:* - load data from csv file
* commands that beginning from *report:* - generate specific report
