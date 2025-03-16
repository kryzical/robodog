#!/bin/bash

# Script to run ROS 2 Humble with Gazebo

# Set workspace folder and image name
WORKSPACE="robodog_ws"
IMAGE_NAME="ros:humble"
MODE="interactive"

# Make sure workspace directory exists
mkdir -p $HOME/$WORKSPACE

# Set up X11 forwarding
echo "Setting up X11 for GUI applications..."
xhost +local:docker || true

# Set DISPLAY if not already set
if [ -z "$DISPLAY" ]; then
  export DISPLAY=:0
  echo "DISPLAY environment variable was not set. Using default: $DISPLAY"
fi

echo "Starting container in $MODE mode..."

# Run the container
docker run -it --rm \
  --name "robodog_gazebo" \
  --net=host \
  --privileged \
  --env="DISPLAY=$DISPLAY" \
  --env="QT_X11_NO_MITSHM=1" \
  --volume="/etc/timezone:/etc/timezone:ro" \
  --volume="/etc/localtime:/etc/localtime:ro" \
  --volume="$HOME/$WORKSPACE:/root/$WORKSPACE:rw" \
  --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
  $IMAGE_NAME \
  bash

# Reset X11 permissions
xhost -local:docker || true
