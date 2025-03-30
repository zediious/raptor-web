# Dockerfile for raptorapp
FROM continuumio/miniconda3:latest as build_image

# Install host dependencies
RUN apt update
RUN apt install libmariadb-dev -y
RUN apt install gcc -y
RUN apt install libc6 -y

# Copy and install environment
COPY environment.yml environment.yml
RUN conda env create

# Install conda-pack:
RUN conda install -c conda-forge conda-pack

# Use conda-pack to create a standalone enviornment
RUN conda-pack -n djangoWork -o /tmp/env.tar && \
  mkdir /venv && cd /venv && tar xf /tmp/env.tar && \
  rm /tmp/env.tar

# Extract standalone environment to /venv/
RUN /venv/bin/conda-unpack

# The Runtime Image
FROM ubuntu:22.04 AS runtime_image

# Install necessary host dependencies
RUN apt update
RUN apt install libmariadb-dev -y
RUN apt install gcc -y
RUN apt install libc6 -y

# Copy /venv from the previous stage:
COPY --from=build_image /venv /venv

# Copy project files
COPY . /raptorWebApp

# Define entrypoint
RUN chmod +x+r -R /raptorWebApp/docker/init
RUN chmod +x+r /venv/bin/activate
SHELL ["/bin/bash", "-c"]
ENTRYPOINT source /venv/bin/activate && \
           ./raptorWebApp/docker/init/run-raptorapp-prod.sh
