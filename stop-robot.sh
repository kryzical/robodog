#!/bin/bash

# Script to stop the robot simulation

echo "Stopping robot simulation..."
cd docker

# Try Docker Compose shutdown first
docker compose down

# If the container is still running, stop it directly
if docker ps | grep -q "gazebo_robot"; then
  echo "Container gazebo_robot still running, stopping directly..."
  docker stop gazebo_robot
  docker rm gazebo_robot
fi

echo "Cleaning up any other containers..."
docker stop $(docker ps -aq) 2>/dev/null || true
docker rm $(docker ps -aq) 2>/dev/null || true

echo "Cleanup complete!" 