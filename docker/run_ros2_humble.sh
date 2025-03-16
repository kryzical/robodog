#!/bin/bash

# Script to run ROS 2 Humble with Gazebo

# Set workspace folder and image name
WORKSPACE="robodog_ws"
IMAGE_NAME="robodog:humble"

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

# Make sure workspace directory exists
mkdir -p $HOME/$WORKSPACE

# Check if the image exists
if [[ "$(docker images -q ${IMAGE_NAME} 2> /dev/null)" == "" ]]; then
  echo "Image ${IMAGE_NAME} not found. Building it first..."
  docker build -t ${IMAGE_NAME} -f $(dirname "$0")/Dockerfile.ros2 .
  if [ $? -ne 0 ]; then
    echo "Build failed. Exiting."
    exit 1
  fi
fi

# Set up X11 forwarding
echo "Setting up X11 for GUI applications..."
xhost +local:docker || true

# Set DISPLAY if not already set
if [ -z "$DISPLAY" ]; then
  export DISPLAY=:0
  echo "DISPLAY environment variable was not set. Using default: $DISPLAY"
fi

# Setup the command based on mode
case "$MODE" in
  "interactive")
    CMD="bash"
    ;;
  "gazebo")
    CMD="bash -c 'source /opt/ros/humble/setup.bash && ros2 launch gazebo_ros gazebo.launch.py'"
    ;;
  "rviz")
    CMD="bash -c 'source /opt/ros/humble/setup.bash && rviz2'"
    ;;
  "build")
    CMD="bash -c 'source /opt/ros/humble/setup.bash && cd /root/$WORKSPACE && colcon build --symlink-install'"
    ;;
esac

echo "Starting container in $MODE mode..."

# Run the container
docker run -it --rm \
  --name "robodog_ros2" \
  --network=host \
  --privileged \
  --env="DISPLAY=$DISPLAY" \
  --env="QT_X11_NO_MITSHM=1" \
  --volume="/etc/timezone:/etc/timezone:ro" \
  --volume="/etc/localtime:/etc/localtime:ro" \
  --volume="$HOME/$WORKSPACE:/root/$WORKSPACE:rw" \
  --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
  $IMAGE_NAME \
  $CMD

# Reset X11 permissions
xhost -local:docker || true 