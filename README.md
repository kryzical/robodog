# PuppyPi Quadruped Robot

This repository contains the code for the PuppyPi robot, a quadruped robot with modular movement controls.

## Quick Start

To launch the robot simulation with the default movement (forward):

```bash
./test_robot.sh
```

This script will:
1. Launch Docker with proper X11 forwarding
2. Build the ROS workspace if needed
3. Launch Gazebo in a paused state
4. Wait for you to press the play button in Gazebo
5. Start the velocity walker controller
6. Execute the selected movement

## Movement Types

You can select different movement types by passing parameters:

```bash
# Format: ./test_robot.sh [movement_type] [speed] [duration]

# Walk forward at 0.2 m/s for 10 seconds (default)
./test_robot.sh forward 0.2 10.0

# Walk backward at 0.15 m/s for 8 seconds
./test_robot.sh backward 0.15 8.0

# Rotate left (counterclockwise) at 0.5 rad/s for 5 seconds
./test_robot.sh rotate_left 0.5 5.0

# Rotate right (clockwise) at 0.3 rad/s for 3 seconds
./test_robot.sh rotate_right 0.3 3.0
```

## Testing Multiple Movements

After the initial movement completes, the simulation will continue running. You can execute additional movement commands manually within the Docker container:

```bash
# Forward walking
python3 /ros_ws/src/puppy_description/scripts/movements/walk_forward.py --speed 0.2 --duration 10.0

# Backward walking
python3 /ros_ws/src/puppy_description/scripts/movements/walk_backward.py --speed 0.2 --duration 10.0

# Left rotation
python3 /ros_ws/src/puppy_description/scripts/movements/rotate_left.py --speed 0.5 --duration 5.0

# Right rotation
python3 /ros_ws/src/puppy_description/scripts/movements/rotate_right.py --speed 0.5 --duration 5.0
```

## Troubleshooting

If you encounter issues:

- **X11 Forwarding**: Make sure your X server allows connections from Docker
- **Multiple Gazebo Instances**: The script tries to clean up existing instances, but you might need to kill processes manually
- **Controller Errors**: Follow the prompts to make sure you press play in Gazebo before continuing
- **Robot Stability**: If the robot falls over, try a slower speed (e.g., 0.1 m/s for walking or 0.3 rad/s for rotation)

## Project Structure

- `puppy_description/`: Main ROS package containing the robot description and controllers
  - `scripts/`: Python scripts for controlling the robot
    - `velocity_walker.py`: Main walker implementation
    - `movements/`: Modular movement scripts
      - `walk_forward.py`: Forward walking implementation
      - `walk_backward.py`: Backward walking implementation
      - `rotate_left.py`: Left rotation implementation
      - `rotate_right.py`: Right rotation implementation
  - `launch/`: ROS launch files
    - `gazebo.launch`: Launches Gazebo with the robot
    - `just_walker.launch`: Launches just the velocity walker node
- `docker/`: Docker configuration for running the simulation
