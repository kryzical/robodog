PUPPY_DESCRIPTION PACKAGE
=====================

This package contains the robot's physical description and simulation assets:

Key Components:
- URDF (Unified Robot Description Format) files
- 3D mesh files for robot parts
- Gazebo simulation configurations
- Launch files for visualization and simulation
- Custom world models for testing

Directories:
/config - Joint configuration and Gazebo control parameters
/launch - Launch files for visualization and simulation
/meshes - STL files for robot parts (base, legs, sensors)
/models - Collection of Gazebo world objects and environment models
/rviz - RViz visualization configurations
/urdf - Robot description files
/worlds - Gazebo world definitions

Main Features:
- Complete robot model description
- Simulation environment setup
- Visualization tools
- Joint configuration management

Used By:
- puppy_gazebo for simulation
- puppy_base for control
- puppy_navigation for path planning
- All packages requiring robot model information