FROM ros:noetic

# Install required packages
RUN apt-get update && apt-get install -y \
    ros-noetic-desktop-full \
    ros-noetic-gazebo-ros-control \
    ros-noetic-ros-control \
    ros-noetic-ros-controllers \
    ros-noetic-joint-state-controller \
    ros-noetic-effort-controllers \
    ros-noetic-position-controllers \
    ros-noetic-joy \
    python3-catkin-tools \
    python3-pyqt5 \
    joystick \
    && rm -rf /var/lib/apt/lists/*

# Create workspace directory
WORKDIR /ros_ws

# Add workspace setup to bashrc
RUN echo "source /opt/ros/noetic/setup.bash" >> /root/.bashrc && \
    echo "cd /ros_ws" >> /root/.bashrc && \
    echo "if [ -f /ros_ws/devel/setup.bash ]; then source /ros_ws/devel/setup.bash; fi" >> /root/.bashrc

# Copy the ros_entrypoint.sh script
COPY docker/ros_entrypoint.sh /ros_entrypoint.sh
RUN chmod +x /ros_entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["/ros_entrypoint.sh"]
CMD ["bash"] 