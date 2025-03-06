#!/bin/bash

# Build the image
docker build -t puppy_robot -f .Dockerfile/Dockerfile .

# Run the container with volume mount
docker run -it \
    --network=host \
    --env="DISPLAY" \
    --env="QT_X11_NO_MITSHM=1" \
    --volume="$PWD:/catkin_ws/src:rw" \
    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
    puppy_robot
