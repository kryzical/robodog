cmake_minimum_required(VERSION 3.8)
project(puppy_description)

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclpy REQUIRED)
find_package(robot_state_publisher REQUIRED)
find_package(rviz2 REQUIRED)
find_package(ros_gz_sim REQUIRED)
find_package(ros_gz_bridge REQUIRED)
find_package(xacro REQUIRED)

# Install necessary directories (URDF, meshes, launch, config, SDF)
install(DIRECTORY
  urdf
  meshes
  launch
  config
  sdf
  DESTINATION share/${PROJECT_NAME}
)

ament_package() 