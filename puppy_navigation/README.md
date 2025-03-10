# Puppy Navigation Package

This package integrates navigation capabilities for the puppy robot, allowing it to plan paths and navigate through environments.

## Overview

The puppy_navigation package provides the necessary components for autonomous navigation:
- Path planning
- Obstacle avoidance
- Localization
- Mapping

## Features

- Integration with ROS navigation stack
- Support for SLAM (Simultaneous Localization and Mapping)
- Custom navigation parameters optimized for quadrupedal motion
- Map management utilities

## Usage

This package is used in conjunction with `puppy_config` for navigation tasks:

```bash
# For autonomous navigation with a pre-built map:
roslaunch puppy_config navigate.launch

# For SLAM to create a new map:
roslaunch puppy_config slam.launch
```