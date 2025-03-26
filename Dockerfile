FROM osrf/ros:noetic-desktop-full

# Install additional dependencies
RUN apt-get update && apt-get install -y \
    python3-tk \
    python3-pip \
    python3-catkin-tools \
    ros-noetic-joy \
    ros-noetic-rqt-console \
    ros-noetic-effort-controllers \
    && rm -rf /var/lib/apt/lists/*

# Create workspace directory
RUN mkdir -p /ros_ws/src

# Set working directory
WORKDIR /ros_ws

# Initialize catkin workspace
RUN . /opt/ros/noetic/setup.sh && \
    catkin init && \
    catkin config --extend /opt/ros/noetic

# Source ROS environment in bashrc
RUN echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc 