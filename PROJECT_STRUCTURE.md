# PuppyPi Robot Project Structure

This document explains the organization of the PuppyPi robot simulation project.

## Main Directory Structure

```
/home/brian/robots/puppypi_v2/robodog/    # Main project directory
├── Dockerfile                            # Docker image definition
├── docker-compose.yml                    # Multi-service configuration
├── run_robot.sh                          # Main launch script
├── puppy_description/                    # ROS package for the robot
│   ├── config/                           # Controller configuration
│   ├── launch/                           # Launch files
│   ├── meshes/                           # 3D model files
│   ├── rviz/                             # RViz configuration
│   ├── urdf/                             # Robot URDF/Xacro files
│   ├── CMakeLists.txt                    # Build configuration
│   └── package.xml                       # Package metadata
├── reference/                            # Reference materials (kept for examples)
├── README.md                             # Main project documentation
├── DOCKER_GUIDE.md                       # Docker configuration guide
└── PROJECT_STRUCTURE.md                  # This file
```

## Primary Files and Their Purpose

### Core Files

- **run_robot.sh**: The main script for launching the simulation
  - Supports multiple modes: simulation, dev, rviz
  - Example usage: `./run_robot.sh simulation`

- **docker-compose.yml**: Defines the Docker services
  - simulation: Full Gazebo simulation
  - dev: Development environment
  - rviz: Lightweight visualization

- **Dockerfile**: Defines the ROS Noetic environment with necessary packages

### Documentation

- **README.md**: Main project documentation with usage instructions
- **DOCKER_GUIDE.md**: Detailed guide for the Docker configuration
- **puppy_description/README.md**: Documentation for the ROS package

### Active Directories

- **puppy_description/**: The main ROS package - This is where all robot model files live
- **reference/**: Contains reference implementations that can be used as examples

## Working with This Project

### Development Workflow

1. Make changes to files in the `puppy_description/` directory
2. Use `./run_robot.sh dev` to test changes interactively
3. Launch the simulation with `./run_robot.sh` to see the full environment

### Adding New Features

- To add sensors: Modify the URDF files in `puppy_description/urdf/`
- To adjust controllers: Edit `puppy_description/config/gazebo_control.yaml`
- To create new launch configurations: Add to `docker-compose.yml` and update `run_robot.sh`

## Maintenance Notes

- The project uses Git for version control
- Keep reference/ for examples but don't use those files directly in the project
