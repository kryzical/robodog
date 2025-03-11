#!/bin/bash

# Set ROS networking environment variables
HOST_IP="192.168.5.40"

# Give access to all video devices
VIDEO_DEVICES=""
for device in /dev/video*; do
    VIDEO_DEVICES="$VIDEO_DEVICES --device=$device:$device"
done

# X11 forwarding setup
XSOCK=/tmp/.X11-unix
XAUTH=/tmp/.docker.xauth
touch $XAUTH
xauth nlist $DISPLAY | sed -e 's/^..../ffff/' | xauth -f $XAUTH nmerge -

docker run -it --rm \
    --name ros1_noetic_dev \
    --network=host \
    --env="ROS_IP=${HOST_IP}" \
    --env="ROS_HOSTNAME=${HOST_IP}" \
    --env="ROS_MASTER_URI=http://${HOST_IP}:11311" \
    --env="DISPLAY=$DISPLAY" \
    --env="XAUTHORITY=$XAUTH" \
    --volume=$XSOCK:$XSOCK:rw \
    --volume=$XAUTH:$XAUTH:rw \
    --volume="$PWD:/catkin_ws/src:rw" \
    $VIDEO_DEVICES \
    --group-add video \
    --privileged \
    ros1_noetic_dev
