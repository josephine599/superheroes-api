# Superheroes API

## Description
A Flask RESTful API to manage superheroes and their superpowers.  
- View heroes and powers  
- Add hero-power relationships  
- Update powers  

## Create & activate virtual environment:

- python3 -m venv venv
- source venv/bin/activate 

## Install dependencies:

- pip install -r requirements.txt


## Initialize database and migrate:

- flask db init
- flask db migrate -m "Initial migration"
- flask db upgrade


## Seed database:

- python seed.py


## Run server:

- python app.py


### Server runs at http://127.0.0.1:5555.

## Setup

1. Clone repo and enter directory:

git clone <git@github.com:josephine599/superheroes-api.git>
cd superheroes-api

