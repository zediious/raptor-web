FROM continuumio/miniconda3:latest

COPY /raptorWeb raptorWeb

COPY /config/nginx/conf.d/* etc/nginx/conf.d

WORKDIR /raptorWeb

RUN conda env create

WORKDIR /

# EXPOSE 9096

# CMD exec conda run -n djangoWork python manage.py makemigrations && conda run -n djangoWork python manage.py migrate && gunicorn raptorWeb.wsgi:application --bind 0.0.0.0:443 --workers 4
