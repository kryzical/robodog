#!/bin/bash

# This script launches Gazebo and spawns a robot model

# Move to the project root directory (assuming scripts is one level down from root)
cd "$(dirname "$0")/.." || exit

# Set X11 permissions for Docker
echo "Setting X11 permissions..."
xhost +local:docker

# Start Gazebo with robot using Docker Compose
echo "Starting Gazebo with robot using Docker Compose..."
docker compose -f docker/docker-compose.yml up

# Note: Press Ctrl+C to stop the simulation 