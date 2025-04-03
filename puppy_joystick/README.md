# PuppyPi Joystick Control Package

This package provides joystick/gamepad control for the PuppyPi robot simulation. It translates joystick inputs into velocity commands that control the robot's movement in Gazebo.

## Features

- Support for both physical and virtual joysticks
- Configurable button and axis mappings
- Analog stick control for smooth operation
- Built-in connection maintenance
- Status reporting for debugging

## Components

### 1. Joypad Controller (`joypad_controller.py`)

The core controller that subscribes to `/joy` messages and publishes to `/cmd_vel`. Features:

- Configurability through ROS parameters
- Customizable button mappings for different controller types
- Support for analog stick movement with deadzone handling
- Automatic connection maintenance with periodic status reporting

### 2. Virtual Joystick (`virtual_joystick.py`)

A GUI-based virtual joystick implemented in Python/Tkinter. Features:

- Visual analog stick representation
- Button controls with visual feedback
- Regular publishing of joystick messages
- Status information display

### 3. Launch Files

- `virtual_joystick.launch`: Uses RQT Virtual Joy
- `virtual_joystick_py.launch`: Uses the custom Python virtual joystick

## Usage

### Physical Joystick

1. Connect your joystick/gamepad to your computer
2. Run the controller:

```bash
roslaunch puppy_joystick physical_joystick.launch
```

### Virtual Joystick

Run the virtual joystick interface:

```bash
roslaunch puppy_joystick virtual_joystick_py.launch
```

### Default Button Mapping

The default button mapping is set up for PS4-style controllers:

- **Triangle** (Button 4): Forward
- **Cross/X** (Button 6): Backward
- **Square** (Button 7): Left rotation
- **Circle** (Button 5): Right rotation
- **Share** (Button 2): Stop

For Xbox controllers, use the `button_mapping:=xbox` parameter.

## Parameters

The joypad controller accepts the following parameters:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `forward_button` | int | 4 | Button index for forward movement |
| `backward_button` | int | 6 | Button index for backward movement |
| `left_button` | int | 7 | Button index for left rotation |
| `right_button` | int | 5 | Button index for right rotation |
| `stop_button` | int | 2 | Button index for stopping movement |
| `linear_axis` | int | 1 | Axis index for forward/backward |
| `angular_axis` | int | 0 | Axis index for left/right rotation |
| `linear_scale` | float | 0.2 | Max linear velocity (m/s) |
| `angular_scale` | float | 0.8 | Max angular velocity (rad/s) |
| `dead_zone` | float | 0.05 | Deadzone for analog sticks |
| `analog_mode` | bool | true | Whether to use analog sticks |

Example:
```bash
roslaunch puppy_joystick virtual_joystick_py.launch linear_scale:=0.3 angular_scale:=0.6
```

## Troubleshooting

1. **No response to joystick input**:
   - Check if joy messages are being published: `rostopic echo /joy`
   - Verify the controller is running: `rosnode info /joypad_controller`
   - Restart the controller: `rosnode kill /joypad_controller && rosrun puppy_joystick joypad_controller.py`

2. **Incorrect button mapping**:
   - Determine your joystick's button indices: `jstest /dev/input/js0`
   - Override with custom parameters: `roslaunch puppy_joystick virtual_joystick_py.launch forward_button:=3`

3. **Simulation not responding to commands**:
   - Make sure the velocity walker is running: `rosnode info /velocity_walker`
   - Check if cmd_vel messages are being published: `rostopic echo /cmd_vel`
   - Verify Gazebo is in running state (not paused)
   - Reset communication with: `rostopic pub -1 /cmd_vel geometry_msgs/Twist "{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}"`

## Integration with PuppyPi

The joystick control package is designed to work with the PuppyPi's velocity walker. The control flow is:

```
Joystick Input → Joy Messages → Joypad Controller → cmd_vel → Velocity Walker → Joint Commands → Robot
```

The velocity walker translates the linear and angular velocities into appropriate joint movements to make the robot walk or rotate.

## Dependencies

- ROS Noetic
- joy package
- geometry_msgs
- sensor_msgs
- python-tk (for virtual joystick) 