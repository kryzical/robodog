#!/bin/bash

# Script to build the OSRF-based simulation Docker image

# Set image name and tag
IMAGE_NAME="puppy_robot_osrf"
TAG="humble"

# Enable BuildKit for parallel building
export DOCKER_BUILDKIT=1

echo "Building OSRF-based simulation Docker image: ${IMAGE_NAME}:${TAG}"
echo "This will take a while but will have full ROS 2 and Gazebo support..."

# Run the build with parallel processing and force pull from source
docker build \
  --progress=plain \
  --pull \
  --no-cache \
  --network=host \
  --tag "${IMAGE_NAME}:${TAG}" \
  --file .Dockerfile/humble/Dockerfile.osrf \
  .

# Check if build was successful
if [ $? -eq 0 ]; then
  echo "Build successful!"
  echo "You can now run the simulation with:"
  echo "  ./run_osrf.sh"
else
  echo "Build failed. Please check the error messages above."
fi 