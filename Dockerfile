FROM continuumio/miniconda3:latest

COPY /raptorWeb raptorWeb

WORKDIR /raptorWeb

RUN conda env create

WORKDIR /
