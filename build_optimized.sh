#!/bin/bash

# Script to build the optimized Docker image with parallel build capability

# Set image name and tag
IMAGE_NAME="puppy_robot_optimized"
TAG="humble"

# Enable BuildKit for better build performance
export DOCKER_BUILDKIT=1

echo "Building optimized Docker image: ${IMAGE_NAME}:${TAG}"
echo "Using multi-stage builds for parallel processing..."

# Run the build with BuildKit enabled
docker build \
  --progress=plain \
  --network=host \
  --tag "${IMAGE_NAME}:${TAG}" \
  --file .Dockerfile/humble/Dockerfile.optimized \
  .

# Check if build was successful
if [ $? -eq 0 ]; then
  echo "Build successful!"
  echo "You can now use the image with:"
  echo "  docker run -it --rm --name ${IMAGE_NAME}_container --network=host ${IMAGE_NAME}:${TAG}"
  echo "Or with docker-compose by updating the image name in docker-compose.yml"
else
  echo "Build failed. Please check the error messages above."
fi 