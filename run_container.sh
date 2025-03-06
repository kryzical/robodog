#!/bin/bash

docker run -it --rm \
    --name puppy_robot_container \
    --network=host \
    --env="DISPLAY" \
    --env="QT_X11_NO_MITSHM=1" \
    --volume="$PWD:/catkin_ws/src:rw" \
    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
    --privileged \
    puppy_robot
