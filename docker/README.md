# Docker Setup for RoboDog

This directory contains the Docker configuration for running ROS 2 Humble with Gazebo for the RoboDog project.

## Files

- `Dockerfile.ros2`: The main Dockerfile that creates a ROS 2 Humble environment with Gazebo and all necessary tools.
- `run_ros2_humble.sh`: A script to build and run the Docker container with various options.

## Quick Start

From the project root directory:

```bash
# Run in interactive mode
./run_humble.sh

# Run with Gazebo
./run_humble.sh --gazebo

# Run with RViz
./run_humble.sh --rviz

# Build the ROS workspace
./run_humble.sh --build
```

## Docker Container Details

The Docker container includes:
- ROS 2 Humble
- Gazebo simulator
- RViz visualization
- ROS 2 development tools
- Cross-architecture support (primarily x86_64 for Steam Deck)

## Steam Deck Architecture

This Docker setup is primarily designed for use on the Steam Deck (x86_64 architecture), which will serve as the main control station for the RoboDog. The lightweight nodes running on the robot itself will communicate with this control station over ROS 2 topics.

## Clean Directory Structure

This directory has been simplified to contain only the essential files needed for the Docker setup. All other Docker-related files that were previously in this directory or in `.Dockerfile/` have been moved to `archive/docker/` for reference. 