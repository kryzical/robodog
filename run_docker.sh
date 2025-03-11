#!/bin/bash

# Build the image
docker build -t puppy_robot -f Dockerfile .

# Run the container with volume mount
docker run -it --rm \
    --name ros1_noetic_dev \
    --network=host \
    --env="DISPLAY" \
    --env="QT_X11_NO_MITSHM=1" \
    --volume="$PWD:/catkin_ws/src:rw" \
    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
    --privileged \
    puppy_robot
