#!/usr/bin/env bash

echo "db is up"
python wsgi.py create_db
python wsgi.py db init
python wsgi.py db migrate
python wsgi.py runserver