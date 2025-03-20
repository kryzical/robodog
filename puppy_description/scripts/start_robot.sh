#!/bin/bash

# Kill any existing containers and processes
echo "Cleaning up existing containers..."
docker ps -a | grep puppy | awk '{print $1}' | xargs -r docker rm -f
pkill -f "roslaunch puppy_description gazebo.launch"
pkill -f roscore

# Start ROS master
echo "Starting ROS master..."
docker run -d --rm --name puppy_ros_master \
    --env="ROS_MASTER_URI=http://localhost:11311" \
    --network=host \
    puppy_description_puppy_ros_test \
    bash -c "source /opt/ros/noetic/setup.bash && roscore"

# Wait for ROS master to be ready
echo "Waiting for ROS master..."
sleep 3

# Start Gazebo with robot
echo "Starting Gazebo with robot..."
docker run -d --rm --name puppy_ros_noetic \
    --env="DISPLAY" \
    --env="QT_X11_NO_MITSHM=1" \
    --env="ROS_MASTER_URI=http://localhost:11311" \
    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
    --volume="$(pwd)/robodog/puppy_description:/ros_ws/src/puppy_description:delegated" \
    --privileged \
    --network=host \
    puppy_description_puppy_ros_test \
    bash -c "source /opt/ros/noetic/setup.bash && cd /ros_ws && source devel/setup.bash && roslaunch puppy_description gazebo.launch"

# Wait for Gazebo to start
echo "Waiting for Gazebo to start..."
sleep 5

# Start movement test
echo "Starting movement test..."
docker exec -it puppy_ros_noetic \
    bash -c "source /opt/ros/noetic/setup.bash && cd /ros_ws && source devel/setup.bash && cd src/puppy_description/scripts && python3 movement_test.py"

# Cleanup on exit
trap "docker ps -a | grep puppy | awk '{print \$1}' | xargs -r docker rm -f; pkill -f 'roslaunch puppy_description gazebo.launch'; pkill -f roscore" EXIT 