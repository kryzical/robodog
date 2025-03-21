# PuppyPi Robot Simulation

This repository contains a ROS1 Noetic setup for simulating the PuppyPi quadruped robot using Docker.

## Prerequisites

- Docker
- Docker Compose
- X11 for GUI applications (for visualization)

## Quick Start

The simulation can be launched with a single command:

```bash
# Launch the default simulation mode
./run_robot.sh
```

## Launch Modes

The project supports three launch modes:

### 1. Simulation Mode (Default)

Launches the robot in Gazebo simulation with controllers and standing pose:

```bash
./run_robot.sh simulation
# or simply
./run_robot.sh
```

### 2. Development Mode

Opens an interactive shell for development and debugging:

```bash
./run_robot.sh dev
```

Inside the container, you can manually run:
```bash
# Launch the Gazebo simulation
roslaunch puppy_description gazebo.launch

# Or run RViz visualization
roslaunch puppy_description display.launch

# Or any other ROS commands
rostopic list
rosnode list
```

### 3. RViz Visualization Mode

Launches only the RViz visualization (lighter weight, no physics simulation):

```bash
./run_robot.sh rviz
```

## Project Structure

The project is organized as follows:

- **Dockerfile**: Defines the ROS Noetic environment with necessary packages
- **docker-compose.yml**: Defines multiple services for different use cases
- **run_robot.sh**: Main script for launching the simulation in different modes
- **puppy_description/**: ROS package containing the robot model and simulation

For more detailed information about the project structure, see [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md).

## Docker Configuration

The project uses Docker to ensure consistent environment setup. Key features:

- ROS Noetic with Gazebo and all required packages
- X11 forwarding for GUI applications
- Volume mounts for development without rebuilding

For detailed information about Docker configuration, see [DOCKER_GUIDE.md](DOCKER_GUIDE.md).

## Development

The `puppy_description` package is mounted as a volume, so any changes you make to the files on your host machine will be reflected inside the container. Use the development mode for interactive testing:

```bash
./run_robot.sh dev
```

## Troubleshooting

### Display Issues

If you encounter issues with the GUI display:

```bash
# Allow X11 connections (Linux)
xhost +local:docker
```

### Docker Issues

If you encounter Docker-related issues:

```bash
# Clean up Docker system
docker system prune -a

# Rebuild without cache
docker-compose build --no-cache
```

For more troubleshooting tips, see [DOCKER_GUIDE.md](DOCKER_GUIDE.md).
