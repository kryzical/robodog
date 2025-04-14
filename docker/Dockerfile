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

# Copy the ROS workspace
COPY puppy_ros2_ws/src/puppy_description /workspace/puppy_ros2_ws/src/puppy_description

# Build workspace
RUN . /opt/ros/humble/setup.sh && \
    cd /workspace/puppy_ros2_ws && \
    colcon build --symlink-install --packages-select puppy_description --cmake-args -DCMAKE_BUILD_TYPE=Release && \
    . install/setup.sh

# Set environment variables
ENV ROS_DISTRO=humble
ENV GAZEBO_VERSION=fortress
ENV RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
ENV PATH="/usr/lib/gazebo-fortress/bin:/usr/bin:${PATH}"

# More flexible paths that work with volume mounts
ENV GAZEBO_MODEL_PATH="/workspace/puppy_ros2_ws/src/puppy_description/meshes:/workspace/puppy_ros2_ws/install/puppy_description/share/puppy_description/meshes"
ENV GAZEBO_RESOURCE_PATH="/workspace/puppy_ros2_ws/src/puppy_description:/workspace/puppy_ros2_ws/install/puppy_description/share/puppy_description"
# Point only to parent dirs for model:// resolution
ENV IGN_GAZEBO_RESOURCE_PATH="/workspace/puppy_ros2_ws/src:/workspace/puppy_ros2_ws/install/puppy_description/share"
ENV IGN_GAZEBO_MODEL_PATH="/workspace/puppy_ros2_ws/src:/workspace/puppy_ros2_ws/install/puppy_description/share"
ENV IGN_GAZEBO_SYSTEM_PLUGIN_PATH="/usr/lib/x86_64-linux-gnu/ign-gazebo-6/plugins"
ENV ROS_PACKAGE_PATH="/workspace/puppy_ros2_ws/install/puppy_description/share"

# Create a setup script
RUN echo 'source /opt/ros/humble/setup.bash' >> /root/.bashrc && \
    echo 'source /workspace/puppy_ros2_ws/install/setup.bash' >> /root/.bashrc && \
    echo 'export ROS_PACKAGE_PATH=/workspace/puppy_ros2_ws/install/puppy_description/share:${ROS_PACKAGE_PATH}' >> /root/.bashrc

# Default command
CMD ["/bin/bash"] 