#!/bin/bash

# Script to build a simulation-focused Docker image - WITH PARALLEL BUILDS AND SOURCE PULLS

# Set image name and tag
IMAGE_NAME="puppy_robot_simulation"
TAG="humble"

# Enable BuildKit for parallel building
export DOCKER_BUILDKIT=1

echo "Building simulation Docker image: ${IMAGE_NAME}:${TAG}"
echo "Ensuring parallel builds and pulling from source..."

# Run the build with parallel processing and force pull from source
docker build \
  --progress=plain \
  --pull \
  --no-cache \
  --network=host \
  --tag "${IMAGE_NAME}:${TAG}" \
  --file .Dockerfile/humble/Dockerfile.simulation \
  .

# Check if build was successful
if [ $? -eq 0 ]; then
  echo "Build successful!"
  echo "You can now use the image with:"
  echo "  docker run -it --rm --name ${IMAGE_NAME}_container --network=host -e DISPLAY=\$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -v /home/avengers/robodog:/ros_ws ${IMAGE_NAME}:${TAG}"
  echo ""
  echo "To run Gazebo simulation:"
  echo "  ./run_simulation.sh -g"
else
  echo "Build failed. Please check the error messages above."
fi 