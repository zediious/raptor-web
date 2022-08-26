FROM continuumio/miniconda3:latest

COPY /raptorWeb raptorWeb

COPY /config/nginx/conf.d/* etc/nginx/conf.d

WORKDIR /raptorWeb

RUN conda env create

WORKDIR /
