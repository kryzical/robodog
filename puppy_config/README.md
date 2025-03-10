# Puppy Config Package

This package provides configuration parameters and settings for the quadruped robot across different subsystems.

## Structure

- **config/**: Configuration files for various subsystems
  - **ekf/**: Extended Kalman Filter parameters
  - **gait/**: Gait pattern configurations
  - **move_base/**: Navigation parameters
  - **ros_control/**: ROS control parameters
  - **twist/**: Twist message conversion parameters
  - **velocity_smoother/**: Velocity smoothing parameters

- **include/**: Header files for configuration
  - **gait_config.h**: Gait configuration definitions
  - **hardware_config.h**: Hardware-specific configurations
  - **quadruped_description.h**: Robot description parameters

- **launch/**: Launch files for different configurations
  - **bringup.launch**: Main robot startup
  - **navigate.launch**: Navigation stack startup
  - **slam.launch**: SLAM (Simultaneous Localization and Mapping)
  - **test_navigation.launch**: Test navigation functionalities
  - **test_walk.launch**: Test walking with teleop control
  - **include/**: Modular launch components

## Usage

To start the robot with navigation:
```
roslaunch puppy_config navigate.launch
```

For testing the walking capabilities with teleop:
```
roslaunch puppy_config test_walk.launch
```

For SLAM operation:
```
roslaunch puppy_config slam.launch
```