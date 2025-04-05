#!/bin/bash

# Allow X server connection
xhost + local:docker || true

# Launch Gazebo in a container
