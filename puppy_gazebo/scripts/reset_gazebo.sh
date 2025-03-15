#!/bin/bash
# Script to reset Gazebo and clean up any existing models

echo "Cleaning up Gazebo..."

# Try to reset simulation first
rostopic pub -1 /gazebo/reset_world std_msgs/Empty '{}' 2>/dev/null || true
echo "Reset world message sent"

# Then try to kill any existing Gazebo processes
pkill -f gzserver || true
pkill -f gzclient || true
echo "Killed any existing Gazebo processes"

# Wait a moment for processes to be fully terminated
sleep 2

# Start Gazebo fresh
echo "Starting Gazebo with new instance..."
roslaunch puppy_gazebo gazebo_fixed.launch 