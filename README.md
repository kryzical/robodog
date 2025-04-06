# PuppyPi ROS2 Robot Simulation

This repository contains the configuration and launch files for running the PuppyPi robot in a Gazebo simulation environment using Docker.

## Directory Structure

```
├── docker/             # Docker configuration files
│   ├── Dockerfile      # Docker image definition
│   ├── docker-compose.yml # Docker Compose configuration
│   └── cleanup-containers.sh # Script to remove conflicting containers
├── launch/             # Launch scripts used inside the container
│   ├── cleanup.sh      # Script to clean up containers
│   ├── launch-with-robot.sh # Main robot launch script
│   └── run-sim.sh      # Secondary launch script
├── models/             # Model files
├── puppy_ros2_ws/      # ROS2 workspace with robot packages
├── start-robot.sh      # Main script to start the simulation
├── stop-robot.sh       # Script to stop the simulation
└── README.md           # This file
```

## Prerequisites

- Docker
- Docker Compose
- X11 (for GUI display)

## Quick Start

### 1. Starting the Simulation

To start the Gazebo simulation with the robot:

```bash
./start-robot.sh
```

This script will:
- Set the necessary X11 permissions
- Start a Gazebo container
- Launch Gazebo with an empty world
- Attempt to spawn your robot model

### 2. Stopping the Simulation

To stop the simulation and clean up containers:

```bash
./stop-robot.sh
```

## Robot Appearance

The simulation will attempt to load your actual robot model from the ROS workspace. If your model is found, it will be displayed with a white body color.

If your robot model is not found, a simple robot model with the following properties will be used:
- White box for the body
- Red cylinders for the legs

## Advanced Usage

### Manual Docker Compose Commands

If you prefer to use Docker Compose directly:

1. First, set X11 permissions:
   ```bash
   xhost +local:docker
   ```

2. Navigate to the docker directory:
   ```bash
   cd docker
   ```

3. If you're having issues with existing containers, run the cleanup script:
   ```bash
   ./cleanup-containers.sh
   ```

4. Start the simulation:
   ```bash
   docker compose up
   ```

5. To stop (in another terminal):
   ```bash
   cd docker && docker compose down
   ```

### Troubleshooting Container Conflicts

If you see errors like "container name already in use" or "cannot start service", try these steps:

```bash
cd docker
./cleanup-containers.sh
docker compose up
```

This will forcefully stop and remove all Docker containers, resolving any conflicts.

### Modifying the Robot Model

To modify the robot's appearance or properties:

1. Edit the appropriate files in `puppy_ros2_ws/src/puppy_description/urdf/`
2. Rebuild the workspace if necessary: 
   ```bash
   cd puppy_ros2_ws && colcon build
   ```
3. Restart the simulation to see your changes

### Troubleshooting

- **Display Issues**: If Gazebo doesn't appear, make sure X11 permissions are set correctly with `xhost +local:docker`
- **Robot Not Spawning**: Check the Docker logs for error messages
- **Mesh Loading Issues**: Verify mesh paths in your URDF files and check that they are correctly linked in the filesystem

## Development Notes

### Adding New Features

To add new functionality to the robot:
1. Make changes to the robot model in the ROS workspace
2. Test in simulation using the provided scripts
3. Update `launch-with-robot.sh` if you need to modify how the robot is spawned

### Building a New Docker Image

If you need to update the Docker image:

```bash
cd docker
docker build -t docker_gazebo .
``` 