# Use the official ROS1 Noetic base image
FROM ros:noetic-ros-base  

# Set shell once at the beginning
SHELL ["/bin/bash", "-c"]

# # Install curl to enable fetching remote resources
# RUN apt-get update && apt-get install -y curl

# # Add NVIDIA Docker repository for Ubuntu 20.04 (adjust if using a different distro)
# RUN distribution=$(. /etc/os-release; echo $ID$VERSION_ID) && \
#     curl -fsSL https://nvidia.github.io/nvidia-docker/gpgkey | apt-key add - && \
#     curl -fsSL https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | tee /etc/apt/sources.list.d/nvidia-docker.list && \
#     apt-get update && \
#     apt-get install -y nvidia-container-toolkit && \
#     rm -rf /var/lib/apt/lists/*

# OPTIONAL: Uncomment for AMD (ROCm) support installation
# RUN apt-get update && apt-get install -y --no-install-recommends \
#    rocm-dkms \
#    rocm-dev && \
#    rm -rf /var/lib/apt/lists/*
# ENV ROCM_VISIBLE_DEVICES=all

# Install required packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-catkin-tools \
    ros-noetic-gazebo-ros-pkgs \
    ros-noetic-joint-state-publisher \
    ros-noetic-joint-state-publisher-gui \
    ros-noetic-robot-state-publisher \
    ros-noetic-rviz \
    ros-noetic-image-view \
    ros-noetic-xacro \
    ros-noetic-ros-control \
    ros-noetic-ros-controllers \
    ros-noetic-gazebo-ros-control \
    x11-apps \
    x11-xserver-utils \
    xauth \
    && rm -rf /var/lib/apt/lists/* \
    && echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc

# Set environment variables for display and NVIDIA GPU support.
# For AMD GPUs (with ROCm) the environment variable ROCM_VISIBLE_DEVICES (if set in the optional section) is used.
ENV DISPLAY=:0 \
    QT_X11_NO_MITSHM=1 \
    NVIDIA_VISIBLE_DEVICES=all \
    NVIDIA_DRIVER_CAPABILITIES=all
