cmake_minimum_required(VERSION 3.8)
project(puppy_control)

# Default to C++14
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(rclpy REQUIRED)
find_package(control_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(controller_manager REQUIRED)
find_package(position_controllers REQUIRED)
find_package(joint_state_broadcaster REQUIRED)
find_package(ros2_control REQUIRED)
find_package(hardware_interface REQUIRED)

# Install Python modules
ament_python_install_package(${PROJECT_NAME})

# Install Python executables
install(PROGRAMS
  puppy_control/puppy_motion_node.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME puppy_motion_node
)

install(PROGRAMS
  puppy_control/stand_command.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME stand_command
)

# Install launch files
install(DIRECTORY
  launch
  config
  DESTINATION share/${PROJECT_NAME}/
)

ament_package() 