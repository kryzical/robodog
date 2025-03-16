# Docker Configurations

This directory contains Docker configurations for different ROS distributions used in the Puppy robot project.

## Structure

- `humble/`: Dockerfile and related files for ROS 2 Humble
  - `Dockerfile`: Multi-stage build configuration for ROS 2 Humble
  
## Building Images

To build the Humble image:

```bash
./run_ros2.sh --build
```

This will use the Dockerfile in the `.Dockerfile/humble/` directory.

## Image Details

### ROS 2 Humble (humble/Dockerfile)

This Dockerfile:
- Uses a multi-stage build for efficiency
- Builds from arm64v8/ros:humble-ros-core base image
- Includes dependencies for puppy_camera and puppypi_control packages
- Optimizes for Raspberry Pi and ARM architecture
- Includes camera and servo controller support 