FROM osrf/ros:noetic-desktop-full

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-catkin-tools \
    ros-noetic-joint-state-publisher \
    ros-noetic-robot-state-publisher \
    ros-noetic-gazebo-ros \
    ros-noetic-gazebo-ros-control \
    ros-noetic-ros-control \
    ros-noetic-ros-controllers \
    ros-noetic-joy \
    ros-noetic-robot-localization \
    ros-noetic-vision-opencv \
    ros-noetic-cv-bridge \
    ros-noetic-image-transport \
    ros-noetic-effort-controllers \
    ros-noetic-joint-trajectory-controller \
    ros-noetic-position-controllers \
    ros-noetic-velocity-controllers \
    ros-noetic-teleop-twist-joy \
    ros-noetic-tf2-ros \
    ros-noetic-move-base \
    ros-noetic-map-server \
    ros-noetic-amcl \
    python3-opencv \
    && rm -rf /var/lib/apt/lists/*

# Additional Python packages
RUN pip3 install numpy scipy transforms3d

# Create workspace directory
WORKDIR /workspace

CMD ["/bin/bash"]
