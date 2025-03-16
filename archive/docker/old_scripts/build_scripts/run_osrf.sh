#!/bin/bash

# Script to run the OSRF-based simulation Docker container

# Set image name and tag
IMAGE_NAME="puppy_robot_osrf"
TAG="humble"
CONTAINER_NAME="puppy_robot_sim"

# Check if the image exists
if [[ "$(docker images -q ${IMAGE_NAME}:${TAG} 2> /dev/null)" == "" ]]; then
  echo "Image ${IMAGE_NAME}:${TAG} not found. Building it first..."
  ./build_osrf.sh
  if [ $? -ne 0 ]; then
    echo "Build failed. Exiting."
    exit 1
  fi
fi

# Parse command line arguments
MODE="interactive"
show_help() {
  echo "Usage: $0 [options]"
  echo "Options:"
  echo "  -h, --help        Show this help message"
  echo "  -i, --interactive Enter container interactively (default)"
  echo "  -g, --gazebo      Launch Gazebo"
  echo "  -r, --rviz        Launch RViz"
  echo "  -b, --build       Build ROS workspace"
  exit 0
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help)
      show_help
      ;;
    -i|--interactive)
      MODE="interactive"
      shift
      ;;
    -g|--gazebo)
      MODE="gazebo"
      shift
      ;;
    -r|--rviz)
      MODE="rviz"
      shift
      ;;
    -b|--build)
      MODE="build"
      shift
      ;;
    *)
      echo "Unknown option: $1"
      show_help
      ;;
  esac
done

# Set up X11 forwarding
echo "Setting up X11 for GUI applications..."
xhost +local:docker || true

# Setup the command based on mode
case "$MODE" in
  "interactive")
    CMD="bash"
    ;;
  "gazebo")
    CMD="bash -c 'source /opt/ros/humble/setup.bash && source /usr/share/gazebo/setup.sh && gazebo'"
    ;;
  "rviz")
    CMD="bash -c 'source /opt/ros/humble/setup.bash && ros2 run rviz2 rviz2'"
    ;;
  "build")
    CMD="bash -c 'source /opt/ros/humble/setup.bash && cd /ros_ws && colcon build --symlink-install'"
    ;;
esac

# Run the container
echo "Starting container in $MODE mode..."
docker run -it --rm \
  --name $CONTAINER_NAME \
  --network=host \
  --privileged \
  --env="DISPLAY=$DISPLAY" \
  --env="QT_X11_NO_MITSHM=1" \
  --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
  --volume="/home/avengers/robodog:/ros_ws:rw" \
  ${IMAGE_NAME}:${TAG} \
  $CMD

# Reset X11 permissions
xhost -local:docker || true 