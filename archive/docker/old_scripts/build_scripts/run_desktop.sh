#!/bin/bash

# Script to run the ROS 2 Desktop Docker container

# Set image name and tag
IMAGE_NAME="puppy_robot_desktop"
TAG="humble"
CONTAINER_NAME="puppy_desktop"

# Check if the image exists
if [[ "$(docker images -q ${IMAGE_NAME}:${TAG} 2> /dev/null)" == "" ]]; then
  echo "Image ${IMAGE_NAME}:${TAG} not found. Building it first..."
  ./build_desktop.sh
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

# Set DISPLAY if not already set
if [ -z "$DISPLAY" ]; then
  export DISPLAY=:0
  echo "DISPLAY environment variable was not set. Using default: $DISPLAY"
fi

# Set up X11 forwarding
echo "Setting up X11 for GUI applications..."
xhost +local:docker || true

# Run the container based on mode
echo "Starting container in $MODE mode..."

if [ "$MODE" = "interactive" ]; then
  docker run -it --rm \
    --name $CONTAINER_NAME \
    --network=host \
    --privileged \
    --env="DISPLAY=$DISPLAY" \
    --env="QT_X11_NO_MITSHM=1" \
    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
    --volume="/home/avengers/robodog:/ros_ws:rw" \
    ${IMAGE_NAME}:${TAG} \
    bash
elif [ "$MODE" = "gazebo" ]; then
  docker run -it --rm \
    --name $CONTAINER_NAME \
    --network=host \
    --privileged \
    --env="DISPLAY=$DISPLAY" \
    --env="QT_X11_NO_MITSHM=1" \
    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
    --volume="/home/avengers/robodog:/ros_ws:rw" \
    ${IMAGE_NAME}:${TAG} \
    bash -c "source /opt/ros/humble/setup.bash && ros2 launch gazebo_ros gazebo.launch.py"
elif [ "$MODE" = "rviz" ]; then
  docker run -it --rm \
    --name $CONTAINER_NAME \
    --network=host \
    --privileged \
    --env="DISPLAY=$DISPLAY" \
    --env="QT_X11_NO_MITSHM=1" \
    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
    --volume="/home/avengers/robodog:/ros_ws:rw" \
    ${IMAGE_NAME}:${TAG} \
    bash -c "source /opt/ros/humble/setup.bash && rviz2"
elif [ "$MODE" = "build" ]; then
  docker run -it --rm \
    --name $CONTAINER_NAME \
    --network=host \
    --privileged \
    --env="DISPLAY=$DISPLAY" \
    --env="QT_X11_NO_MITSHM=1" \
    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
    --volume="/home/avengers/robodog:/ros_ws:rw" \
    ${IMAGE_NAME}:${TAG} \
    bash -c "source /opt/ros/humble/setup.bash && cd /ros_ws && colcon build --symlink-install"
fi

# Reset X11 permissions
xhost -local:docker || true 