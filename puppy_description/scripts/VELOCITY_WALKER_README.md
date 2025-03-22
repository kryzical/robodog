# Velocity Walker for PuppyPi Robot

This implementation adds velocity-based control to the PuppyPi robot using ROS topics. The robot is controlled by publishing messages to the `/cmd_vel` topic, which are translated into appropriate leg movements to achieve forward walking.

## Overview

The velocity walker implementation consists of the following components:

1. `velocity_walker.py`: The main node that subscribes to `/cmd_vel` messages and controls the robot's legs
2. `test_velocity_walking.py`: A testing utility to send velocity commands to the robot
3. `run_velocity_walker.sh`: A shell script to launch the system with proper sequencing
4. Launch files:
   - `velocity_control.launch`: Launches Gazebo and the robot (paused initially)
   - `velocity_walker.launch`: Launches just the velocity walker node (after Gazebo is running)

## Setup and Usage

### Running the Velocity Walker

1. Make the scripts executable:
   ```bash
   chmod +x puppy_description/scripts/velocity_walker.py
   chmod +x puppy_description/scripts/test_velocity_walking.py
   chmod +x puppy_description/scripts/run_velocity_walker.sh
   ```

2. Launch the system using the run script:
   ```bash
   ./puppy_description/scripts/run_velocity_walker.sh
   ```
   This script will:
   - Launch Gazebo with the robot in a paused state
   - Wait for you to press the play button in Gazebo
   - Launch the velocity walker node
   - Set the robot to its standing position

### Testing the Walker

#### Automatic Test Sequence

To run a predefined test sequence:
```bash
rosrun puppy_description test_velocity_walking.py --mode auto
```

This will:
1. Walk forward at 0.2 m/s for 10 seconds
2. Stop and return to standing position for 3 seconds
3. Walk at 0.1 m/s for 5 seconds
4. Stop again

#### Interactive Mode

To control the robot interactively:
```bash
rosrun puppy_description test_velocity_walking.py --mode interactive
```

This starts an interactive prompt where you can enter commands in the format:
```
linear_x angular_z duration
```

For example:
- `0.2 0.0 5.0` - Walk forward at 0.2 m/s for 5 seconds
- `0.0 0.0 1.0` - Stop and stand for 1 second

Type `q` to exit interactive mode.

#### Single Command

To send a single command:
```bash
rosrun puppy_description test_velocity_walking.py --linear 0.2 --angular 0.0 --duration 5.0
```

### Manual Control

You can also send commands directly using the `rostopic` command:

```bash
# Walk forward at 0.2 m/s
rostopic pub /cmd_vel geometry_msgs/Twist '{linear: {x: 0.2, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}'

# Stop and return to standing position
rostopic pub /cmd_vel geometry_msgs/Twist '{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}'
```

## Implementation Details

The velocity walker works by:
1. Maintaining a stable standing position when not moving
2. Using a diagonal gait pattern (similar to how dogs walk) for forward movement
3. Scaling step size based on the requested linear velocity
4. Ensuring the robot returns to a stable standing position when stopped

The implementation uses either the built-in inverse kinematics (if available) or a simplified joint angle control approach as a fallback.

## Troubleshooting

- If the robot seems unstable, try decreasing the linear velocity
- Make sure to wait for the robot to reach a stable standing position before sending movement commands
- If legs get stuck, send a stop command (0.0 velocity) to reset to the standing position

## Future Improvements

Potential improvements include:
- Adding support for angular velocity to implement turning
- Implementing more sophisticated gait patterns
- Adding adaptive step height based on terrain
- Implementing smoother transitions between velocity changes 