FROM ros:humble

# Install Gazebo Garden and dependencies
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

# Add Gazebo Garden repository and install
RUN wget https://packages.osrfoundation.org/gazebo.gpg -O /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null \
    && apt-get update \
    && apt-get install -y gz-garden \
    && rm -rf /var/lib/apt/lists/*

# Set Gazebo version for ROS
ENV GZ_VERSION=garden

# Set critical environment variables for mesh loading
ENV GZ_SIM_RESOURCE_PATH=/workspace/src:/workspace/models
ENV GZ_RESOURCE_PATH=/workspace/src:/workspace/models
ENV IGN_GAZEBO_RESOURCE_PATH=/workspace/src:/workspace/models
ENV IGN_FILE_PATH=/workspace/src:/workspace/models
ENV GAZEBO_MODEL_PATH=/workspace/src:/workspace/models
ENV GAZEBO_RESOURCE_PATH=/workspace/src:/workspace/models
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib/x86_64-linux-gnu/mesa:/usr/lib/x86_64-linux-gnu/mesa-egl:/usr/lib/x86_64-linux-gnu/pulseaudio
ENV MESA_LOADER_DRIVER_OVERRIDE=iris
ENV OGRE_RESOURCE_PATH=/usr/lib/x86_64-linux-gnu/OGRE-1.9.0

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

# Create display setup test script
RUN echo '#!/bin/bash\n\
echo "--- Checking graphics capabilities ---"\n\
echo "OpenGL vendor: $(glxinfo | grep \"OpenGL vendor\" || echo \"Not available\")" \n\
echo "OpenGL renderer: $(glxinfo | grep \"OpenGL renderer\" || echo \"Not available\")"\n\
echo "Checking if direct rendering is enabled: $(glxinfo | grep "direct rendering" || echo "Not available")"\n\
echo "--- Checking environment variables ---"\n\
echo "GZ_SIM_RESOURCE_PATH=$GZ_SIM_RESOURCE_PATH"\n\
echo "GZ_RESOURCE_PATH=$GZ_RESOURCE_PATH"\n\
echo "IGN_GAZEBO_RESOURCE_PATH=$IGN_GAZEBO_RESOURCE_PATH"\n\
echo "--- Checking mesh files ---"\n\
find /workspace -name "*.STL" -ls\n\
echo "--- Creating simple test model ---"\n\
mkdir -p /tmp/meshtest\n\
cat > /tmp/meshtest/model.sdf << EOF\n\
<?xml version="1.0" ?>\n\
<sdf version="1.6">\n\
  <model name="test_mesh">\n\
    <link name="link">\n\
      <visual name="visual">\n\
        <geometry>\n\
          <mesh>\n\
            <uri>file:///workspace/models/puppybot/meshes/base_link.STL</uri>\n\
            <scale>0.001 0.001 0.001</scale>\n\
          </mesh>\n\
        </geometry>\n\
        <material>\n\
          <ambient>0 0 1 1</ambient>\n\
          <diffuse>0 0 1 1</diffuse>\n\
        </material>\n\
      </visual>\n\
      <collision name="collision">\n\
        <geometry>\n\
          <box>\n\
            <size>0.1 0.1 0.1</size>\n\
          </box>\n\
        </geometry>\n\
      </collision>\n\
    </link>\n\
  </model>\n\
</sdf>\n\
EOF\n\
echo "Test model created at /tmp/meshtest/model.sdf"\n\
echo "--- Test complete ---"' > /workspace/check_graphics.sh && chmod +x /workspace/check_graphics.sh

# Build workspace
RUN /bin/bash -c "source /opt/ros/humble/setup.bash && \
    cd /workspace && \
    colcon build --symlink-install"

# Set up environment in bashrc
RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc && \
    echo "source /workspace/install/setup.bash" >> ~/.bashrc && \
    echo "export GZ_VERSION=garden" >> ~/.bashrc && \
    echo "export GZ_SIM_RESOURCE_PATH=/workspace/src:/workspace/models" >> ~/.bashrc && \
    echo "export GZ_RESOURCE_PATH=/workspace/src:/workspace/models" >> ~/.bashrc && \
    echo "export IGN_GAZEBO_RESOURCE_PATH=/workspace/src:/workspace/models" >> ~/.bashrc && \
    echo "export IGN_FILE_PATH=/workspace/src:/workspace/models" >> ~/.bashrc

# Skip the welcome screen
RUN mkdir -p ~/.gz && echo '<?xml version="1.0"?><gz><gui><plugin filename="GzScene3D" name="3D View"><gz-gui><title>3D View</title><property key="showTitleBar" type="bool">false</property><property key="state" type="string">docked</property></gz-gui></plugin><plugin filename="WorldControl" name="World control"><gz-gui><title>World control</title><property key="showTitleBar" type="bool">false</property><property key="state" type="string">docked</property></gz-gui></plugin><plugin filename="WorldStats" name="World stats"><gz-gui><title>World stats</title><property key="showTitleBar" type="bool">false</property><property key="state" type="string">docked</property></gz-gui></plugin></gz></gz>' > ~/.gz/gui.config 

# Set the command to run when container starts
CMD ["bash"] 