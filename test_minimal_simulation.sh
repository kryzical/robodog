#!/bin/bash
#
# PuppyPi Minimal Simulation with Joystick Control
#
# This script sets up a minimal PuppyPi robot simulation with joystick control.
# It launches a Docker container with ROS Noetic, Gazebo, and the necessary
# components for controlling the robot via a virtual joystick interface.
#
# The script handles:
# - Setting up the Docker environment with X11 forwarding
# - Building the ROS workspace with the puppy_joystick and puppy_description packages
# - Starting ROS master, the velocity walker, and Gazebo
# - Launching the virtual joystick for robot control
# - Establishing communication between components with monitoring
#
# Usage: ./test_minimal_simulation.sh
#
# Author: PuppyPi Development Team
# License: MIT

echo "=============================="
echo "   PuppyPi Minimal Simulation with Joystick Control"
echo "=============================="
echo ""

# Allow X server connections
xhost +local:

# Check if required directories exist
if [ ! -d "puppy_joystick" ] || [ ! -d "puppy_description" ]; then
  echo "Error: Required directories not found!"
  echo "Make sure you're running this script from the robodog directory."
  exit 1
fi

# Kill any existing docker containers to avoid conflicts
echo "Stopping any existing Docker containers..."
docker ps -q | xargs -r docker stop > /dev/null 2>&1

# Start a Docker container with the minimal simulation
echo "Starting minimal simulation with joystick control..."
docker run --rm -it \
  --name puppypi_minimal \
  --network=host \
  -e DISPLAY=$DISPLAY \
  -e PYTHONUNBUFFERED=1 \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  -v $(pwd)/puppy_joystick:/ros_ws/src/puppy_joystick \
  -v $(pwd)/puppy_description:/ros_ws/src/puppy_description \
  --privileged \
  docker-dev bash -c "
    cd /ros_ws
    source /opt/ros/noetic/setup.bash
    
    echo 'Preparing minimal workspace...'
    mkdir -p src
    cp -r /ros_ws/src/puppy_joystick /ros_ws/src/
    cp -r /ros_ws/src/puppy_description /ros_ws/src/
    
    echo 'Building minimal workspace...'
    catkin_make
    
    source /ros_ws/devel/setup.bash
    
    # Make scripts executable
    chmod +x /ros_ws/src/puppy_description/scripts/velocity_walker.py
    chmod +x /ros_ws/src/puppy_description/scripts/movements/*.py
    chmod +x /ros_ws/src/puppy_joystick/scripts/*.py
    
    # For debugging - make all Python output unbuffered
    export PYTHONUNBUFFERED=1
    
    # Start roscore in the background
    echo 'Starting roscore...'
    roscore &
    ROSCORE_PID=\$!
    sleep 5
    
    # Create a topic for joystick commands
    rostopic pub -r 1 /joy sensor_msgs/Joy '{header: {stamp: now}, axes: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0], buttons: [0, 0, 0, 0, 0, 0, 0, 0]}' --once
    
    # Start the velocity walker first to ensure it's ready
    echo 'Starting velocity walker...'
    roslaunch puppy_description just_walker.launch &
    WALKER_PID=\$!
    
    # Short wait for velocity walker to initialize
    echo 'Waiting for velocity walker to initialize...'
    sleep 5
    
    # Start Gazebo and robot
    echo 'Starting Gazebo with PuppyPi robot...'
    roslaunch puppy_description gazebo.launch delete_model:=false gui:=true &
    GAZEBO_PID=\$!
    
    # Wait for Gazebo to initialize
    echo 'Waiting for Gazebo to initialize...'
    sleep 15
    
    # Start our joystick controller in a separate process
    echo 'Starting joypad controller...'
    rosrun puppy_joystick joypad_controller.py __name:=joypad_controller &
    JOYPAD_PID=\$!
    
    # Start the topic publisher to keep cmd_vel connection active
    echo 'Starting heartbeat publisher...'
    (
      while true; do
        rostopic pub -1 /cmd_vel geometry_msgs/Twist '{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}' > /dev/null 2>&1
        sleep 2
      done
    ) &
    HEARTBEAT_PID=\$!
    
    echo ''
    echo 'JOYSTICK CONTROLS:'
    echo '  - ▲ Button (4) or Left Stick Up: Walk Forward'
    echo '  - ▼ Button (6) or Left Stick Down: Walk Backward'
    echo '  - ◄ Button (7) or Left Stick Left: Rotate Left'
    echo '  - ► Button (5) or Left Stick Right: Rotate Right'
    echo '  - ■ Button (2): Stop all movements'
    echo ''
    
    # Start topic monitor - more compact version
    echo 'Starting topic monitor...'
    (
      while true; do
        echo -e '\n--- CMD_VEL LATEST ---'
        rostopic echo -n 1 /cmd_vel
        sleep 3
      done
    ) &
    MONITOR_PID=\$!
    
    # Start virtual joystick
    echo 'Starting virtual joystick...'
    rosrun puppy_joystick virtual_joystick.py
    
    # Clean up all processes
    echo 'Shutting down...'
    kill \$MONITOR_PID \$HEARTBEAT_PID \$JOYPAD_PID \$GAZEBO_PID \$WALKER_PID \$ROSCORE_PID
  "

# Reset X server permissions
xhost -local:
echo "Minimal simulation terminated." 