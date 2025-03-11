# Use the official ROS1 Noetic base image
FROM ros:noetic-ros-base

# Set shell
SHELL ["/bin/bash", "-c"]

# Set environment variables to optimize build
ENV MAKEFLAGS="-j$(nproc)" \
    CATKIN_MAKE_FLAGS="-j$(nproc)" \
    DISPLAY=:0 \
    QT_X11_NO_MITSHM=1

# Install dependencies
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    python3-catkin-tools \
    python3-osrf-pycommon \
    python3-rosdep \
    python3-pip \
    ros-noetic-gazebo-ros-control \
    ros-noetic-gazebo-ros-pkgs \
    ros-noetic-image-view \
    ros-noetic-joint-state-publisher \
    ros-noetic-joint-state-publisher-gui \
    ros-noetic-robot-state-publisher \
    ros-noetic-ros-control \
    ros-noetic-ros-controllers \
    ros-noetic-rqt-plot \
    ros-noetic-rqt-image-view \
    ros-noetic-web-video-server \
    ros-noetic-rviz \
    ros-noetic-xacro \
    ros-noetic-navigation \
    ros-noetic-map-server \
    ros-noetic-amcl \
    ros-noetic-move-base \
    ros-noetic-robot-localization \
    ros-noetic-effort-controllers \
    x11-apps \
    x11-xserver-utils \
    xauth \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install pip packages
RUN pip3 install --no-cache-dir adafruit-circuitpython-servokit

# Create catkin workspace
WORKDIR /catkin_ws/src

# Note: We'll mount the source code at runtime instead of copying it
# This makes development easier and avoids unnecessary copying

# Add ROS environment sourcing to .bashrc
RUN echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc && \
    echo "if [ -f /catkin_ws/devel/setup.bash ]; then source /catkin_ws/devel/setup.bash; fi" >> ~/.bashrc

# Create entrypoint script
RUN echo '#!/bin/bash' > /ros_entrypoint.sh && \
    echo 'set -e' >> /ros_entrypoint.sh && \
    echo 'source "/opt/ros/noetic/setup.bash"' >> /ros_entrypoint.sh && \
    echo 'if [ -f "/catkin_ws/devel/setup.bash"]; then source "/catkin_ws/devel/setup.bash"; fi' >> /ros_entrypoint.sh && \
    echo 'exec "$@"' >> /ros_entrypoint.sh && \
    chmod +x /ros_entrypoint.sh

ENTRYPOINT ["/ros_entrypoint.sh"]
CMD ["bash"]
