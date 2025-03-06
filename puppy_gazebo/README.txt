PUPPY_GAZEBO PACKAGE
===================

This package handles all Gazebo simulation-specific functionality:

Key Components:
- Gazebo plugin configurations
- Simulation-specific launch files
- Custom world environments
- Gazebo-ROS interface controllers

Directories:
/config - Simulation-specific configurations
/launch - Gazebo simulation launch files
/scripts - Helper scripts for simulation
/src - Custom Gazebo plugin implementations
/worlds - Simulation world definitions

Main Features:
- Integration between ROS and Gazebo
- Physics simulation setup
- Sensor simulation (IMU, contacts, etc.)
- Custom world environments

Dependencies:
- Gazebo ROS packages
- puppy_description for robot model
- ROS Control for actuator simulation