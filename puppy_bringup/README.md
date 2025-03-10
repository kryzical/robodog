# Puppy Bringup Package

This package contains the scripts and configuration files needed to start the puppy robot system in different modes.

## Overview

The bringup package serves as the entry point for starting up the robot, either in simulation or on real hardware. It coordinates the launch sequence for all necessary components.

## Structure

- **scripts/**: Helper scripts for robot initialization
  - **__init__.py**: Package initialization

## Usage

While this package is currently a template that will be filled in with startup procedures later, it will eventually provide the main launch files for the robot system:

```bash
# Future usage example:
roslaunch puppy_bringup start_robot.launch
```