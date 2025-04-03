# PuppyPi Robot Movement Scripts

This directory contains scripts for controlling the movement of the PuppyPi quadruped robot.

## Available Movement Scripts

### Forward Walking
- **`cmd_vel_publisher.py`**: Sends linear velocity commands to make the robot walk forward
  ```bash
  rosrun puppy_description cmd_vel_publisher.py --linear 0.2 --duration 10.0
  ```

### Backward Walking
- **`reverse_velocity_walker.py`**: Makes the robot walk backward using direct joint control
  ```bash
  python3 reverse_velocity_walker.py --duration 10.0 --speed 0.3
  ```

## Usage Within Docker Environment

To run these scripts within the Docker environment, use:

```bash
docker-compose -f docker/docker-compose.yml run --rm dev /bin/bash -c "cd /ros_ws && source devel/setup.bash && python3 /ros_ws/src/puppy_description/scripts/movements/SCRIPT_NAME.py [options]"
```

## Recommended Scripts for Various Movements

| Movement | Recommended Script | Parameters |
|----------|-------------------|------------|
| Forward walking | cmd_vel_publisher.py | --linear 0.2 --duration 10.0 |
| Backward walking | reverse_velocity_walker.py | --duration 10.0 --speed 0.3 |

## Implementation Notes

- The `reverse_velocity_walker.py` is the most reliable method for backward walking, implementing a direct reversal of the original velocity walker's gait pattern.
- For detailed documentation on backward walking implementation, see `docs/BACKWARD_WALKING.md`.

## Archive

Previous experimental versions of the backward walking scripts have been moved to the `archive` directory for reference. 