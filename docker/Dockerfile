# Dockerfile for raptorapp
FROM continuumio/miniconda3:latest

# Install host dependencies
RUN apt update
RUN apt install libmariadb-dev -y
RUN apt install gcc -y
RUN python -m pip install --upgrade pip

# Copy Conda environment and install environment
COPY ../environment.yml environment.yml
RUN conda env create

# Add initialization script and define entrypoint
ADD docker/init init
RUN chmod +x+r -R init
ENTRYPOINT ["/init/run-raptorapp.sh"]
