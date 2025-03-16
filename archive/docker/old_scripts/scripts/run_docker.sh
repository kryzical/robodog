#!/bin/bash

# Build the Docker image
docker build -t puppy_camera .

# Run the container with device access and network
docker run -it \
    --network host \
    --device=/dev/video0:/dev/video0 \
    --device=/dev/vchiq:/dev/vchiq \
    --volume="$HOME/.Xauthority:/root/.Xauthority:rw" \
    --env="DISPLAY" \
    --name puppy_camera \
    puppy_camera
