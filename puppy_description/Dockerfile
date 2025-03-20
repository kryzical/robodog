FROM osrf/ros:noetic-desktop-full

# Install additional ROS packages
RUN apt-get update && apt-get install -y \
    ros-noetic-joint-state-publisher-gui \
    ros-noetic-effort-controllers \
    ros-noetic-gazebo-ros-control \
    ros-noetic-joint-state-controller \
    ros-noetic-position-controllers \
    ros-noetic-robot-state-publisher \
    ros-noetic-controller-manager \
    python3-catkin-tools \
    && rm -rf /var/lib/apt/lists/*

# Create workspace
WORKDIR /ros_ws
RUN mkdir -p /ros_ws/src

# Copy package files
COPY . /ros_ws/src/puppy_description/

# Build workspace
WORKDIR /ros_ws
RUN /bin/bash -c "source /opt/ros/noetic/setup.bash && \
    rm -rf build devel && \
    catkin_make"

# Copy and set entrypoint
COPY ./ros_entrypoint.sh /
RUN chmod +x /ros_entrypoint.sh

# Set display environment variable
ENV DISPLAY=:0

# Set entry point
ENTRYPOINT ["/ros_entrypoint.sh"]
CMD ["bash"] 