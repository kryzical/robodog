#!/bin/bash

echo "=============================="
echo "   PuppyPi Gazebo Test"
echo "=============================="
echo ""

# Function to check if a command exists
check_command() {
    if ! command -v $1 &> /dev/null; then
        echo "Error: $1 is not installed"
        exit 1
    fi
}

# Check for required commands
check_command "docker"
check_command "xhost"

# Get the Windows host IP address
WINDOWS_IP=$(ip route | grep default | awk '{print $3}')
echo "Windows host IP: $WINDOWS_IP"

# Set up display for WSL
export DISPLAY=$WINDOWS_IP:0.0
echo "Using DISPLAY: $DISPLAY"

# Allow X server connections
xhost + > /dev/null

echo "Starting the Docker container..."
docker run --rm -it \
  --net=host \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -v $(pwd)/puppy_description:/ros_ws/src/puppy_description \
  --privileged \
  puppypi-dev bash -c "
    cd /ros_ws
    source /opt/ros/noetic/setup.bash
    
    echo 'Building ROS workspace...'
    catkin config --extend /opt/ros/noetic
    catkin build
    
    source devel/setup.bash
    
    echo 'Starting Gazebo simulation...'
    roslaunch puppy_description gazebo.launch
"

# Reset X server permissions
xhost - > /dev/null

echo "Simulation terminated." 