# Build arguments
ARG GAZEBO_VERSION=fortress

FROM osrf/ros:humble-desktop-full

# Install wget first
RUN apt-get update && apt-get install -y wget && rm -rf /var/lib/apt/lists/*

# Add Gazebo repository
RUN wget https://packages.osrfoundation.org/gazebo.gpg -O /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null

# Install Gazebo
RUN . /opt/ros/humble/setup.sh && \
    apt-get update \
    && apt-get install -y gazebo-${GAZEBO_VERSION} \
    && rm -rf /var/lib/apt/lists/*

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
    ros-humble-xacro \
    ros-humble-control-msgs \
    ros-humble-controller-interface \
    ros-humble-hardware-interface \
    ros-humble-transmission-interface \
    ros-humble-ros-gz-sim \
    ros-humble-ros-gz-bridge \
    ros-humble-controller-manager \
    ros-humble-joint-state-broadcaster \
    ros-humble-position-controllers \
    ros-humble-ros2-control \
    ros-humble-ros2-controllers \
    ros-humble-gazebo-ros2-control \
    ros-humble-gz-ros2-control \
    xorg-dev \
    mesa-utils \
    libgl1-mesa-glx \
    libgl1-mesa-dri \
    python3-pyqt5 \
    python3-pyqt5.qtwebengine \
    python3-xlib \
    git \
    build-essential \
    python3-vcstool \
    && rm -rf /var/lib/apt/lists/*

# Install Gazebo and development packages
RUN . /opt/ros/humble/setup.sh && \
    apt-get update \
    && apt-get install -y \
    libgz-sim7 \
    libgz-sim7-dev \
    libgz-common5 \
    libgz-common5-dev \
    libgz-math7 \
    libgz-math7-dev \
    libgz-msgs9 \
    libgz-msgs9-dev \
    libgz-transport12 \
    libgz-transport12-dev \
    libgz-utils2 \
    libgz-utils2-dev \
    && rm -rf /var/lib/apt/lists/*

# Set up workspace
WORKDIR /workspace

# Create the workspace structure
RUN mkdir -p /workspace/puppy_ros2_ws/src

# Copy the ROS workspace source code
COPY . /workspace/puppy_ros2_ws/src

# Build workspace *inside* the image
RUN ["bash", "-c", "source /opt/ros/humble/setup.bash && cd /workspace/puppy_ros2_ws && colcon build --symlink-install"]

# Set environment variables
ENV ROS_DISTRO=humble
ENV GAZEBO_VERSION=fortress
ENV RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
ENV PATH="/usr/lib/gazebo-fortress/bin:/usr/bin:${PATH}"

# Point Gazebo/Ignition paths to the built install space and potentially copied source
ENV GAZEBO_MODEL_PATH="/workspace/puppy_ros2_ws/install/share:/workspace/puppy_ros2_ws/src"
ENV GAZEBO_RESOURCE_PATH="/workspace/puppy_ros2_ws/install/share:/workspace/puppy_ros2_ws/src"
ENV IGN_GAZEBO_RESOURCE_PATH="/workspace/puppy_ros2_ws/install/share:/workspace/puppy_ros2_ws/src"
ENV IGN_GAZEBO_MODEL_PATH="/workspace/puppy_ros2_ws/install/share:/workspace/puppy_ros2_ws/src"

# Set plugin paths for Gazebo and ROS2 control
ENV IGN_GAZEBO_SYSTEM_PLUGIN_PATH="/usr/lib/x86_64-linux-gnu/ign-gazebo-6/plugins:/opt/ros/humble/lib:/opt/ros/humble/lib/x86_64-linux-gnu"
ENV LD_LIBRARY_PATH="/opt/ros/humble/lib:/opt/ros/humble/lib/x86_64-linux-gnu"

# Append sourcing to .bashrc
RUN echo 'source /opt/ros/humble/setup.bash' >> /root/.bashrc && \
    echo 'source /workspace/puppy_ros2_ws/install/setup.bash' >> /root/.bashrc

# Default command
CMD ["/bin/bash"] 
