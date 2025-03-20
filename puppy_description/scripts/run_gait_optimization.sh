#!/bin/bash

# Script to run gait optimization with proper setup and cleanup
# Usage: ./run_gait_optimization.sh

echo "Starting Gait Optimization Process"

# Check if ROS is sourced
if ! command -v roscore &> /dev/null; then
    echo "ROS environment not detected. Sourcing setup files..."
    source /opt/ros/noetic/setup.bash
    source /ros_ws/devel/setup.bash
fi

# Create results directory if it doesn't exist
RESULTS_DIR="../results"
mkdir -p $RESULTS_DIR

# Function to clean up processes
cleanup() {
    echo "Cleaning up processes..."
    pkill -f "gzserver|gzclient|rosmaster|python.*gait_optimizer" || true
    sleep 2
    echo "Cleanup complete"
}

# Trap Ctrl+C to ensure proper cleanup
trap cleanup INT TERM

# Ensure clean state
cleanup

# Start ROS core
echo "Starting ROS master..."
roscore &
ROSMASTER_PID=$!
sleep 3

# Start Gazebo
echo "Starting Gazebo simulation..."
roslaunch puppy_description gazebo.launch &
GAZEBO_PID=$!
sleep 10  # Wait for Gazebo to fully initialize

# Check if Gazebo launched successfully
if ! pgrep gzserver > /dev/null; then
    echo "ERROR: Gazebo failed to start properly"
    cleanup
    exit 1
fi

echo "Running gait optimization..."
python3 gait_optimizer.py

# Get the exit status
EXIT_STATUS=$?

# Cleanup
cleanup

if [ $EXIT_STATUS -eq 0 ]; then
    echo "Gait optimization completed successfully"
    echo "Results saved in $RESULTS_DIR"
else
    echo "Gait optimization failed with exit code $EXIT_STATUS"
fi

exit $EXIT_STATUS 