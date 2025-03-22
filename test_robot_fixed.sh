#!/bin/bash

# =========================================================================
# PuppyPi Robot - Fixed Test Script
# =========================================================================
# This script fixes issues with the Controller Spawner waiting for /clock
# when Gazebo is paused, which can lead to hangs and error 130.
# =========================================================================

set -e  # Exit on error

# Movement types
MOVEMENT_TYPES=("forward" "backward" "rotate_left" "rotate_right")

# Default values
MOVEMENT=${1:-"forward"}
SPEED=${2:-0.2}
DURATION=${3:-10.0}

# Validate movement type
valid_movement=false
for type in "${MOVEMENT_TYPES[@]}"; do
    if [ "$MOVEMENT" == "$type" ]; then
        valid_movement=true
        break
    fi
done

if [ "$valid_movement" = false ]; then
    echo "Error: Invalid movement type '$MOVEMENT'"
    echo "Valid types: ${MOVEMENT_TYPES[*]}"
    exit 1
fi

# Print banner
echo "=============================="
echo "   PuppyPi Robot Test Script  "
echo "=============================="
echo "Movement: $MOVEMENT"
echo "Speed: $SPEED"
echo "Duration: $DURATION seconds"
echo "=============================="

# Allow X server connections from Docker
xhost +local:docker

# Clean up any existing containers
echo "Cleaning up existing containers..."
docker-compose -f docker/docker-compose.yml down

# Run the container with X11 forwarding
echo "Starting Docker with X11 forwarding..."
docker-compose -f docker/docker-compose.yml run --rm \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  dev /bin/bash -c "
    # Inside Docker container
    cd /ros_ws
    
    # Build workspace if needed
    if [ ! -f devel/setup.bash ]; then
      echo 'Workspace not built, building now...'
      catkin_make
    fi
    
    # Source ROS workspace
    source devel/setup.bash
    
    # Kill any existing processes
    pkill -9 -f gazebo 2>/dev/null || true
    pkill -9 -f gzserver 2>/dev/null || true
    pkill -9 -f gzclient 2>/dev/null || true
    pkill -9 -f velocity_walker.py 2>/dev/null || true
    pkill -9 -f controller_spawner 2>/dev/null || true
    sleep 2
    
    # Make scripts executable
    chmod +x /ros_ws/src/puppy_description/scripts/velocity_walker.py
    chmod +x /ros_ws/src/puppy_description/scripts/movements/*.py
    
    # Start Gazebo in UNPAUSED state - this is different from before
    # CRITICAL: Not using paused:=true here to prevent controller_spawner issues
    echo 'Starting Gazebo (unpaused)...'
    roslaunch puppy_description gazebo.launch gui:=true &
    GAZEBO_PID=\$!
    
    # Give Gazebo time to initialize (important for clock to be published)
    echo 'Waiting for Gazebo to initialize (20 seconds)...'
    sleep 20
    
    # Verify Gazebo is running by checking the process
    if ! ps -p \$GAZEBO_PID > /dev/null; then
      echo 'ERROR: Gazebo failed to start properly.'
      exit 1
    fi
    
    # Launch the velocity walker - now that Gazebo is running
    echo 'Starting velocity walker...'
    roslaunch puppy_description just_walker.launch &
    WALKER_PID=\$!
    
    # Wait for velocity walker to initialize
    echo 'Waiting for velocity walker to initialize (15 seconds)...'
    sleep 15
    
    # Verify the walker is running
    if ! ps -p \$WALKER_PID > /dev/null; then
      echo 'ERROR: Velocity walker failed to start.'
      exit 1
    fi
    
    # Run the selected movement script
    echo 'Executing $MOVEMENT movement...'
    case '$MOVEMENT' in
      'forward')
        python3 /ros_ws/src/puppy_description/scripts/movements/walk_forward.py --speed $SPEED --duration $DURATION
        ;;
      'backward')
        python3 /ros_ws/src/puppy_description/scripts/movements/walk_backward.py --speed $SPEED --duration $DURATION
        ;;
      'rotate_left')
        python3 /ros_ws/src/puppy_description/scripts/movements/rotate_left.py --speed $SPEED --duration $DURATION
        ;;
      'rotate_right')
        python3 /ros_ws/src/puppy_description/scripts/movements/rotate_right.py --speed $SPEED --duration $DURATION
        ;;
    esac
    
    echo 'Movement completed.'
    echo ''
    echo '=============================='
    echo '  Available Commands:         '
    echo '=============================='
    echo '  Forward walking:  '
    echo '    python3 /ros_ws/src/puppy_description/scripts/movements/walk_forward.py --speed <speed> --duration <duration>'
    echo '  Backward walking: '
    echo '    python3 /ros_ws/src/puppy_description/scripts/movements/walk_backward.py --speed <speed> --duration <duration>'
    echo '  Rotate left:      '
    echo '    python3 /ros_ws/src/puppy_description/scripts/movements/rotate_left.py --speed <speed> --duration <duration>'
    echo '  Rotate right:     '
    echo '    python3 /ros_ws/src/puppy_description/scripts/movements/rotate_right.py --speed <speed> --duration <duration>'
    echo '=============================='
    echo ''
    echo 'Press Ctrl+C to terminate Gazebo and exit.'
    
    # Keep the script running until Ctrl+C
    wait
"

# Reset X server permissions
xhost -local:docker

echo "Robot simulation terminated." 