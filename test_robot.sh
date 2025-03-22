#!/bin/bash

# =========================================================================
# PuppyPi Robot - Modular Test Script
# =========================================================================
# This script provides a modular approach to:
#  1. Launch Docker with proper X11 forwarding
#  2. Run ROS workspace setup 
#  3. Kill any existing Gazebo processes
#  4. Launch Gazebo (paused)
#  5. Prompt for user input to continue
#  6. Start the velocity walker
#  7. Execute the selected movement type (forward, backward, etc.)
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
    
    # Start Gazebo paused
    echo 'Starting Gazebo (paused)...'
    roslaunch puppy_description gazebo.launch gui:=true paused:=true &
    GAZEBO_PID=\$!
    
    # Wait for Gazebo to initialize
    echo 'Waiting for Gazebo to initialize (15 seconds)...'
    sleep 15
    
    # Prompt user to unpause Gazebo
    echo ''
    echo '=============================================================='
    echo '  IMPORTANT: Gazebo is now running with simulation PAUSED     '
    echo ''
    echo '  1. WAIT until no more messages appear in the terminal       '
    echo '  2. Press the PLAY button in Gazebo UI                       '
    echo '  3. Press ENTER in this terminal to continue                 '
    echo '=============================================================='
    echo ''
    
    read -p 'Press ENTER after clicking PLAY in Gazebo...' -r
    
    # Unpause physics (redundant but just in case)
    rosservice call /gazebo/unpause_physics || true
    
    # Launch the velocity walker
    echo 'Starting velocity walker...'
    roslaunch puppy_description just_walker.launch &
    WALKER_PID=\$!
    
    # Wait for velocity walker to initialize
    echo 'Waiting for velocity walker to initialize (15 seconds)...'
    sleep 15
    
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