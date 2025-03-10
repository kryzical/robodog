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
