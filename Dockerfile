FROM osrf/ros:noetic-desktop-full

# Install additional dependencies
RUN apt-get update && apt-get install -y \
    python3-tk \
    python3-pip \
    python3-catkin-tools \
    ros-noetic-joy \
    ros-noetic-rqt-console \
    ros-noetic-effort-controllers \
    ros-noetic-joint-state-controller \
    ros-noetic-position-controllers \
    ros-noetic-robot-state-publisher \
    ros-noetic-gazebo-ros-control \
    ros-noetic-gazebo-plugins \
    ros-noetic-gazebo-ros \
    ros-noetic-controller-manager \
    ros-noetic-joint-state-publisher \
    ros-noetic-joint-state-publisher-gui \
    ros-noetic-xacro \
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
RUN echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc && \
    echo "source /ros_ws/devel/setup.bash" >> ~/.bashrc

# Set up X11 forwarding for GUI applications
ENV DISPLAY=:0

# Set up Gazebo environment variables
ENV GAZEBO_MODEL_PATH=/ros_ws/src/puppy_description/models:${GAZEBO_MODEL_PATH}
ENV GAZEBO_RESOURCE_PATH=/ros_ws/src/puppy_description:${GAZEBO_RESOURCE_PATH} 