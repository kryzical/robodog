#!/bin/bash

#=======================================
# PuppyPi Robot - Master Control Script
#=======================================

# Display help information
function show_help {
  echo "PuppyPi Robot Control"
  echo "Usage: ./puppypi.sh [command]"
  echo ""
  echo "Commands:"
  echo "  start    - Start the robot environment and controller"
  echo "  stop     - Stop the robot environment"
  echo "  restart  - Restart the robot environment"
  echo "  status   - Show status of the robot environment"
  echo "  help     - Show this help message"
}

# Check the status of the container
function check_status {
  echo "PuppyPi Robot Status:"
  
  # Check if container is running
  if docker ps | grep -q puppy_ros_dev_gazebo; then
    echo "✅ Docker container: RUNNING"
    
    # Check if controller is running
    if docker exec puppy_ros_dev_gazebo bash -c "ps aux | grep -v grep | grep -q spot_style_controller.py"; then
      echo "✅ Spot Controller: RUNNING"
    else
      echo "❌ Spot Controller: NOT RUNNING"
    fi
    
    # Check if UI is running
    if docker exec puppy_ros_dev_gazebo bash -c "ps aux | grep -v grep | grep -q controller.py"; then
      echo "✅ Joystick UI: RUNNING"
    else
      echo "❌ Joystick UI: NOT RUNNING"
    fi
    
    # Check ROS topics
    echo -e "\nROS Topics:"
    docker exec -it puppy_ros_dev_gazebo bash -c "source /opt/ros/noetic/setup.bash && source /workspace/devel/setup.bash && rostopic list | grep -E 'joy|cmd_vel|joint'"
  else
    echo "❌ Docker container: NOT RUNNING"
  fi
}

# Start the robot
function start_robot {
  echo "Starting PuppyPi robot environment..."
  
  # Check if container is already running
  if docker ps | grep -q puppy_ros_dev_gazebo; then
    echo "Container is already running."
  else
    echo "Starting Docker container..."
    docker-compose up -d
    echo "Waiting for container to initialize..."
    sleep 10
  fi
  
  # Launch the controller and UI
  echo "Starting controller and UI..."
  bash ./scripts/run_controller.sh
}

# Stop the robot
function stop_robot {
  echo "Stopping PuppyPi robot environment..."
  
  # Stop any running controller processes
  if docker ps | grep -q puppy_ros_dev_gazebo; then
    echo "Stopping controller processes..."
    docker exec -it puppy_ros_dev_gazebo bash -c "pkill -f spot_style_controller.py || true"
    docker exec -it puppy_ros_dev_gazebo bash -c "pkill -f controller.py || true"
    
    # Stop the container
    echo "Stopping Docker container..."
    docker-compose down
  else
    echo "Container is not running."
  fi
}

# Restart the robot
function restart_robot {
  echo "Restarting PuppyPi robot environment..."
  
  # Full stop of all components
  stop_robot
  
  # Wait a moment for everything to completely stop
  echo "Waiting for all processes to stop..."
  sleep 5
  
  # Start everything fresh
  start_robot
}

# Check if argument is provided
if [ $# -eq 0 ]; then
  show_help
  exit 0
fi

# Process the command
case "$1" in
  start)
    start_robot
    ;;
  stop)
    stop_robot
    ;;
  restart)
    restart_robot
    ;;
  status)
    check_status
    ;;
  help|--help|-h)
    show_help
    ;;
  *)
    echo "Invalid command: $1"
    show_help
    exit 1
    ;;
esac

exit 0 