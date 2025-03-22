#!/bin/bash
set -e

# Source ROS installation
source /opt/ros/noetic/setup.bash

# If workspace isn't built yet, build it
if [ ! -f "/ros_ws/devel/setup.bash" ]; then
    echo "Workspace not built, building now..."
    cd /ros_ws
    
    # Clean up any previous build artifacts
    rm -rf build/ devel/ install/ .catkin_workspace
    
    # Create the workspace and build
    mkdir -p src
    catkin_make
    echo "Workspace built successfully!"
fi

# Source the workspace setup file
source /ros_ws/devel/setup.bash || echo "Warning: Could not source workspace"

# Execute the command passed to the docker run
exec "$@" 