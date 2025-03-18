#!/bin/bash

# Allow X11 connections from local docker containers
xhost +local:docker

# Build and start the container
docker-compose build
docker-compose up -d

# Enter the container
docker-compose exec puppy_ros bash

# When exiting the container, this will run
echo "Container session ended. To stop the container, run: docker-compose down" 