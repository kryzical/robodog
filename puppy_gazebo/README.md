# Puppy Gazebo Package

This package contains Gazebo-specific simulation tools and environments for the puppy robot.

## Structure

- **config/**: Gazebo-specific configuration files
  - Contains parameters for simulation physics and controllers

- **launch/**: Gazebo simulation launch files
  - **custom_world.launch**: Launch custom simulation worlds (linked to puppy_description)
  - **gazebo.launch**: Launch Gazebo with the robot in an empty world
  - **rviz.launch**: Launch RViz visualization for the simulation

- **scripts/**: Helper scripts for simulation
  - Contains utility scripts for Gazebo simulation

- **src/**: Source code for simulation plugins
  - Custom Gazebo plugins for the puppy robot

- **worlds/**: Gazebo world definitions
  - Pre-defined simulation environments

## Usage

To launch the simulation:
```
roslaunch puppy_gazebo gazebo.launch
```

For visualization:
```
roslaunch puppy_gazebo rviz.launch
```