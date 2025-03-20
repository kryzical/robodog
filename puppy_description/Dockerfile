FROM osrf/ros:noetic-desktop-full

# Install dependencies
RUN apt-get update && apt-get install -y \
    ros-noetic-joint-state-publisher-gui \
    ros-noetic-gazebo-ros-pkgs \
    ros-noetic-gazebo-ros-control \
    ros-noetic-ros-controllers \
    ros-noetic-controller-manager \
    ros-noetic-joint-state-controller \
    ros-noetic-position-controllers \
    ros-noetic-effort-controllers \
    ros-noetic-robot-state-publisher \
    ros-noetic-xacro \
    ros-noetic-rviz \
    python3-catkin-tools \
    && rm -rf /var/lib/apt/lists/*

# Create a catkin workspace
WORKDIR /ros_ws
RUN mkdir -p /ros_ws/src

# Copy the package into the container
COPY . /ros_ws/src/puppy_description/

# Build the workspace
WORKDIR /ros_ws
RUN /bin/bash -c "source /opt/ros/noetic/setup.bash && \
    catkin init && \
    catkin build"

# Setup entrypoint
COPY ./ros_entrypoint.sh /
RUN chmod +x /ros_entrypoint.sh
ENTRYPOINT ["/ros_entrypoint.sh"]
CMD ["bash"] 