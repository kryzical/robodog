#!/bin/bash

# Cleanup script to stop and remove Docker containers

echo "Stopping and removing Docker containers..."
docker-compose down

echo "Cleaning up any other containers..."
docker stop $(docker ps -aq) 2>/dev/null || true
docker rm $(docker ps -aq) 2>/dev/null || true

echo "Cleanup complete!" 