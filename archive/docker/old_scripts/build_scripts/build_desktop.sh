#!/bin/bash

# Script to build a Docker image with ROS 2 Humble Desktop Full

# Set image name and tag
IMAGE_NAME="puppy_robot_desktop"
TAG="humble"

# Clean up Docker to free space
echo "Cleaning up Docker to free space..."
docker system prune -f

# Check available space
echo "Available disk space:"
df -h /

echo "Building ROS 2 Humble Desktop Full Docker image: ${IMAGE_NAME}:${TAG}"
echo "Using pre-built desktop-full image to save on redundant installs..."

# Build the image
docker build \
  --pull \
  --network=host \
  --tag "${IMAGE_NAME}:${TAG}" \
  --file .Dockerfile/humble/Dockerfile.desktop \
  .

# Check if build was successful
if [ $? -eq 0 ]; then
  echo "Build successful!"
  echo "You can now run the desktop environment with:"
  echo "  ./run_desktop.sh"
else
  echo "Build failed. Please check the error messages above."
fi 