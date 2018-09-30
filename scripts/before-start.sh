#!/usr/bin/env bash
# use this script to run needed actions before start the app
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput

