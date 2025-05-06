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
find_package(std_msgs REQUIRED)

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

install(PROGRAMS
  puppy_control/puppy_walk_node.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME puppy_walk_node
)

# Install launch files
install(DIRECTORY
  launch
  DESTINATION share/${PROJECT_NAME}/
)

# Install config files
install(DIRECTORY
  config
  DESTINATION share/${PROJECT_NAME}/
)

# Install resource files
install(DIRECTORY
  resource
  DESTINATION share/${PROJECT_NAME}/
)

# Add tests only if explicitly requested
if(BUILD_TESTING AND DEFINED ENV{BUILD_TESTS})
  find_package(ament_lint_auto REQUIRED)
  find_package(ament_cmake_pytest REQUIRED)
  find_package(ros2_control_test_nodes REQUIRED)
  ament_lint_auto_find_test_dependencies()
  
  # Add pytest test for package dependencies and installation
  ament_add_pytest_test(test_build test/test_build.py)
endif()

ament_package() 