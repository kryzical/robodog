# Puppy Description Package

This package contains the robot's physical description including URDF models, meshes, and simulation configuration.

## Structure

- **config/**: Configuration files for the robot
  - **gazebo_control.yaml**: Gazebo controller configurations
  - **joint_names_puppy_description.yaml**: Standard joint naming definitions

- **launch/**: Launch files for visualization and simulation
  - **gazebo.launch**: Launch the robot in Gazebo simulator
  - **custom_world.launch**: Launch custom worlds with optional robot spawning

- **meshes/**: 3D mesh files for visual and collision representation
  - Contains STL files for each robot link

- **models/**: Gazebo model definitions for simulation environment objects
  - Contains various objects that can be used in simulation

- **urdf/**: Unified Robot Description Format files
  - Defines the robot's physical structure, joint properties, and sensors

- **worlds/**: Gazebo world definitions
  - Pre-configured simulation environments

## Usage

To launch the robot in Gazebo:
```
roslaunch puppy_description gazebo.launch
```

To launch just a custom world without the robot:
```
roslaunch puppy_description custom_world.launch
```

To launch a custom world with the robot:
```
roslaunch puppy_description custom_world.launch spawn_robot:=true
```