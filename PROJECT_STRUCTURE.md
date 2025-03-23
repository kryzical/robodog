# PuppyPi Project Structure

This document outlines the directory structure and file organization of the PuppyPi robot simulation project to help users and developers navigate the codebase.

## Directory Structure

```
puppypi_v3/
└── robodog/
    ├── docker/                  # Docker configuration files
    ├── docs/                    # Documentation files
    ├── puppy_description/       # Robot description package (URDF, meshes, configs)
    │   ├── config/              # Configuration files for controllers
    │   ├── launch/              # ROS launch files
    │   ├── meshes/              # 3D models for visualization
    │   ├── scripts/             # Control scripts and utilities
    │   │   └── movements/       # Movement implementation scripts
    │   ├── urdf/                # URDF model files
    │   ├── CMakeLists.txt       # Build configuration
    │   └── package.xml          # Package metadata
    │
    ├── puppy_joystick/          # Joystick control package
    │   ├── launch/              # Launch files for joystick control
    │   ├── scripts/             # Joystick controller scripts
    │   │   └── utils/           # Utility scripts for joystick control
    │   ├── CMakeLists.txt       # Build configuration
    │   ├── package.xml          # Package metadata
    │   └── README.md            # Package-specific documentation
    │
    ├── puppy_control_ros2/      # ROS2 controller template
    │   ├── include/             # C++ header files
    │   ├── src/                 # C++ source files
    │   ├── CMakeLists.txt       # Build configuration
    │   └── package.xml          # Package metadata
    │
    ├── ros1_bridge_config/      # ROS1-ROS2 bridge configuration
    │   ├── bridge_mapping.yaml  # Topic mapping configuration
    │   └── launch_bridge.sh     # Bridge launch script
    │
    ├── scripts/                 # Miscellaneous utility scripts
    │
    ├── JOYSTICK_IMPLEMENTATION.md  # Joystick implementation documentation
    ├── README.md                   # Main project documentation
    ├── test_joystick_control.sh    # Physical joystick test script
    ├── test_minimal_simulation.sh  # Main test script
    ├── test_robot.sh               # Full robot simulation test
    └── test_virtual_joystick.sh    # Virtual joystick test script
```

## Key Files and Their Purpose

### Core Robot Description

- `puppy_description/urdf/puppy.urdf.xacro`: Main robot model definition
- `puppy_description/config/controller.yaml`: Controller configuration
- `puppy_description/launch/gazebo.launch`: Main simulation launch file

### Control Implementation

- `puppy_description/scripts/velocity_walker.py`: Main walking controller
- `puppy_description/scripts/movements/cmd_vel_publisher.py`: Forward movement utility
- `puppy_description/scripts/movements/reverse_velocity_walker.py`: Backward movement implementation

### Joystick Control

- `puppy_joystick/scripts/joypad_controller.py`: Joystick to velocity command translator
- `puppy_joystick/scripts/virtual_joystick.py`: GUI-based virtual joystick
- `puppy_joystick/launch/joystick.launch`: Launch file for joystick control

### Docker and Testing

- `docker/Dockerfile`: Docker environment definition
- `test_minimal_simulation.sh`: Main test script for simulation with joystick
- `test_virtual_joystick.sh`: Test script for the virtual joystick

## Package Relationships

The project's components interact in the following way:

1. `puppy_description` provides the robot model and simulation environment
2. `puppy_joystick` provides control interfaces through joystick input
3. `puppy_control_ros2` (experimental) provides a bridge to ROS2 control systems

## Build System

The project uses the ROS Catkin build system. The main workspace is set up within the Docker container at `/ros_ws`.

## Testing and Execution

The project includes several test scripts for different scenarios:

- `test_minimal_simulation.sh`: Minimal test with joystick control
- `test_joystick_control.sh`: Test with physical joystick
- `test_virtual_joystick.sh`: Test with virtual joystick
- `test_robot.sh`: Full simulation test 