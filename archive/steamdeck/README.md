# RoboDog Project - Steam Deck Control Station

This directory contains files for setting up the ROS 2 Humble environment on a Steam Deck to control the RoboDog.

## Architecture

Our approach is:
1. Use the Steam Deck (x86_64 architecture) as the main control station/computer
2. Run ROS 2 Humble with Gazebo simulation on the Steam Deck
3. Run lightweight ROS 2 nodes on the robot itself
4. Communicate between Steam Deck and robot via ROS 2 topics over WiFi/network

## Setup Instructions

1. Install Docker on the Steam Deck
2. Use the consolidated Docker setup from the root project:
   ```
   cd /path/to/robodog
   ./run_humble.sh --gazebo  # To run with Gazebo
   ./run_humble.sh --rviz    # To run with RViz
   ./run_humble.sh           # To run interactive shell
   ```

## Unified Docker Setup

We've created a unified Docker setup in `docker/Dockerfile.ros2` and `docker/run_ros2_humble.sh` that should be used instead of the files in this directory. The files here remain for reference purposes only.

## Included Files

- `Dockerfile`: Defines the ROS 2 Humble environment with Gazebo and other tools
- `run_gazebo.sh`: Script to launch the Docker container with proper settings

## Next Steps

1. Develop the robot's lightweight ROS 2 nodes for communication
2. Create robot description (URDF) files for simulation in Gazebo
3. Develop control interfaces for Steam Deck
4. Test communication between Steam Deck and robot 