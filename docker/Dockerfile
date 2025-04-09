FROM ros:humble-ros-base

# Install Gazebo Fortress and dependencies
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    gnupg \
    lsb-release \
    libgl1-mesa-glx \
    libgl1-mesa-dri \
    ros-humble-ros-gz \
    ros-humble-ros-gz-sim \
    ros-humble-xacro \
    ros-humble-robot-state-publisher \
    ros-humble-joint-state-publisher \
    ros-humble-controller-manager \
    ros-humble-gazebo-ros2-control \
    ros-humble-ros2-control \
    ros-humble-ros2-controllers \
    # Extra packages for mesh loading
    libogre-1.9-dev \
    libassimp-dev \
    libavcodec-dev \
    libavdevice-dev \
    libavformat-dev \
    libavutil-dev \
    libswscale-dev \
    && rm -rf /var/lib/apt/lists/*

# Add Gazebo Fortress repository and install
RUN wget https://packages.osrfoundation.org/gazebo.gpg -O /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null \
    && apt-get update \
    && apt-get install -y gz-fortress \
    && rm -rf /var/lib/apt/lists/*

# Set up workspace
WORKDIR /workspace
RUN mkdir -p /workspace/src /workspace/models

# Copy project files
COPY puppy_ros2_ws/src /workspace/src

# Set up the models directory for easier access
WORKDIR /workspace/models
RUN mkdir -p puppybot/meshes

# Ensure access to the meshes by creating a symbolic link
RUN cd /workspace/models/puppybot/meshes && \
    if [ -d /workspace/src/puppy_description/meshes ]; then \
    ln -s /workspace/src/puppy_description/meshes/* .; \
    fi

# Fix STL files permissions just in case
RUN find /workspace -name "*.STL" -exec chmod 644 {} \; || true

# Return to workspace directory
WORKDIR /workspace

# Build workspace
RUN /bin/bash -c "source /opt/ros/humble/setup.bash && \
    cd /workspace && \
    colcon build --symlink-install"

# Set up environment in bashrc
RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc && \
    echo "source /workspace/install/setup.bash" >> ~/.bashrc && \
    echo "export GZ_VERSION=fortress" >> ~/.bashrc && \
    echo "export GZ_SIM_RESOURCE_PATH=/workspace/src:/workspace/models" >> ~/.bashrc && \
    echo "export GZ_RESOURCE_PATH=/workspace/src:/workspace/models" >> ~/.bashrc && \
    echo "export IGN_GAZEBO_RESOURCE_PATH=/workspace/src:/workspace/models" >> ~/.bashrc && \
    echo "export IGN_FILE_PATH=/workspace/src:/workspace/models" >> ~/.bashrc

# Skip the welcome screen
RUN mkdir -p ~/.gz && echo '<?xml version="1.0"?><gz><gui><plugin filename="GzScene3D" name="3D View"><gz-gui><title>3D View</title><property key="showTitleBar" type="bool">false</property><property key="state" type="string">docked</property></gz-gui></plugin><plugin filename="WorldControl" name="World control"><gz-gui><title>World control</title><property key="showTitleBar" type="bool">false</property><property key="state" type="string">docked</property></gz-gui></plugin><plugin filename="WorldStats" name="World stats"><gz-gui><title>World stats</title><property key="showTitleBar" type="bool">false</property><property key="state" type="string">docked</property></gz-gui></plugin></gz></gz>' > ~/.gz/gui.config

# Set the command to run when container starts
CMD ["/startup.sh"] 