#!/bin/bash

# Script to launch the PuppyPi robot simulation with multiple options
# Usage: ./run_robot.sh [simulation|dev|rviz|help]

# Function to display help
show_help() {
  echo "PuppyPi Robot Simulation Launcher"
  echo ""
  echo "Usage: ./run_robot.sh [MODE]"
  echo ""
  echo "Modes:"
  echo "  simulation  - Launch Gazebo simulation with controllers (default)"
  echo "  dev         - Launch interactive development environment"
  echo "  rviz        - Launch RViz visualization only"
  echo "  help        - Display this help message"
  echo ""
  echo "Examples:"
  echo "  ./run_robot.sh           # Launch default simulation"
  echo "  ./run_robot.sh dev       # Launch development environment"
  echo "  ./run_robot.sh rviz      # Launch RViz visualization"
  exit 0
}

# Check for help
if [[ "$1" == "help" || "$1" == "--help" || "$1" == "-h" ]]; then
  show_help
fi

# Default mode
MODE=${1:-simulation}

# Check for valid mode
if [[ "$MODE" != "simulation" && "$MODE" != "dev" && "$MODE" != "rviz" ]]; then
  echo "Error: Invalid mode. Choose from: simulation, dev, rviz"
  echo "For help, use: ./run_robot.sh help"
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
