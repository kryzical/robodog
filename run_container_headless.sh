#!/bin/bash
# Run the container in headless mode (no GUI needed)
docker run -it --rm \
    --name ros1_noetic_dev \
    --network=host \
    --volume="$PWD:/catkin_ws/src:rw" \
    --privileged \
    --env="ROS_IP=$(hostname -I | awk '{print $1}')" \
    --env="ROS_HOSTNAME=$(hostname -I | awk '{print $1}')" \
    ros1_noetic_dev