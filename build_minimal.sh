#!/bin/bash

# Script to build a minimal Docker image for Gazebo testing

# Set image name and tag
IMAGE_NAME="puppy_robot_minimal"
TAG="humble"

# Clean up Docker to free space
echo "Cleaning up Docker to free space..."
docker system prune -f

# Check available space
echo "Available disk space:"
df -h /

echo "Building minimal simulation Docker image: ${IMAGE_NAME}:${TAG}"
echo "Using smaller ros-base image to save space..."

# Build the image
docker build \
  --pull \
  --no-cache \
  --network=host \
  --tag "${IMAGE_NAME}:${TAG}" \
  --file .Dockerfile/humble/Dockerfile.minimal \
  .

# Check if build was successful
if [ $? -eq 0 ]; then
  echo "Build successful!"
  echo "You can now run the simulation with:"
  echo "  ./run_minimal.sh"
else
  echo "Build failed. Please check the error messages above."
fi 