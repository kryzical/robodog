# RoboDog2 Quadruped Robot Platform

A ROS-based platform for controlling and simulating a quadruped robot.

documentation supporting this structure system: https://wiki.ros.org/BestPractices

## Project Structure

The project is organized into several ROS packages:

- **puppy**: this serves as a "navigation", or a quick snippet of all the packages we use here
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

## Development Notes

- All controllers inherit from the base `PuppyJointController` class
- IK calculations handle front/back leg differences automatically
- Common standing positions are shared between different controllers

# Robodog Project

## Running the Project

This project is designed to be portable and run on any device. There are two main ways to run it:

### 1. Core Robot Functionality (Headless)
For running the core robot functionality without visualization:
```bash
chmod +x run_container_headless.sh
./run_container_headless.sh
```

Then inside the container:
```bash
roslaunch puppy_camera puppy_camera.launch
```

### 2. Visualization (On Any Device with X11)
To view the robot visualization on any machine with X11 support (including Steam Deck):

1. Make sure you have Docker and ROS Noetic installed
2. Run the visualization container:
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

The visualization should work on Steam Deck as it runs Linux and has X11 support.
