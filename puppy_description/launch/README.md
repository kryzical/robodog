# Launch Files Documentation

This directory contains launch files for the puppy_description package.

## custom_world.launch

A flexible launch file for spawning a custom Gazebo world with optional robot and walking behavior.

**Arguments:**
- `spawn_robot` (default: false): Whether to spawn the robot model
- `start_walking` (default: false): Whether to start the walking node
- `world_file` (default: fetchit_challenge_tests_lowlights.world): World file to load

**Examples:**
- Load only the custom world: `roslaunch puppy_description custom_world.launch`
- Load world with robot: `roslaunch puppy_description custom_world.launch spawn_robot:=true`
- Load world with robot and start walking: `roslaunch puppy_description custom_world.launch spawn_robot:=true start_walking:=true`

## gazebo.launch

Launches an empty Gazebo world and spawns the puppy robot with appropriate controllers.

This version:
- Uses specific timing for spawning controllers
- Uses a phased initialization approach
- Focuses on stable robot spawning with knees slightly bent

**Note:** This differs from the version in `puppy_gazebo` which uses a different initialization approach.