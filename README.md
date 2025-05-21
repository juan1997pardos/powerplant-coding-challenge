## Powerplant Coding Challenge
This project implements a RESTful API using FastAPI, a modern web framework for building APIs with Python 3. 
The endpoint /productionplan accepts JSON input and returns JSON output as specified in the challenge.
This solution runs on docker as suggested un the "want more challenge?" and aslo takes in to account the co2 costs.

## Aditional features
As an extra feature, the API logs each request, response, total load, total cost, and any errors to a SQLite database. When running in Docker, the database is persisted using a mounted volume, ensuring that logs are preserved across container restarts.

## Prerequisites
To run this project on docker you need to have installed:
Docker (Docker Engine and/or Docker CLI)
You can check if docker is installed by running::
docker --version

## DOCKER
You have 2 options to run docker-compose or run docker manually

## Option 1
# Using docker-compose
## Run the service
docker-compose up -d
## Stop the service
docker-compose down

## Option 2
## Run docker manually
# Build image
docker build -t powerplant-api .
# Run container
# Windows (PowerShell o CMD):
docker run -d -p 8888:8888 -v ${PWD}/data:/app/data powerplant-api
# Linux / macOS:
docker run -d -p 8888:8888 -v $(pwd)/data:/app/data powerplant-api

# Usefull comands:
# See live logs
docker logs -f powerplant-api
# Manual stop of the container
docker stop powerplant-api
# restart container
docker start powerplant-api
# permanently delete container
docker rm -f powerplant-api


# Access the API
http://localhost:8888/docs