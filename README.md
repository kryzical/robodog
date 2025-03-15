# RoboDog2 Quadruped Robot Platform

A ROS-based platform for controlling and simulating a quadruped robot.

Documentation supporting this structure system: https://wiki.ros.org/BestPractices

## Project Structure

The project is organized into several ROS packages:

- **puppy**: Quick navigation to all the packages we use here
- **puppy_base**: Core control algorithms and scripts for the robot
- **puppy_description**: URDF models and visualization for the robot
- **puppy_gazebo**: Gazebo simulation environments and plugins
- **puppy_msgs**: Custom message definitions for the robot
- **puppy_navigation**: Navigation stack integration for autonomous movement
- **puppy_config**: Centralized configuration for all packages
- **puppy_bringup**: Launch files to start the real robot
- **puppy_camera**: Camera integration for perception

## Key Components

### Robot Controller Library

The centralized controller library (`robot_controller_lib.py`) provides:

- Joint control abstractions
- Inverse kinematics for leg positioning
- Smooth movement transitions
- Common robot poses and movements

### Standing and Walking

Two primary movement scripts are provided:

1. **stand_up.py**: Gets the robot into a balanced standing position
2. **walking.py**: Implements various gaits for forward movement

## Usage

### Standing the Robot

```
roslaunch puppy_base stand.launch
```

### Walking Control

```
roslaunch puppy_base walking.launch
```

### Running in Simulation

```
roslaunch puppy_gazebo custom_world.launch
roslaunch puppy_base simulation_control.launch
```

You can specify which controller to use with the `controller` argument:

```
roslaunch puppy_base simulation_control.launch controller:=stand
roslaunch puppy_base simulation_control.launch controller:=walking
roslaunch puppy_base simulation_control.launch controller:=test
```

## Configuration

The robot's configuration parameters are centralized in the `puppy_config` package:

- **Gait parameters**: Defined in `gait_config.h`
- **Hardware settings**: Defined in `hardware_config.h`
- **Robot description**: Available in `quadruped_description.h`

## Running the Project

This project can run on any device through Docker containers:

### 1. Core Robot Functionality (Headless)
For running the core robot functionality without visualization:
```bash
chmod +x run_container_headless.sh
./run_container_headless.sh
```

### 2. Visualization (On Any Device with X11)
To view the robot visualization on any machine with X11 support (including Steam Deck):

```bash
chmod +x run_container_gui.sh
./run_container_gui.sh
```

### Network Configuration
If running the visualization on a different machine:

1. On the robot (core) machine, set:
```bash
export ROS_IP=<robot_ip>
export ROS_HOSTNAME=<robot_ip>
```

2. On the visualization machine, set:
```bash
export ROS_MASTER_URI=http://<robot_ip>:11311
export ROS_IP=<local_ip>
export ROS_HOSTNAME=<local_ip>
```

Replace `<robot_ip>` with the IP address of the robot machine and `<local_ip>` with the IP of your visualization machine.

## Steam Deck Setup
For Steam Deck users:

1. Switch to Desktop Mode
2. Install Docker using the standard installation method
3. Follow the "Visualization" instructions above

## Quick Start Commands

The `puppypi.sh` script provides several commands:

```bash
./puppypi.sh start      # Start the robot simulation and controllers
./puppypi.sh status     # Check the status of the robot
./puppypi.sh stop       # Stop the robot
./puppypi.sh restart    # Restart the robot
./puppypi.sh controller # Run only the controller
./puppypi.sh help       # Show help information
```

## Robot Features

- Advanced gait control with multiple patterns (trot, walk, pace, bound)
- Stabilization using IMU data
- Camera integration
- Navigation capabilities
- RViz visualization tools
- Spot-like crouched position for optimal stability

## enter docker from another terminal
docker exec -it puppy_ros_dev_gazebo bash

cd /workspace
source devel/setup.bash