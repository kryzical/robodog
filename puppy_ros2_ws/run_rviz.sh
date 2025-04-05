#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Stop and remove any existing container
docker stop puppy_rviz 2>/dev/null || true
docker rm puppy_rviz 2>/dev/null || true

# Allow X server connection
xhost + local:docker || true

# Build the Docker image if it doesn't exist
if ! docker images | grep -q puppy_ros2_gazebo; then
  echo "Building Docker image..."
  docker build -t puppy_ros2_gazebo "$SCRIPT_DIR"
fi

# Run the container
echo "Running RViz with the puppy robot..."
docker run --rm -it \
  --name puppy_rviz \
  --net=host \
  -e DISPLAY=$DISPLAY \
  -e QT_X11_NO_MITSHM=1 \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  -v "${HOME}/.Xauthority:/root/.Xauthority:ro" \
  puppy_ros2_gazebo \
  ros2 launch puppy_description display.launch.py

echo "Container exited." 