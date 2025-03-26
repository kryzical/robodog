# PuppyPi ROS1 Robot Simulation

This repository contains the ROS1 simulation for the PuppyPi robot, including Gazebo simulation, virtual joystick control, and velocity-based walking.

## Prerequisites

- ROS1 Noetic
- Gazebo
- Python 3
- Required ROS packages:
  - `ros-noetic-effort-controllers`
  - `ros-noetic-joy`
  - `ros-noetic-rqt-console`

## Setup

1. Clone this repository into your ROS workspace:
```bash
cd ~/catkin_ws/src
git clone <repository-url>
```

2. Build the workspace:
```bash
cd ~/catkin_ws
catkin build
```

3. Source the workspace:
```bash
source ~/catkin_ws/devel/setup.bash
```

## Running the Simulation

### Quick Start
The easiest way to run the simulation is using the test script:
```bash
./test_virtual_joystick.sh
```

### Manual Launch
To launch components manually:

1. Start Gazebo with the robot:
```bash
roslaunch puppy_description gazebo.launch
```

2. Launch the velocity walker:
```bash
roslaunch puppy_description just_walker.launch
```

3. Start the virtual joystick:
```bash
rosrun puppy_joystick virtual_joystick.py
```

4. Launch the joypad controller:
```bash
rosrun puppy_joystick joypad_controller.py
```

## Controller Configuration

The robot uses effort controllers for joint position control. The configuration is located in `puppy_description/config/gazebo_control.yaml`. Key points:

- Each joint has a position controller with PID parameters
- Joint limits are set for velocity and position
- The configuration is loaded under the `puppy` namespace

### Default Button Mappings
- Forward: Button 4 (Triangle/Up)
- Backward: Button 6 (X/Down)
- Left: Button 7 (Square/Left)
- Right: Button 5 (Circle/Right)
- Stop: Button 2 (Share/Center)

### Analog Controls
- Linear velocity: Axis 1 (Up/down)
- Angular velocity: Axis 0 (Left/right)
- Linear scale: 0.2 m/s
- Angular scale: 0.8 rad/s
- Dead zone: 0.05

## Important Notes

1. **Controller Manager Initialization**
   - The controller manager must be initialized before spawning controllers
   - Controllers are spawned under the `puppy` namespace
   - A delay is added to ensure proper initialization order

2. **Joint State Publishing**
   - Joint states are published at 100Hz
   - The robot state publisher remaps joint states to `/puppy/joint_states`

3. **Initial Robot Pose**
   - The robot spawns at z=0.15
   - Initial joint positions are set for a standing pose:
     - Joint1 (lf_joint1): 0.8
     - Joint2 (rf_joint1): 0.8
     - Joint3 (lb_joint1): 0.8
     - Joint4 (rb_joint1): 0.8
     - Joint5-8 (lf_joint2, rf_joint2, lb_joint2, rb_joint2): 0.0

4. **Troubleshooting**
   - If controllers fail to spawn, check the controller manager logs
   - Ensure the effort controllers package is installed
   - Verify the robot model is properly loaded in Gazebo
   - Check that joint names match between URDF and controller configuration

## Directory Structure

```
puppy_description/
├── config/
│   └── gazebo_control.yaml    # Controller configuration
├── launch/
│   ├── gazebo.launch         # Main Gazebo launch file
│   └── just_walker.launch    # Velocity walker launch file
└── urdf/
    └── puppy.urdf.xacro      # Robot description

puppy_joystick/
├── launch/
│   └── gazebo_with_joystick.launch  # Combined launch file
└── scripts/
    ├── virtual_joystick.py   # Virtual joystick GUI
    └── joypad_controller.py  # Joypad control node
```

## Features

- Gazebo simulation with realistic physics
- Joint position and velocity control
- Joystick/gamepad control (virtual and physical)
- Movement scripts for basic locomotion
- Command-line tools for testing
- Support for a ROS1-ROS2 bridge (experimental)

