# Build arguments
ARG GAZEBO_VERSION=fortress

FROM osrf/ros:humble-desktop-full

# Install all necessary dependencies
RUN . /opt/ros/humble/setup.sh && \
    apt-get update && apt-get install -y \
    cmake \
    curl \
    libglu1-mesa-dev \
    python3-pip \
    python3-pydantic \
    python3-rosdep \
    python3-colcon-common-extensions \
    ros-humble-gazebo-ros \
    ros-humble-gazebo-ros-pkgs \
    ros-humble-joint-state-publisher \
    ros-humble-joint-state-publisher-gui \
    ros-humble-robot-localization \
    ros-humble-robot-state-publisher \
    ros-humble-ros2bag \
    ros-humble-rosbag2-storage-default-plugins \
    ros-humble-rmw-fastrtps-cpp \
    ros-humble-rmw-cyclonedds-cpp \
    ros-humble-ros-gz-sim \
    ros-humble-ros-gz-bridge \
    ros-humble-controller-manager \
    ros-humble-ros2-control \
    ros-humble-ros2-controllers \
    ros-humble-gazebo-ros2-control \
    ros-humble-xacro \
    wget \
    xorg-dev \
    mesa-utils \
    libgl1-mesa-glx \
    libgl1-mesa-dri \
    && rm -rf /var/lib/apt/lists/*
#install pygame
RUN pip3 install pygame
RUN pip3 install adafruit-circuitpython-servokit

# Install Gazebo
RUN . /opt/ros/humble/setup.sh && \
    wget https://packages.osrfoundation.org/gazebo.gpg -O /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null \
    && apt-get update \
    && apt-get install -y gazebo-${GAZEBO_VERSION} \
    && rm -rf /var/lib/apt/lists/*

# Set up workspace
WORKDIR /workspace

# Create the workspace structure
RUN mkdir -p /workspace/puppy_ros2_ws/src

# Copy the ROS workspace source code
# Build context is assumed to be the robodog directory
COPY . /workspace/puppy_ros2_ws/src

# Build workspace *inside* the image
RUN ["bash", "-c", "source /opt/ros/humble/setup.bash && cd /workspace/puppy_ros2_ws && colcon build --symlink-install"]

# Set environment variables (Ensure ROS_PACKAGE_PATH points to install space)
ENV ROS_DISTRO=humble
ENV GAZEBO_VERSION=fortress
ENV RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
ENV PATH="/usr/lib/gazebo-fortress/bin:/usr/bin:${PATH}"
# Point Gazebo/Ignition paths to the built install space and potentially copied source
# General paths for install and source space
ENV GAZEBO_MODEL_PATH="/workspace/puppy_ros2_ws/install/share:/workspace/puppy_ros2_ws/src"
ENV GAZEBO_RESOURCE_PATH="/workspace/puppy_ros2_ws/install/share:/workspace/puppy_ros2_ws/src"
ENV IGN_GAZEBO_RESOURCE_PATH="/workspace/puppy_ros2_ws/install/share:/workspace/puppy_ros2_ws/src"
ENV IGN_GAZEBO_MODEL_PATH="/workspace/puppy_ros2_ws/install/share:/workspace/puppy_ros2_ws/src"
ENV IGN_GAZEBO_SYSTEM_PLUGIN_PATH="/usr/lib/x86_64-linux-gnu/ign-gazebo-6/plugins"
# ROS_PACKAGE_PATH is generally not needed/set explicitly in ROS 2; sourcing install/setup.bash handles discovery.

# Append sourcing to .bashrc (sources the built workspace)
RUN echo 'source /opt/ros/humble/setup.bash' >> /root/.bashrc && \
    echo 'source /workspace/puppy_ros2_ws/install/setup.bash' >> /root/.bashrc
# Removed explicit ROS_PACKAGE_PATH export

# Default command
CMD ["/bin/bash"] 