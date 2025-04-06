#!/bin/bash

# Script to forcefully remove any existing containers that might conflict

echo "Forcefully stopping and removing all Docker containers..."
docker stop $(docker ps -a -q) 2>/dev/null || true
docker rm $(docker ps -a -q) 2>/dev/null || true

echo "All containers have been removed."
echo "You can now run 'docker compose up' safely." 