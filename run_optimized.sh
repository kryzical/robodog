#!/bin/bash

# Script to run the optimized Docker Compose setup for Puppy Robot

# Make script executable
chmod +x build_optimized.sh

# Set paths
PROJECT_ROOT="/home/avengers/robodog"
COMPOSE_FILE="${PROJECT_ROOT}/docker/compose/docker-compose.optimized.yml"

# Check if optimized Docker image exists
if [[ "$(docker images -q puppy_robot_optimized:humble 2> /dev/null)" == "" ]]; then
  echo "Optimized Docker image not found. Building it now..."
  ./build_optimized.sh
fi

# Parse command line arguments
SERVICE=""
ACTION="up"
DETACHED=false
BUILD=false

show_help() {
  echo "Usage: $0 [options] [down|ps|logs|restart]"
  echo "Options:"
  echo "  -h, --help        Show this help message"
  echo "  -b, --build       (Re)build the Docker image"
  echo "  -s, --service     Service to run (e.g., camera_node, controller, gazebo, rviz, dev)"
  echo "  -d, --detached    Run in detached mode"
  echo "Examples:"
  echo "  $0 -s controller   # Run the controller service"
  echo "  $0 -s dev          # Run an interactive development shell"
  echo "  $0 down            # Stop all services"
  exit 0
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help)
      show_help
      ;;
    -b|--build)
      BUILD=true
      shift
      ;;
    -s|--service)
      SERVICE="$2"
      shift 2
      ;;
    -d|--detached)
      DETACHED=true
      shift
      ;;
    down|ps|logs|restart)
      ACTION="$1"
      shift
      ;;
    *)
      echo "Unknown option: $1"
      show_help
      ;;
  esac
done

# Build the image if requested
if [ "$BUILD" = true ]; then
  echo "Building optimized Docker image..."
  ./build_optimized.sh
fi

# Set up the compose command
COMPOSE_CMD="docker-compose -f \"${COMPOSE_FILE}\""

# Handle different actions
if [ "$ACTION" = "up" ]; then
  COMPOSE_CMD="docker-compose -f \"${COMPOSE_FILE}\" up"
  
  # Add detached flag if requested
  if [ "$DETACHED" = true ]; then
    COMPOSE_CMD="$COMPOSE_CMD -d"
  fi
  
  # Add service if specified
  if [ -n "$SERVICE" ]; then
    COMPOSE_CMD="$COMPOSE_CMD $SERVICE"
  fi
else
  COMPOSE_CMD="docker-compose -f \"${COMPOSE_FILE}\" $ACTION"
fi

# Execute the command
echo "Executing: $COMPOSE_CMD"
eval $COMPOSE_CMD 