# Use the official ROS1 Noetic base image
FROM ros:noetic-ros-base  

# Set shell once at the beginning
SHELL ["/bin/bash", "-c"]

# Install required packages including joint_state_publisher
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-catkin-tools \
    ros-noetic-gazebo-ros-pkgs \
    ros-noetic-joint-state-publisher \
    ros-noetic-robot-state-publisher \
    ros-noetic-rviz \
    ros-noetic-xacro \
    x11-apps \
    x11-xserver-utils \
    xauth \
    && rm -rf /var/lib/apt/lists/* \
    && echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc

# Set environment variables together
ENV DISPLAY=:0 \
    QT_X11_NO_MITSHM=1
