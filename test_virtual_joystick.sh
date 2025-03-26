#!/bin/bash

echo "=============================="
echo "   PuppyPi Virtual Joystick Test"
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

# Set up display for WSL
export DISPLAY=:0
echo "Using DISPLAY: $DISPLAY"

# Allow X server connections
xhost +local:

echo "Starting the Docker container..."
docker run --rm -it \
  --net=host \
  -e DISPLAY=:0 \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -v $(pwd)/puppy_joystick:/ros_ws/src/puppy_joystick \
  -v $(pwd)/puppy_description:/ros_ws/src/puppy_description \
  --privileged \
  puppypi-dev bash -c "
    cd /ros_ws
    source /opt/ros/noetic/setup.bash
    
    echo 'Building ROS workspace...'
    catkin config --extend /opt/ros/noetic
    catkin build
    
    source devel/setup.bash
    
    # Make scripts executable
    chmod +x /ros_ws/src/puppy_joystick/scripts/*.py
    chmod +x /ros_ws/src/puppy_description/scripts/velocity_walker.py
    chmod +x /ros_ws/src/puppy_description/scripts/movements/*.py
    
    echo 'Starting Gazebo simulation with virtual joystick control...'
    echo 'CONTROLS:'
    echo '  - ▲ Button or drag up: Walk Forward'
    echo '  - ▼ Button or drag down: Walk Backward'
    echo '  - ◄ Button or drag left: Rotate Left'
    echo '  - ► Button or drag right: Rotate Right'
    echo '  - ■ Button (center): Stop all movements'
    echo '  - Virtual Joystick: Drag for continuous directional control'
    echo ''
    
    # Launch everything using the combined launch file
    roslaunch puppy_joystick gazebo_with_joystick.launch
"

# Reset X server permissions
xhost -local:

echo "Test terminated." 