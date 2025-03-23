#!/bin/bash

echo "=============================="
echo "   Testing PuppyPi Virtual Joystick"
echo "=============================="
echo ""

# Allow X server connections
xhost +local:

# Check if puppy_joystick directory exists
if [ ! -d "puppy_joystick" ]; then
  echo "Error: puppy_joystick directory not found!"
  echo "Make sure you're running this script from the robodog directory."
  exit 1
fi

echo "Starting the Docker container with virtual joystick..."
docker run --rm -it \
  --network=host \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  -v $(pwd)/puppy_joystick:/ros_ws/src/puppy_joystick \
  -v $(pwd)/puppy_description:/ros_ws/src/puppy_description \
  --privileged \
  docker-dev bash -c "
    cd /ros_ws
    source /opt/ros/noetic/setup.bash
    
    echo 'Building ROS workspace...'
    catkin config --extend /opt/ros/noetic
    catkin build
    
    source /ros_ws/devel/setup.bash
    
    # Make scripts executable
    chmod +x /ros_ws/src/puppy_joystick/scripts/*.py
    
    # Kill any existing processes
    pkill -9 -f virtual_joystick.py 2>/dev/null || true
    
    echo ''
    echo 'VIRTUAL JOYSTICK CONTROLS:'
    echo '  - ▲ Button or drag up: Walk Forward'
    echo '  - ▼ Button or drag down: Walk Backward'
    echo '  - ◄ Button or drag left: Rotate Left'
    echo '  - ► Button or drag right: Rotate Right'
    echo '  - ■ Button (center): Stop all movements'
    echo '  - Virtual Joystick: Drag for continuous directional control'
    echo ''
    
    # Start ROS core in the background
    roscore &
    sleep 5
    
    # Start the virtual joystick
    echo 'Starting virtual joystick...'
    rosrun puppy_joystick virtual_joystick.py
"

# Reset X server permissions
xhost -local:
echo "Test completed." 