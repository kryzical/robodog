cmake_minimum_required(VERSION 3.0.2)
project(robodog_base)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  geometry_msgs
  sensor_msgs
  nav_msgs
  visualization_msgs
  tf2_ros
  robodog_msgs
  robot_localization
)

catkin_package(
  INCLUDE_DIRS include
  LIBRARIES ${PROJECT_NAME}
  CATKIN_DEPENDS 
    roscpp 
    rospy
    geometry_msgs 
    sensor_msgs 
    nav_msgs 
    visualization_msgs
    tf2_ros 
    robodog_msgs
    robot_localization
)

include_directories(
  include
  ${catkin_INCLUDE_DIRS}
)

add_library(${PROJECT_NAME}
  src/quadruped_controller.cpp
  src/state_estimation.cpp
  src/message_relay.cpp
)

add_dependencies(${PROJECT_NAME}
  ${${PROJECT_NAME}_EXPORTED_TARGETS}
  ${catkin_EXPORTED_TARGETS}
)

target_link_libraries(${PROJECT_NAME}
  ${catkin_LIBRARIES}
)

add_executable(quadruped_controller_node src/quadruped_controller_node.cpp)
target_link_libraries(quadruped_controller_node
  ${PROJECT_NAME}
  ${catkin_LIBRARIES}
)

add_executable(state_estimation_node src/state_estimation_node.cpp)
target_link_libraries(state_estimation_node
  ${PROJECT_NAME}
  ${catkin_LIBRARIES}
)

add_executable(message_relay_node src/message_relay_node.cpp)
target_link_libraries(message_relay_node
  ${PROJECT_NAME}
  ${catkin_LIBRARIES}
)