# Dockerfile for raptorapp

FROM continuumio/miniconda3:latest

COPY environment.yml environment.yml

RUN apt update

RUN python -m pip install --upgrade pip

RUN apt install libmariadb-dev -y

RUN apt install gcc -y

RUN conda env create
