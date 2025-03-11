#!/bin/bash

# Check if DISPLAY is available
if [ -z "$DISPLAY" ]; then
    echo "No display detected. Please run this script on a system with X11."
    exit 1
fi

# Ensure X11 permissions are set (if running locally)
if xhost >/dev/null 2>&1; then
    xhost +local:root >/dev/null 2>&1
fi

# Run the container with GUI support
docker run -it --rm \
    --name ros1_noetic_viz \
    --network=host \
    --env="DISPLAY=$DISPLAY" \
    --env="QT_X11_NO_MITSHM=1" \
    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
    --env="ROS_MASTER_URI=http://localhost:11311" \
    ros1_noetic_dev \
    bash -c "source /opt/ros/noetic/setup.bash && rosrun rviz rviz"