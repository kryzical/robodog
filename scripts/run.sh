#!/bin/bash

# Script to run Gazebo Garden

# Stop any existing containers
echo "Stopping existing containers..."
docker-compose -f docker-compose-gazebo-full.yml down
docker rm -f gazebo_garden 2>/dev/null || true

# Create .docker.xauth if it doesn't exist
if [ ! -f /tmp/.docker.xauth ]; then
  echo "Creating .docker.xauth file..."
  touch /tmp/.docker.xauth
  xauth nlist $DISPLAY | sed -e 's/^..../ffff/' | xauth -f /tmp/.docker.xauth nmerge -
fi

# Set X11 permissions
echo "Setting X11 permissions..."
xhost +local:docker

# Build and start the container
echo "Building Gazebo Garden container..."
docker-compose -f docker-compose-gazebo-full.yml build

echo "Starting Gazebo Garden container..."
docker-compose -f docker-compose-gazebo-full.yml up -d

# Wait for the container to initialize
sleep 3

echo "Container is ready. To start Gazebo, run:"
echo "docker exec -it gazebo_garden bash -c \"source /opt/ros/humble/setup.bash && gz sim -r empty.sdf\""
echo ""
echo "To launch the robot model, run:"
echo "./scripts/launch_robot.sh"
echo ""
echo "To access the container shell, run:"
echo "docker exec -it gazebo_garden bash" 