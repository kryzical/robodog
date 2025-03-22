#!/bin/bash

# Script to launch the robot with Gazebo through Docker

echo "Starting robot simulation with X11 forwarding..."

# Allow X server connections from Docker
xhost +local:docker

# Kill any existing docker containers
echo "Stopping any existing Docker containers..."
docker-compose -f docker/docker-compose.yml down

# Run the Docker container with X11 forwarding
echo "Launching Docker container with Gazebo and robot..."
docker-compose -f docker/docker-compose.yml run --rm \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  dev \
  /bin/bash -c "cd /ros_ws && source devel/setup.bash && /ros_ws/src/puppy_description/scripts/run_simple_walker.sh"

# Reset X server permissions
xhost -local:docker
