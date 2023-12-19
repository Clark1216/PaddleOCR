#!/bin/bash

# startup containers
export VERSION="$(cat version.txt)"
export COMPOSE_PROJECT_NAME="$(cat project_name.txt)"
docker-compose build
