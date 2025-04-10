# Build arguments
ARG GAZEBO_VERSION=fortress

# Builder stage
FROM osrf/ros:humble-desktop-full as builder

# Install build dependencies
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
    wget \
    xorg-dev \
    mesa-utils \
    libgl1-mesa-glx \
    libgl1-mesa-dri \
    && rm -rf /var/lib/apt/lists/*

# Set up workspace
WORKDIR /workspace

# Copy the ROS workspace
COPY puppy_ros2_ws /workspace

# Build workspace
RUN . /opt/ros/humble/setup.sh && \
    cd /workspace && \
    colcon build --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=Release || (echo "Build failed" && exit 1)

# Runtime stage
FROM osrf/ros:humble-desktop-full

# Install runtime dependencies
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

# Copy built artifacts from builder
COPY --from=builder /workspace/install /workspace/install

# Copy only necessary runtime files
COPY puppy_ros2_ws/src/puppy_description /workspace/src/puppy_description

# Set environment variables
ENV ROS_DISTRO=humble
ENV GAZEBO_VERSION=${GAZEBO_VERSION}
ENV RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
ENV PATH="/usr/lib/gazebo-${GAZEBO_VERSION}/bin:${PATH}" 