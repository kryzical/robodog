# Launch Files Documentation

This directory contains launch files for the puppy_gazebo package.

## custom_world.launch

This is a symbolic link to the version in puppy_description package, providing a unified launch interface.

## gazebo.launch

Launches an empty Gazebo world and spawns the puppy robot with appropriate controllers.

This version:
- Initializes the robot with specific joint positions (-0.4, 1.2 for various joints)
- Sets initial controller positions to match spawn positions
- Uses a simpler controller spawning approach with a single spawner node
- Has a different physics pausing/unpausing sequence

## rviz.launch

Launches RViz with a configuration specialized for visualizing the puppy robot.