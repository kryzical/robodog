#!/bin/bash

# Script to run Docker Compose services for the Puppy Robot project (ROS 2)

# Set project root directory (parent of docker directory)
PROJECT_ROOT="$(dirname "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)")"
PROJECT_ROOT="$(dirname "$PROJECT_ROOT")"
cd "${PROJECT_ROOT}"

# Default values
COMPOSE_FILE="docker/compose/docker-compose.yml"
SERVICE=""
ACTION="up"
DETACHED=false
BUILD=false

# Parse command line arguments
show_help() {
  echo "Usage: $0 [options] [down|ps|logs|restart]"
  echo "Options:"
  echo "  -h, --help        Show this help message"
  echo "  -b, --build       Build the Docker images (default: false)"
  echo "  -s, --service     Service to run (e.g., camera_node, controller, gazebo, rviz, dev)"
  echo "  -d, --detached    Run in detached mode (default: false)"
  echo "  -c, --clean       Clean up before building (runs the clean_docker.sh script)"
  echo "Commands:"
  echo "  down              Stop and remove containers"
  echo "  ps                List running containers"
  echo "  logs              Show container logs"
  echo "  restart           Restart services"
  echo "Examples:"
  echo "  $0 -b -s controller  # Build and run the controller service"
  echo "  $0 -d -s camera_node # Run the camera node in detached mode"
  echo "  $0 down              # Stop all services"
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
    -c|--clean)
      # Run the clean_docker.sh script
      echo "Cleaning Docker environment before building..."
      bash docker/scripts/clean_docker.sh
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

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
  echo "Docker Compose not found. Please install Docker Compose."
  exit 1
fi

# Construct the docker-compose command
COMPOSE_CMD="docker-compose -f $COMPOSE_FILE"

# Add build flag if requested
if [ "$BUILD" = true ]; then
  if [ "$ACTION" = "up" ]; then
    # Enable parallel building by default for better performance
    COMPOSE_CMD="$COMPOSE_CMD build --no-cache --parallel"
    echo "Building Docker images with parallel jobs..."
    eval $COMPOSE_CMD
  fi
fi

# Set the action
if [ "$ACTION" = "up" ]; then
  COMPOSE_CMD="docker-compose -f $COMPOSE_FILE up"
  
  # Add detached flag if requested
  if [ "$DETACHED" = true ]; then
    COMPOSE_CMD="$COMPOSE_CMD -d"
  fi
  
  # Add service if specified
  if [ -n "$SERVICE" ]; then
    COMPOSE_CMD="$COMPOSE_CMD $SERVICE"
  fi
else
  COMPOSE_CMD="docker-compose -f $COMPOSE_FILE $ACTION"
fi

# Execute the command
echo "Executing: $COMPOSE_CMD"
eval $COMPOSE_CMD 