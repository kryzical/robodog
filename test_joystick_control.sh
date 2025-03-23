#!/bin/bash

echo "=============================="
echo "   PuppyPi Robot with Virtual Joystick"
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

# Start a single Docker container with everything
echo "Starting PuppyPi simulation with joystick control..."
docker run --rm -it \
  --name puppypi_joystick_control \
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
    chmod +x /ros_ws/src/puppy_description/scripts/velocity_walker.py
    chmod +x /ros_ws/src/puppy_description/scripts/movements/*.py
    chmod +x /ros_ws/src/puppy_joystick/scripts/*.py
    
    # Start Gazebo with the robot in the background
    echo 'Starting Gazebo...'
    roslaunch puppy_description gazebo.launch &
    GAZEBO_PID=$!
    
    # Wait for Gazebo to initialize
    echo 'Waiting for Gazebo to initialize (20 seconds)...'
    sleep 20
    
    # Check if Gazebo is still running
    if ! ps -p $GAZEBO_PID > /dev/null; then
      echo 'ERROR: Gazebo failed to start or crashed!'
      exit 1
    fi
    
    # Start the velocity walker in the background
    echo 'Starting velocity walker...'
    roslaunch puppy_description just_walker.launch &
    WALKER_PID=$!
    
    # Sleep a bit to let the walker initialize
    sleep 5
    
    # Check if velocity walker is running
    if ! ps -p $WALKER_PID > /dev/null; then
      echo 'ERROR: Velocity walker failed to start or crashed!'
      exit 1
    fi
    
    # Set up a background monitoring process for the topics
    (
      while true; do
        echo '------- TOPIC DIAGNOSTICS -------'
        echo 'Active topics:'
        rostopic list
        echo 'Checking /joy topic message rate:'
        rostopic hz /joy -w 10 &
        JOY_PID=$!
        sleep 2
        kill $JOY_PID 2>/dev/null
        echo 'Checking /cmd_vel topic message rate:'
        rostopic hz /cmd_vel -w 10 &
        CMD_PID=$!
        sleep 2
        kill $CMD_PID 2>/dev/null
        echo '--------------------------------'
        sleep 10
      done
    ) &
    MONITOR_PID=$!
    
    echo ''
    echo 'VIRTUAL JOYSTICK CONTROLS:'
    echo '  - ▲ Button or drag up: Walk Forward'
    echo '  - ▼ Button or drag down: Walk Backward'
    echo '  - ◄ Button or drag left: Rotate Left'
    echo '  - ► Button or drag right: Rotate Right'
    echo '  - ■ Button (center): Stop all movements'
    echo '  - Virtual Joystick: Drag for continuous directional control'
    echo ''
    echo 'DEBUGGING INFO:'
    echo '  - Check if the joystick UI appears and responds to mouse input'
    echo '  - Check if the Gazebo window shows the robot model'
    echo '  - The velocity walker should respond to /cmd_vel messages'
    echo '  - If the robot does not move, check the diagnostic output for topic activity'
    echo ''
    
    # Start the virtual joystick in the foreground
    echo 'Starting virtual joystick and controller...'
    roslaunch puppy_joystick virtual_joystick.launch || {
      echo 'ERROR: Virtual joystick failed to start or crashed!'
      kill $MONITOR_PID 2>/dev/null
      kill $WALKER_PID 2>/dev/null
      kill $GAZEBO_PID 2>/dev/null
      exit 1
    }
    
    # If the joystick exits, kill the monitoring process
    kill $MONITOR_PID 2>/dev/null
  "

# Reset X server permissions
xhost -local:
echo "Simulation terminated." 