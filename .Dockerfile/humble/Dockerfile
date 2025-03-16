# syntax=docker/dockerfile:1.4

# Use the minimal base image
FROM arm64v8/ros:humble-ros-core

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Install only essential dependencies in a single layer with aggressive cleanup
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-pip \
    python3-opencv \
    ros-humble-cv-bridge \
    ros-humble-image-transport \
    ros-humble-compressed-image-transport \
    ros-humble-rqt-image-view \
    python3-numpy \
    python3-prctl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /tmp/* /var/tmp/*

# Create minimal workspace
WORKDIR /ros_ws
COPY --chmod=755 puppy_camera/scripts/camera_publisher.py /ros_ws/src/puppy_camera/scripts/
COPY puppy_camera/package.xml puppy_camera/CMakeLists.txt /ros_ws/src/puppy_camera/
COPY puppy_camera/launch /ros_ws/src/puppy_camera/launch

# Create Python package directory
RUN mkdir -p /ros_ws/src/puppy_camera/puppy_camera && \
    echo "# placeholder" > /ros_ws/src/puppy_camera/puppy_camera/__init__.py

# Build only what's needed
RUN . /opt/ros/humble/setup.sh && \
    colcon build --symlink-install --packages-select puppy_camera && \
    rm -rf /ros_ws/build /ros_ws/log && \
    echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc && \
    echo "source /ros_ws/install/setup.bash" >> ~/.bashrc

# Default command
CMD ["bash"]