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
    wget \
    xorg-dev \
    mesa-utils \
    libgl1-mesa-glx \
    libgl1-mesa-dri \
    && rm -rf /var/lib/apt/lists/*

# Install Gazebo
RUN . /opt/ros/humble/setup.sh && \
    wget https://packages.osrfoundation.org/gazebo.gpg -O /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null \
    && apt-get update \
    && apt-get install -y gazebo-${GAZEBO_VERSION} \
    && rm -rf /var/lib/apt/lists/*

# Set up workspace
WORKDIR /workspace

# Copy only the ROS workspace
COPY puppy_ros2_ws /workspace

# Build workspace
RUN . /opt/ros/humble/setup.sh && \
    cd /workspace && \
    colcon build --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=Release

# Set environment variables
ENV ROS_DISTRO=humble
ENV GAZEBO_VERSION=fortress
ENV RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
ENV PATH="/usr/lib/gazebo-fortress/bin:/usr/bin:${PATH}"
ENV GAZEBO_MODEL_PATH=/workspace/src/puppy_description/models
ENV GAZEBO_RESOURCE_PATH=/workspace/src/puppy_description/worlds
ENV IGN_GAZEBO_RESOURCE_PATH=/workspace/src/puppy_description
ENV IGN_GAZEBO_SYSTEM_PLUGIN_PATH=/usr/lib/x86_64-linux-gnu/ign-gazebo-6/plugins

# Default command
CMD ["/bin/bash"] 