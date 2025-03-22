#!/bin/bash

echo "====================================================="
echo "PuppyPi Robot Walking Test"
echo "====================================================="
echo "This script will launch the robot and test the walking functionality"

# Set error handling
set -e

# Stop and remove any existing containers
echo "Cleaning up existing containers..."
docker stop docker_simulation_run &>/dev/null || true
docker rm docker_simulation_run &>/dev/null || true

# Allow X11 connections (Linux only)
echo "Setting up X11 forwarding..."
xhost +local:docker &>/dev/null

# Path to docker-compose file
DOCKER_COMPOSE_FILE="$(pwd)/docker/docker-compose.yml"

# Build and run using Docker Compose
echo "Building and launching in simulation mode..."

# Define custom command to run Gazebo and the walking test
CUSTOM_COMMAND="roslaunch puppy_description gazebo.launch && sleep 5 && cd /ros_ws/src/puppy_description/scripts && python3 movement_test.py"
echo "Will run: $CUSTOM_COMMAND"

# Build and run
docker-compose -f "$DOCKER_COMPOSE_FILE" build simulation
docker-compose -f "$DOCKER_COMPOSE_FILE" run --rm simulation bash -c "$CUSTOM_COMMAND"

# Cleanup on exit
echo "Cleaning up..."
docker-compose -f "$DOCKER_COMPOSE_FILE" down

echo "====================================================="
echo "Test completed: $(date)"
echo "=====================================================" 