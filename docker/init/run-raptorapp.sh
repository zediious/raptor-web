#!/bin/bash

# Move to app directory
cd raptorWebApp

# Migrate database
conda run -n djangoWork python manage.py migrate

# Collect static files for serving
conda run -n djangoWork python manage.py collectstatic --noinput

# Create superuser if no users exist
conda run -n djangoWork python manage.py createSuper

# Run celery beat
conda run -n djangoWork celery -A config.celery beat --loglevel=info --detach

# Run celery worker server
conda run -n djangoWork celery -A config worker -l INFO --detach 

# Run Django development server, NOT suitable for production!
conda run -n djangoWork python manage.py runserver 0.0.0.0:80