#!/bin/bash

# Script to run Gazebo simulation for Puppy Robot

# Set image name
IMAGE_NAME="puppy_robot_simulation"
TAG="humble"
CONTAINER_NAME="puppy_robot_simulation_container"

# Check if image exists
if [[ "$(docker images -q ${IMAGE_NAME}:${TAG} 2> /dev/null)" == "" ]]; then
  echo "Simulation Docker image not found. Building it now..."
  ./build_simulation.sh
fi

# Parse command line arguments
show_help() {
  echo "Usage: $0 [options]"
  echo "Options:"
  echo "  -h, --help        Show this help message"
  echo "  -b, --build       (Re)build the simulation image"
  echo "  -i, --interactive Enter container in interactive mode"
  echo "  -g, --gazebo      Run Gazebo simulation"
  echo "  -r, --rviz        Run RViz visualization"
  exit 0
}

MODE="interactive"

while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help)
      show_help
      ;;
    -b|--build)
      echo "Building simulation image..."
      ./build_simulation.sh
      exit 0
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
    *)
      echo "Unknown option: $1"
      show_help
      ;;
  esac
done

# Set up X11 forwarding
echo "Setting up X11 for GUI applications..."
xhost +local:docker || true

# Run container based on selected mode
case "$MODE" in
  "interactive")
    echo "Starting interactive container..."
    docker run -it --rm \
      --name $CONTAINER_NAME \
      --network=host \
      --privileged \
      -e DISPLAY=$DISPLAY \
      -v /tmp/.X11-unix:/tmp/.X11-unix \
      -v /home/avengers/robodog:/ros_ws \
      ${IMAGE_NAME}:${TAG}
    ;;
  "gazebo")
    echo "Starting container and launching Gazebo simulation..."
    docker run -it --rm \
      --name $CONTAINER_NAME \
      --network=host \
      --privileged \
      -e DISPLAY=$DISPLAY \
      -v /tmp/.X11-unix:/tmp/.X11-unix \
      -v /home/avengers/robodog:/ros_ws \
      ${IMAGE_NAME}:${TAG} \
      bash -c "source /opt/ros/humble/setup.bash && cd /ros_ws && colcon build --symlink-install --packages-select puppy_description puppy_gazebo && source /ros_ws/install/setup.bash && ros2 launch puppy_gazebo robot.launch.py"
    ;;
  "rviz")
    echo "Starting container and launching RViz..."
    docker run -it --rm \
      --name $CONTAINER_NAME \
      --network=host \
      --privileged \
      -e DISPLAY=$DISPLAY \
      -v /tmp/.X11-unix:/tmp/.X11-unix \
      -v /home/avengers/robodog:/ros_ws \
      ${IMAGE_NAME}:${TAG} \
      bash -c "source /opt/ros/humble/setup.bash && ros2 run rviz2 rviz2"
    ;;
esac

# Reset X11 permissions
xhost -local:docker || true 