# PuppyPi Movement Commands Guide

This guide provides comprehensive documentation for controlling the movement of the PuppyPi quadruped robot using various commands and scripts.

## Quick Reference

| Movement | Command | Parameters |
|----------|---------|------------|
| **Forward walk** | `cmd_vel_publisher.py` | `--linear 0.2 --duration 10.0` |
| **Backward walk** | `reverse_velocity_walker.py` | `--duration 10.0 --speed 0.3` |

## Setting Up the Environment

Before running any movement commands, you need a running Gazebo simulation with the robot. Use:

```bash
docker-compose -f docker/docker-compose.yml run --rm dev /bin/bash -c "cd /ros_ws && source devel/setup.bash && roslaunch puppy_description gazebo.launch"
```

In a separate terminal, start the velocity walker controller:

```bash
docker-compose -f docker/docker-compose.yml run --rm dev /bin/bash -c "cd /ros_ws && source devel/setup.bash && roslaunch puppy_description just_walker.launch"
```

## Forward Walking

The robot walks forward by sending positive linear velocity commands through the `/cmd_vel` topic.

### Simple Forward Walking Command

```bash
docker-compose -f docker/docker-compose.yml run --rm dev /bin/bash -c "cd /ros_ws && source devel/setup.bash && rosrun puppy_description cmd_vel_publisher.py --linear 0.2 --duration 10.0"
```

Parameters:
- `--linear`: Speed in m/s (positive values for forward)
- `--duration`: How long to walk in seconds
- `--angular`: Optional rotation rate for turning (radians/s)

## Backward Walking

We've implemented a specialized controller for backward walking that directly controls joint positions for reliable backward motion.

### Using the Reverse Velocity Walker

```bash
docker-compose -f docker/docker-compose.yml run --rm dev /bin/bash -c "cd /ros_ws && source devel/setup.bash && python3 /ros_ws/src/puppy_description/scripts/movements/reverse_velocity_walker.py --duration 10.0 --speed 0.3"
```

Parameters:
- `--duration`: How long to walk backward in seconds
- `--speed`: Movement speed factor (higher is faster)

This implementation directly reverses the gait pattern by un-reversing the angle adjustments in the original velocity walker that were marked with "REVERSED FOR FORWARD MOTION" comments.

## Implementation Notes

### Forward Walking
- Uses the velocity walker controller via cmd_vel messages
- Predictable and stable movement
- Speed scaling is linear and works well up to about 0.3 m/s

### Backward Walking
- Direct joint control is more effective than cmd_vel interface for backward motion
- The original velocity walker heavily favors forward motion in its implementation
- Best results come from directly reversing the original gait pattern

## Troubleshooting

If the robot doesn't move as expected:

1. Ensure the Gazebo simulation is running and not paused
2. Verify the velocity walker controller is active
3. Confirm there are no errors in the terminal
4. Try resetting the robot's position if it has fallen or is in an unstable state
5. Try a lower speed if the movement is unstable

## Further Documentation

- For detailed backward walking implementation: see `docs/BACKWARD_WALKING.md`
- For all movement scripts: see `puppy_description/scripts/movements/README.md` 