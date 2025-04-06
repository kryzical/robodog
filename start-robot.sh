#!/bin/bash

# Main script to launch the robot simulation using Docker Compose

# Set X11 permissions for Docker
echo "Setting X11 permissions..."
xhost +local:docker

# Launch the simulation with Docker Compose
echo "Starting Gazebo with robot using Docker Compose..."
cd docker && docker compose up

# Note: Press Ctrl+C to stop the simulation 