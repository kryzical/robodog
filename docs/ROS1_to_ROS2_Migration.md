# ROS 1 to ROS 2 Migration Guide with Docker

## Overview

This document outlines the process of migrating a ROS 1 project to ROS 2 Humble using Docker containers. It provides guidance on setting up Docker for ROS 2 development, using Docker Compose for multi-container applications, and includes best practices for efficient workflows.

## ROS 1 to ROS 2 Migration Steps

### Package Structure Changes

1. **Package Format**: Update from format 2 to format 3 in package.xml
   ```xml
   <?xml version="1.0"?>
   <?xml-model href="http://download.ros.org/schema/package_format3.xsd" schematypens="http://www.w3.org/2001/XMLSchema"?>
   <package format="3">
   ```

2. **Build System**: Update CMakeLists.txt for ament_cmake
   ```cmake
   cmake_minimum_required(VERSION 3.8)
   project(my_package)
   
   # Find dependencies
   find_package(ament_cmake REQUIRED)
   find_package(rclcpp REQUIRED)
   
   # Add executables
   add_executable(my_node src/my_node.cpp)
   ament_target_dependencies(my_node rclcpp)
   
   # Install
   install(TARGETS my_node
     DESTINATION lib/${PROJECT_NAME})
   
   ament_package()
   ```

3. **Dependencies**: Update package.xml with ROS 2 dependencies
   ```xml
   <depend>rclcpp</depend>  <!-- instead of roscpp -->
   <depend>std_msgs</depend>
   ```

### Code Changes

1. **Header Changes**:
   ```cpp
   // ROS 1
   #include <ros/ros.h>
   #include <std_msgs/String.h>
   
   // ROS 2
   #include <rclcpp/rclcpp.hpp>
   #include <std_msgs/msg/string.hpp>
   ```

2. **Node Initialization**:
   ```cpp
   // ROS 1
   ros::init(argc, argv, "my_node");
   ros::NodeHandle nh;
   
   // ROS 2
   rclcpp::init(argc, argv);
   auto node = std::make_shared<rclcpp::Node>("my_node");
   ```

3. **Publishers/Subscribers**:
   ```cpp
   // ROS 1
   ros::Publisher pub = nh.advertise<std_msgs::String>("topic", 10);
   ros::Subscriber sub = nh.subscribe("topic", 10, callback);
   
   // ROS 2
   auto pub = node->create_publisher<std_msgs::msg::String>("topic", 10);
   auto sub = node->create_subscription<std_msgs::msg::String>(
     "topic", 10, std::bind(&callback, std::placeholders::_1));
   ```

4. **Python Nodes**:
   ```python
   # ROS 1
   #!/usr/bin/env python
   import rospy
   from std_msgs.msg import String
   
   # ROS 2
   #!/usr/bin/env python3
   import rclpy
   from rclpy.node import Node
   from std_msgs.msg import String
   ```

### Launch Files

1. **ROS 1 (XML)**:
   ```xml
   <launch>
     <node pkg="my_package" type="my_node" name="my_node" />
   </launch>
   ```

2. **ROS 2 (Python)**:
   ```python
   from launch import LaunchDescription
   from launch_ros.actions import Node
   
   def generate_launch_description():
       return LaunchDescription([
           Node(
               package='my_package',
               executable='my_node',
               name='my_node',
               output='screen'
           )
       ])
   ```

## Docker Setup for ROS 2

### Basic Dockerfile

```dockerfile
FROM ros:humble-ros-base

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-colcon-common-extensions \
    ros-humble-cv-bridge \
    && rm -rf /var/lib/apt/lists/*

# Create workspace
WORKDIR /ros_ws
COPY . /ros_ws/src/

# Build workspace
RUN . /opt/ros/humble/setup.sh && \
    colcon build && \
    echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc && \
    echo "source /ros_ws/install/setup.bash" >> ~/.bashrc

# Default command
CMD ["bash"]
```

### Space-Optimized Dockerfile

```dockerfile
FROM ros:humble-ros-core

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Install only essential dependencies with aggressive cleanup
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-pip \
    python3-colcon-common-extensions \
    ros-humble-cv-bridge \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /tmp/* /var/tmp/*

# Create workspace with minimal files
WORKDIR /ros_ws
COPY package_name/package.xml package_name/CMakeLists.txt /ros_ws/src/package_name/
COPY package_name/launch /ros_ws/src/package_name/launch
COPY package_name/scripts /ros_ws/src/package_name/scripts

# Build only necessary packages
RUN . /opt/ros/humble/setup.sh && \
    colcon build --symlink-install --packages-select package_name && \
    rm -rf /ros_ws/build /ros_ws/log

# Default command
CMD ["bash"]
```

## Docker Compose for ROS 2

### docker-compose.yml

```yaml
version: '3'

services:
  # Base ROS container
  ros2_base:
    build: .
    image: my_ros2_project:humble
    network_mode: host
    ipc: host
  
  # Camera node
  camera:
    extends: ros2_base
    privileged: true
    devices:
      - /dev/video0:/dev/video0
    volumes:
      - /dev/vchiq:/dev/vchiq
      - ./:/ros_ws/src
    command: bash -c "source /ros_ws/install/setup.bash && ros2 launch package_name camera.launch.py"
  
  # Visualization
  rviz:
    extends: ros2_base
    volumes:
      - ./:/ros_ws/src
      - /tmp/.X11-unix:/tmp/.X11-unix
    environment:
      - DISPLAY=${DISPLAY}
    command: bash -c "source /ros_ws/install/setup.bash && ros2 run rviz2 rviz2"

  # Development container
  dev:
    extends: ros2_base
    volumes:
      - ./:/ros_ws/src
    command: bash
```

## Docker and Docker Compose Commands

### Docker Commands

```bash
# Build an image
docker build -t my_image:tag .

# Run a container
docker run -it --rm my_image:tag

# List running containers
docker ps

# Stop all containers
docker stop $(docker ps -aq)

# Remove all containers
docker rm $(docker ps -aq)

# Clean up unused resources
docker system prune -af
```

### Docker Compose Commands

```bash
# Build services
docker-compose build

# Start services
docker-compose up

# Start specific service
docker-compose up camera

# Run in detached mode
docker-compose up -d

# Stop services
docker-compose down

# Execute command in running service
docker-compose exec camera bash
```

## Space Management Tips

1. **Clean Docker Regularly**:
   ```bash
   # Create a cleanup script (clean_docker.sh)
   docker system prune -af --volumes
   ```

2. **Optimize Dockerfile**:
   - Use smaller base images (ros:humble-ros-core instead of ros:humble-desktop)
   - Combine RUN commands to reduce layers
   - Clean apt cache in the same RUN command
   - Use multi-stage builds for complex applications

3. **Mount Source Code**:
   - Use volume mounts for development to avoid rebuilding
   - For production, copy only necessary files

4. **BuildKit Optimizations**:
   ```bash
   DOCKER_BUILDKIT=1 docker build .
   ```

## Troubleshooting

1. **Missing Dependencies**: Check if all ROS 2 dependencies are correctly listed in package.xml

2. **Build Errors**: Use `colcon build --symlink-install --packages-select your_package` to isolate package builds

3. **Node Crashes**: Check for ROS 1 API usage in your code; ROS 2 APIs are significantly different

4. **Cannot Find Package**: Ensure the package is sourced with `. install/setup.bash`

5. **Camera Issues**: For ARM devices like Raspberry Pi, ensure the correct camera packages are installed:
   ```bash
   apt-get install -y python3-picamera2 libcamera0
   ``` 