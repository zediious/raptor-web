#!/bin/bash

# Move to app directory
cd raptorWebApp

# Wait for 15 seconds to allow database to start completely
sleep 15

# Migrate database
python manage.py migrate

# Collect static files for serving
python manage.py collectstatic --noinput

# Create superuser if no users exist
python manage.py createSuper

# Run celery beat
celery -A config.celery beat --loglevel=info --detach

# Run celery worker server
celery -A config worker -l INFO --detach 

# Run asgi server
daphne -b 0.0.0.0 -p 80 config.asgi:application
