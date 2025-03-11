#!/bin/bash

# Get the Raspberry Pi's IP address
HOST_IP=$(hostname -I | awk '{print $1}')

# Give access to all video devices
VIDEO_DEVICES=""
for device in /dev/video*; do
    VIDEO_DEVICES="$VIDEO_DEVICES --device=$device:$device"
done

# Run the container with video devices and ROS networking
docker run -it --rm \
    --name ros1_noetic_camera \
    --network=host \
    --env="ROS_IP=${HOST_IP}" \
    --env="ROS_HOSTNAME=${HOST_IP}" \
    --env="ROS_MASTER_URI=http://${HOST_IP}:11311" \
    --volume="$(pwd):/catkin_ws/src:rw" \
    $VIDEO_DEVICES \
    --group-add video \
    --privileged \
    ros1_noetic_dev \
    bash -c "source /opt/ros/noetic/setup.bash && roslaunch puppy_camera core.launch ros_ip:=${HOST_IP}"