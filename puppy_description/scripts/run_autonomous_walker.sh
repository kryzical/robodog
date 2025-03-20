#!/bin/bash

# Generate a unique container name using timestamp
CONTAINER_ID="puppy_walker_$(date +%Y%m%d_%H%M%S)"
echo "Starting PuppyPi autonomous walker in container: $CONTAINER_ID"

# Get the absolute path of the directory containing this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Run the container with the unique name
docker run \
  --name $CONTAINER_ID \
  --rm \
  -it \
  -e "DISPLAY=$DISPLAY" \
  -e "QT_X11_NO_MITSHM=1" \
  -v "/tmp/.X11-unix:/tmp/.X11-unix:rw" \
  -v "$PROJECT_DIR:/home/puppy_ws/src/puppy_description" \
  --network=host \
  --privileged \
  puppy_description:latest \
  bash -c "cd /home/puppy_ws && \
           source /opt/ros/noetic/setup.bash && \
           source devel/setup.bash && \
           echo 'Launching Gazebo with PuppyPi...' && \
           roslaunch puppy_description gazebo.launch & \
           echo 'Waiting for Gazebo to initialize...' && \
           sleep 10 && \
           echo 'Starting autonomous walker...' && \
           python3 /home/puppy_ws/src/puppy_description/scripts/autonomous_walker.py"

echo "Walker container $CONTAINER_ID has finished execution"