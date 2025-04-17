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

# Debug message to show install destination
message(STATUS "Installing resources to: ${CMAKE_INSTALL_PREFIX}/share/${PROJECT_NAME}")

# Install Python launch files
install(DIRECTORY launch/
  DESTINATION share/${PROJECT_NAME}/launch
)

# Install URDF files
install(DIRECTORY urdf/
  DESTINATION share/${PROJECT_NAME}/urdf
)

# Install mesh files
install(DIRECTORY meshes/
  DESTINATION share/${PROJECT_NAME}/meshes
)

# Install config files
install(DIRECTORY config/
  DESTINATION share/${PROJECT_NAME}/config
)

# Commenting out sdf as it might not exist
# install(DIRECTORY sdf/
#   DESTINATION share/${PROJECT_NAME}/sdf
# )

ament_package() 