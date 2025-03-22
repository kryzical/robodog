# PuppyPi Robot Walking Guide

This guide provides instructions on testing, running, and evaluating the walking capabilities of the PuppyPi robot.

## Overview

The PuppyPi robot uses a diagonal gait pattern where diagonal pairs of legs move together to maintain stability while walking. The implementation supports:

- Walking forward with stable balance
- Automatic parameter optimization for improved gait
- Performance monitoring and testing
- Distance and time-limited walking tests

## Running Test Scripts

There are several ways to test the robot's walking functionality:

### 1. Basic Movement Test

The movement test script runs a simple walking test with performance monitoring. It will walk the robot to a target distance of 2 meters by default.

```bash
cd puppy_description/scripts
./run_test.sh
```

### 2. Autonomous Walking

The autonomous walker provides a more advanced, continuous walking capability with automatic parameter adjustment.

```bash
cd puppy_description/scripts
./run_autonomous_walker.sh
```

You can also specify distance or time limits:

```bash
# Walk for 5 meters
./run_autonomous_walker.sh -d 5.0

# Walk for 60 seconds
./run_autonomous_walker.sh -t 60.0

# Walk for 3 meters or 30 seconds, whichever comes first
./run_autonomous_walker.sh -d 3.0 -t 30.0
```

### 3. Gait Optimization

For advanced users, you can run the gait optimization to find the best walking parameters for your robot:

```bash
cd puppy_description/scripts
./run_gait_optimization.sh
```

## Performance Metrics

The walking implementation tracks several performance metrics:

1. **Distance Traveled**: Total distance the robot has moved from its starting position
2. **Speed**: Current and average walking speed in meters per second
3. **Lateral Drift**: Side-to-side deviation from straight-line path
4. **Direction Angle**: Angle of travel compared to intended direction
5. **Stability Score**: A normalized score (0-1) indicating how stable the robot is while walking

## How the Walking Works

The robot uses a diagonal gait pattern where diagonal pairs of legs (LF+RB, then RF+LB) move in sequence to maintain balance:

1. First diagonal pair (Left Front + Right Back) lifts and moves forward
2. First diagonal pair lowers to the ground and pushes
3. Second diagonal pair (Right Front + Left Back) lifts and moves forward
4. Second diagonal pair lowers to the ground and pushes
5. Repeat

This creates a stable walking motion while maintaining the robot's standing position throughout the gait cycle.

## Troubleshooting

If you encounter issues with the robot's walking:

1. **Robot falls over**: The step height might be too high, or the movement too fast
   - Reduce `STEP_HEIGHT` in the code
   - Increase phase timing values to slow down the motion

2. **Robot doesn't move forward**: The step length might be too small
   - Increase `STEP_LENGTH` in the code

3. **Robot drifts to one side**: The leg positions might be asymmetrical
   - Check the leg position calculations
   - Adjust the stance width parameters

4. **Jerky movement**: The transition steps might be too few
   - Increase `TRANSITION_STEPS` for smoother movement

## Advanced Configuration

The walking behavior can be customized by modifying these parameters in the `autonomous_walker.py` file:

```python
# Standing position parameters
self.STAND_HEIGHT = 0.12  # Height from ground to body
self.STAND_WIDTH = 0.05   # Width between legs
self.STAND_LENGTH = 0.07  # Length offset for standing position

# Step parameters
self.STEP_HEIGHT = 0.05   # Height for leg lifting
self.STEP_LENGTH = 0.05   # Length of forward step

# Timing parameters
self.PHASE_1_TIME = 0.10  # Time for lifting leg
self.PHASE_2_TIME = 0.08  # Time for moving leg forward
self.PHASE_3_TIME = 0.10  # Time for lowering leg
self.PHASE_4_TIME = 0.08  # Time for pushing back
```

## Evaluating Walking Performance

To evaluate the walking performance:

1. Run the movement test with default settings
2. Check the final distance, time, and calculated speed
3. Observe stability during walking (does the robot maintain balance?)
4. Check for lateral drift (does the robot walk in a straight line?)
5. Adjust parameters as needed and retest

Good walking performance should achieve:
- Speed of 0.1-0.3 m/s
- Lateral drift less than 0.2m over 2m distance
- Direction angle deviation less than 10 degrees
- Stability score consistently above 0.8 