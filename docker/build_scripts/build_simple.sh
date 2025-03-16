#!/bin/bash

# Simple build script for Gazebo simulation container

# Set image name and tag
IMAGE_NAME="puppy_robot_simple"
TAG="humble"

echo "Building simple simulation Docker image: ${IMAGE_NAME}:${TAG}"

# Run the build (pulling from source)
docker build \
  --pull \
  --no-cache \
  --network=host \
  --tag "${IMAGE_NAME}:${TAG}" \
  --file .Dockerfile/humble/Dockerfile.simple \
  .

# Check if build was successful
if [ $? -eq 0 ]; then
  echo "Build successful!"
  echo "You can now use the image with:"
  echo "  docker run -it --rm --name ${IMAGE_NAME}_container --network=host -e DISPLAY=\$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -v /home/avengers/robodog:/ros_ws ${IMAGE_NAME}:${TAG}"
  echo ""
  echo "To run Gazebo:"
  echo "  ros2 run gazebo_ros gazebo"
else
  echo "Build failed. Please check the error messages above."
fi 