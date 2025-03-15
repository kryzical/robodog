#!/bin/bash
# Script to install missing ROS dependencies that might be causing controller issues

set -e
echo "Installing/updating ROS controller dependencies..."

# Update package lists
apt-get update

# Install controller-related packages
apt-get install -y \
  ros-noetic-controller-manager \
  ros-noetic-joint-state-controller \
  ros-noetic-position-controllers \
  ros-noetic-effort-controllers \
  ros-noetic-velocity-controllers \
  ros-noetic-robot-state-publisher \
  ros-noetic-gazebo-ros-control \
  ros-noetic-joint-state-publisher

# Install additional dependencies
apt-get install -y \
  ros-noetic-control-toolbox \
  ros-noetic-realtime-tools \
  ros-noetic-ros-controllers \
  ros-noetic-ros-control

echo "All dependencies installed successfully!"
echo "Please restart your Docker container to apply changes."

# Optionally rebuild ROS workspace
echo "Rebuilding ROS workspace..."
cd /workspace && catkin_make clean && catkin_make

echo "Done! Please source the workspace: source /workspace/devel/setup.bash" 