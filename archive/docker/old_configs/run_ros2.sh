#!/bin/bash

# Set default values
IMAGE_NAME="puppy_ros2:humble"
CMD=""
COMPONENT=""

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    -b|--build)
      CMD="build"
      shift
      ;;
    -r|--run)
      CMD="run"
      shift
      ;;
    -c|--clean)
      CMD="clean"
      shift
      ;;
    --camera)
      COMPONENT="camera"
      shift
      ;;
    --controller)
      COMPONENT="controller"
      shift
      ;;
    --gazebo)
      COMPONENT="gazebo"
      shift
      ;;
    --rviz)
      COMPONENT="rviz"
      shift
      ;;
    -h|--help)
      echo "Usage: $0 [OPTIONS]"
      echo "Options:"
      echo "  -b, --build        Build the Docker image"
      echo "  -r, --run          Run the Docker container with interactive shell"
      echo "  -c, --clean        Clean Docker images and containers"
      echo "  --camera           Run the camera node"
      echo "  --controller       Run the controller node"
      echo "  --gazebo           Run Gazebo simulation"
      echo "  --rviz             Run RViz visualization"
      echo "  -h, --help         Display this help message"
      exit 0
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

# If no command specified, show help
if [ -z "$CMD" ]; then
  $0 --help
  exit 1
fi

# Set project root directory (parent of docker directory)
PROJECT_ROOT="$(dirname "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)")"
cd "${PROJECT_ROOT}"

# Clean before building to save space
if [ "$CMD" = "build" ]; then
  echo "Cleaning up Docker space before building..."
  bash docker/scripts/clean_docker.sh
  
  echo "Building Docker image: $IMAGE_NAME"
  DOCKER_BUILDKIT=1 docker build \
    --progress=plain \
    --network=host \
    --no-cache \
    --force-rm \
    -f .Dockerfile/humble/Dockerfile \
    -t $IMAGE_NAME .
    
  # Clean intermediate images after build
  docker image prune -f
fi

# Run the Docker container
if [ "$CMD" = "run" ]; then
  # If component specified, set the command
  if [ "$COMPONENT" = "camera" ]; then
    echo "Running camera node"
    docker run -it --rm --privileged --network=host \
      -v /dev/video0:/dev/video0 \
      -v /dev/vchiq:/dev/vchiq \
      -v $(pwd):/ros_ws/src \
      -e DISPLAY=$DISPLAY \
      -v /tmp/.X11-unix:/tmp/.X11-unix \
      $IMAGE_NAME bash -c "
        cd /ros_ws && \
        source /opt/ros/humble/setup.bash && \
        source /ros_ws/install/setup.bash && \
        ros2 run puppy_camera camera_publisher.py
      "
  elif [ "$COMPONENT" = "controller" ]; then
    echo "Running controller node"
    docker run -it --rm --privileged --network=host \
      -v /dev/ttyAMA0:/dev/ttyAMA0 \
      -v $(pwd):/ros_ws/src \
      -e DISPLAY=$DISPLAY \
      -v /tmp/.X11-unix:/tmp/.X11-unix \
      $IMAGE_NAME bash -c "
        cd /ros_ws && \
        source /opt/ros/humble/setup.bash && \
        source /ros_ws/install/setup.bash && \
        ros2 launch puppypi_control controller.launch.py
      "
  elif [ "$COMPONENT" = "gazebo" ]; then
    echo "Running Gazebo simulation"
    docker run -it --rm --privileged --network=host \
      -v $(pwd):/ros_ws/src \
      -e DISPLAY=$DISPLAY \
      -v /tmp/.X11-unix:/tmp/.X11-unix \
      $IMAGE_NAME bash -c "
        cd /ros_ws && \
        source /opt/ros/humble/setup.bash && \
        source /ros_ws/install/setup.bash && \
        ros2 launch puppy_gazebo robot.launch.py
      "
  elif [ "$COMPONENT" = "rviz" ]; then
    echo "Running RViz visualization"
    docker run -it --rm --privileged --network=host \
      -v $(pwd):/ros_ws/src \
      -e DISPLAY=$DISPLAY \
      -v /tmp/.X11-unix:/tmp/.X11-unix \
      $IMAGE_NAME bash -c "
        cd /ros_ws && \
        source /opt/ros/humble/setup.bash && \
        source /ros_ws/install/setup.bash && \
        ros2 run rviz2 rviz2
      "
  else
    echo "Running Docker container with interactive shell"
    docker run -it --rm --privileged --network=host \
      -v /dev/video0:/dev/video0 \
      -v /dev/vchiq:/dev/vchiq \
      -v /dev/ttyAMA0:/dev/ttyAMA0 \
      -v $(pwd):/ros_ws/src \
      -e DISPLAY=$DISPLAY \
      -v /tmp/.X11-unix:/tmp/.X11-unix \
      $IMAGE_NAME bash
  fi
fi

# Clean Docker
if [ "$CMD" = "clean" ]; then
  echo "Cleaning Docker space..."
  bash docker/scripts/clean_docker.sh
fi 