# Docker Compose for Puppy Robot

This directory contains Docker Compose configuration for running the Puppy Robot ROS 2 system.

## Files

- `docker-compose.yml` - The main Docker Compose configuration for ROS 2 (Humble)
- `docker-compose-ros1-deprecated.yml` - Deprecated ROS 1 (Noetic) configuration (kept for reference)

## Usage

The recommended way to use Docker Compose is through the `run_docker_compose.sh` script:

```bash
# From the project root directory:

# Build and run the controller
./run_compose.sh -b -s controller

# Run the camera node in detached mode
./run_compose.sh -d -s camera_node

# Stop all services
./run_compose.sh down
```

See `./run_compose.sh --help` for more options.

## Available Services

- `ros2_base`: Base container that others extend from
- `camera_node`: Camera publisher node
- `controller`: The main robot controller
- `gazebo`: Gazebo simulation
- `rviz`: RViz visualization
- `dev`: Development shell with ROS 2 environment

## Notes

All services are configured to use:
- Host network mode for easy communication with the host
- GPU acceleration if available
- Access to necessary hardware devices
- Shared X11 display for GUI applications 