## Quick Start

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/puppypi_v3.git
cd puppypi_v3
```

2. **Run the test script (with Docker)**

```bash
cd robodog
./test.sh
```

This will run a complete simulation setup inside Docker, including Gazebo with the PuppyPi robot.

3. **Test with joystick control**

```bash
cd robodog
./test_minimal_simulation.sh
```

This will run a minimal simulation with joystick control.

## Joystick Control

PuppyPi can be controlled using either a physical joystick/gamepad or a virtual joystick interface.

### Using a Physical Joystick

1. Connect your joystick/gamepad to your computer
2. Run the joystick test script:

```bash
cd robodog
./test_joystick_control.sh
```

### Default Button Mapping (PS4 Controller)

- **Triangle** (Button 4): Move forward
- **X** (Button 6): Move backward
- **Square** (Button 7): Rotate left
- **Circle** (Button 5): Rotate right
- **Share** (Button 2): Stop all movement
- **Left Analog Stick**: Move (forward/backward/turn)

### Using the Virtual Joystick

The virtual joystick provides a GUI interface for controlling the robot when a physical gamepad is not available.

```bash
cd robodog
./test_virtual_joystick.sh
```

## Movement Commands

The PuppyPi robot can be directly controlled using movement commands sent via ROS topics. These commands offer precise control for specific movements.

### Movement Command Reference

| Movement | Command | Parameters |
|----------|---------|------------|
| **Forward walk** | `cmd_vel_publisher.py` | `--linear 0.2 --duration 10.0` |
| **Backward walk** | `reverse_velocity_walker.py` | `--duration 10.0 --speed 0.3` |

### Forward Movement

The robot walks forward by sending positive linear velocity commands through the `/cmd_vel` topic.

```bash
# Example command for forward movement
rosrun puppy_description cmd_vel_publisher.py --linear 0.2 --duration 10.0
```

Parameters:
- `--linear`: Speed in m/s (positive values for forward)
- `--duration`: How long to walk in seconds
- `--angular`: Optional rotation rate for turning (radians/s)

### Backward Movement

For backward movement, a specialized controller is implemented that directly controls joint positions.

```bash
# Example command for backward movement
python3 /ros_ws/src/puppy_description/scripts/movements/reverse_velocity_walker.py --duration 10.0 --speed 0.3
```

Parameters:
- `--duration`: How long to walk backward in seconds
- `--speed`: Movement speed factor (higher is faster)

### Implementation Notes

Forward movement uses the velocity walker controller via cmd_vel messages and is stable up to about 0.3 m/s.

Backward movement uses direct joint control which is more effective than the cmd_vel interface for this direction.

## Architecture

The PuppyPi simulation is built on ROS1 (Noetic) and consists of several key components:

1. **Robot Description Package (`puppy_description`)**: Contains the URDF model, control configuration, and simulation setup for the robot.

2. **Joystick Controller Package (`puppy_joystick`)**: Handles joystick inputs and converts them to velocity commands.

3. **Velocity Walker**: The main control script that translates velocity commands into joint movements, implementing a simple walking gait.

### Control Flow

```
Joystick Input → Joy Messages → Joystick Controller → cmd_vel → Velocity Walker → Joint Commands → Robot
```

## ROS1-ROS2 Bridge (Experimental)

An experimental bridge setup is included for future integration with ROS2 systems:

- Bridge configuration: `ros1_bridge_config/bridge_mapping.yaml` 
- Launch script: `ros1_bridge_config/launch_bridge.sh`
- ROS2 controller template: `puppy_control_ros2/`

To use the bridge (requires ROS2 installation):
```bash
./ros1_bridge_config/launch_bridge.sh
```

## Project Structure

- `puppy_description/`: Robot description package containing URDF, meshes, and controller configurations
- `puppy_joystick/`: Joystick control package
- `ros1_bridge_config/`: Configuration for the ROS1-ROS2 bridge
- `puppy_control_ros2/`: Template for ROS2 control implementation
- `test_minimal_simulation.sh`: Main test script with joystick control
- `test_virtual_joystick.sh`: Test script for the virtual joystick interface
- `test_joystick_control.sh`: Test script for physical joystick control
- `JOYSTICK_IMPLEMENTATION.md`: Detailed documentation of joystick implementation and fixes

## Documentation

- For detailed joystick implementation information, see `JOYSTICK_IMPLEMENTATION.md`
- For a complete overview of the project directory structure, see `PROJECT_STRUCTURE.md`
- Each package includes its own README with specific details

## Troubleshooting

### ROS Core System Issues

If you encounter errors related to `roscore` already running:

```bash
# List running Docker containers
docker ps

# Stop all containers
docker stop $(docker ps -q)
```

### Joystick Not Working in Simulation

If the joystick control is not working properly:

1. **Verify joystick input**: Check if joy messages are being published:
   ```bash
   rostopic echo /joy
   ```

2. **Verify velocity commands**: Check if velocity commands are being published:
   ```bash
   rostopic echo /cmd_vel
   ```

3. **Debug the velocity walker**: Check if the velocity walker is receiving commands:
   ```bash
   # In the log output, look for lines containing:
   "Received velocity command: linear.x=X.XX, angular.z=X.XX"
   ```

4. **Restart communication**: Sometimes restarting the joystick controller helps:
   ```bash
   rosnode kill /joypad_controller
   rosrun puppy_joystick joypad_controller.py
   ```

5. **Ensure simulation is running**: The robot will only respond to commands when Gazebo is in running state, not paused.

### X11 Display Issues

If you encounter X11 display problems:

```bash
xhost +local:
```

### Joystick Not Detected

If your physical joystick is not detected:

```bash
# Check if joystick is detected
ls -l /dev/input/js*

# Run jstest to verify inputs
jstest /dev/input/js0
```

## Contributing

Contributions to improve the PuppyPi simulation are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
