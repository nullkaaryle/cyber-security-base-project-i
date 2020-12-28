# Cyber Security Base 2020 - Project I

The project was made using recommended "Writing your first Django app" tutorial.

## Installation instructions:

Run in terminal (in folder mysite) to start the project development server with a database and some data:
* python3 manage.py migrate 
* python3 manage.py loaddata polls-seed.json
* python3 manage.py runserver

Open web browser and go to http://localhost:8000 (default port)
* you can login as a admin in http://localhost:8000/admin
* you can login as user bob or alice in http://localhost:8000/polls
* you can find the secret page at http://localhost:8000/polls/admin
