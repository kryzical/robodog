# Use the official ROS1 Noetic base image
FROM ros:noetic-ros-base

# Set shell once at the beginning
SHELL ["/bin/bash", "-c"]

# Reduce layer count, but optimize apt operations
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    python3-catkin-tools \
    ros-noetic-gazebo-ros-control \
    ros-noetic-gazebo-ros-pkgs \
    ros-noetic-image-view \
    ros-noetic-joint-state-publisher \
    ros-noetic-joint-state-publisher-gui \
    ros-noetic-robot-state-publisher \
    ros-noetic-ros-control \
    ros-noetic-ros-controllers \
    ros-noetic-rqt-plot \
    ros-noetic-rviz \
    ros-noetic-xacro \
    x11-apps \
    x11-xserver-utils \
    xauth && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set environment variables for display and NVIDIA GPU support
ENV DISPLAY=:0 \
    QT_X11_NO_MITSHM=1 \
