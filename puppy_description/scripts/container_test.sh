#!/bin/bash

# Exit on any error
set -e

# Setup logging
LOG_DIR="/tmp/ros_logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/test_$(date +%Y%m%d_%H%M%S).log"
exec 1> >(tee -a "$LOG_FILE")
exec 2>&1

echo "Starting container test at $(date)"

# Function to cleanup on exit
cleanup() {
    echo "Cleaning up..."
    # Kill any running ROS/Gazebo processes
    pkill -f "gazebo" || true
    pkill -f "gzserver" || true
    pkill -f "gzclient" || true
    pkill -f "rosmaster" || true
    pkill -f "roscore" || true
    pkill -f "python3" || true
    exit 0
}

# Setup trap for cleanup
trap cleanup SIGINT SIGTERM EXIT

# Source ROS setup
echo "Sourcing ROS setup..."
source /opt/ros/noetic/setup.bash
source /ros_ws/devel/setup.bash

# Test ROS setup
echo "Testing ROS setup..."
rosnode list || { echo "Failed to list ROS nodes"; exit 1; }

# Start Gazebo with our robot
echo "Starting Gazebo simulation..."
timeout 30 roslaunch puppy_description gazebo.launch &
GAZEBO_PID=$!

# Wait for Gazebo to start and load the robot
echo "Waiting for Gazebo to start..."
sleep 15  # Give Gazebo time to load everything

# Check if Gazebo is still running
if ! kill -0 $GAZEBO_PID 2>/dev/null; then
    echo "Gazebo failed to start"
    exit 1
fi

# Unpause Gazebo simulation
echo "Unpausing Gazebo simulation..."
rosservice call /gazebo/unpause_physics "{}" || {
    echo "Failed to unpause Gazebo"
    exit 1
}

# Test movement script with timeout
echo "Testing movement script..."
timeout 30 python3 /ros_ws/src/puppy_description/scripts/movement_test.py || {
    echo "Movement test failed"
    exit 1
}

echo "All tests completed successfully!"
exit 0 