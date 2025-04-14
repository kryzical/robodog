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

# Install Python launch files
install(DIRECTORY
  launch/
  DESTINATION share/${PROJECT_NAME}
)

# Install other resource directories (URDF, meshes, config, SDF)
install(DIRECTORY
  urdf/
  meshes/
  config/
  sdf/
  DESTINATION share/${PROJECT_NAME}
)

ament_package() 