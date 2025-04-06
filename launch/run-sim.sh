#!/bin/bash

# Wrapper script to launch Gazebo simulation with Docker Compose

# Set X11 permissions for Docker
echo "Setting X11 permissions..."
xhost +local:docker

# Launch the simulation with Docker Compose
echo "Starting Gazebo with robot using Docker Compose..."
docker-compose up

# Note: Press Ctrl+C to stop the simulation
# After stopping with Ctrl+C, run 'docker-compose down' to clean up 