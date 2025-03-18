#!/bin/bash

# Allow X11 connections
xhost +local:docker

# Navigate to the puppy_description directory
cd /home/brian/ros1_test/puppy_testing/ros1_puppy_ws/src/puppy_description

# Build and run the container
docker-compose build
docker-compose up -d

# Enter the container
docker-compose exec puppy_ros bash -c '
# Source the ROS setup files
source /opt/ros/noetic/setup.bash

# Navigate to the root of the workspace
cd /ros_ws

# Remove existing build and devel directories
rm -rf build devel

# Build the workspace
catkin_make

# Source the workspace setup file
source devel/setup.bash

# Run the simulation
roslaunch puppy_description gazebo.launch
'