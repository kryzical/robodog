# Docker Resources for Puppy Robot

This directory contains Docker-related resources for the Puppy robot project.

## Directory Structure

- `run_ros2.sh`: Main script to build and run ROS 2 Docker containers
- `scripts/`: Utility scripts for Docker operations
  - `clean_docker.sh`: Script for cleaning up Docker resources

## Usage

### Building the ROS 2 Image

```bash
./run_ros2.sh --build
```

This will:
1. Clean up existing Docker resources
2. Build a new Docker image from the Dockerfile
3. Tag it as `puppy_ros2:humble`

### Running Components

#### Interactive Shell

```bash
./run_ros2.sh --run
```

#### Camera Node

```bash
./run_ros2.sh --run --camera
```

#### Controller Node

```bash
./run_ros2.sh --run --controller
```

#### Gazebo Simulation

```bash
./run_ros2.sh --run --gazebo
```

#### RViz Visualization

```bash
./run_ros2.sh --run --rviz
```

### Cleaning Docker Resources

```bash
./run_ros2.sh --clean
```

## Container Configuration

The Docker container:
- Runs with privileged access
- Mounts required devices (/dev/video0, /dev/vchiq, /dev/ttyAMA0)
- Shares the host network
- Mounts X11 for GUI applications
- Maps the project directory to /ros_ws/src 