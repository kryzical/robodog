#!/bin/bash

# Script to launch the PuppyPi robot simulation with multiple options
# Usage: ./run_robot.sh [simulation|dev|rviz]

# Default mode
MODE=${1:-simulation}

# Check for valid mode
if [[ "$MODE" != "simulation" && "$MODE" != "dev" && "$MODE" != "rviz" ]]; then
  echo "Error: Invalid mode. Choose from: simulation, dev, rviz"
  exit 1
fi

# Stop and remove any existing containers
echo "Cleaning up existing containers..."
docker stop puppy_robot_simulation puppy_robot_dev puppy_robot_rviz &>/dev/null || true
docker rm puppy_robot_simulation puppy_robot_dev puppy_robot_rviz &>/dev/null || true

# Allow X11 connections (Linux only)
echo "Setting up X11 forwarding..."
xhost +local:docker &>/dev/null

# Build and run using Docker Compose
echo "Building and launching in $MODE mode..."
docker-compose build $MODE
docker-compose run --rm $MODE

# Cleanup on exit
echo "Cleaning up..."
docker-compose down
