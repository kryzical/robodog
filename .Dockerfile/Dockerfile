# Use the official ROS1 Noetic base image
FROM ros:noetic

# Install necessary packages
RUN apt-get update && apt-get install -y \
    python3-catkin-tools \
    ros-noetic-xacro \
    ros-noetic-robot-state-publisher \
    ros-noetic-rviz \
    ros-noetic-gazebo-ros-pkgs \
    x11-apps \
    x11-xserver-utils \
    xauth \
    # ...other dependencies... \
    && rm -rf /var/lib/apt/lists/*  # Clean up to reduce image size

# Set up the ROS1 environment
SHELL ["/bin/bash", "-c"]

RUN echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc

# Set up environment variables for X11 forwarding
ENV DISPLAY=:0
ENV QT_X11_NO_MITSHM=1

# Set the working directory
WORKDIR /catkin_ws

# Copy the source code
COPY . /catkin_ws/src

# Build the workspace
RUN /bin/bash -c "source /opt/ros/noetic/setup.bash && catkin_make"