cmake_minimum_required(VERSION 3.0.2)
project(robodog_gazebo)

find_package(catkin REQUIRED COMPONENTS
  gazebo_ros
  gazebo_ros_control
  robodog_description
  robodog_msgs
  roscpp
  sensor_msgs
)

find_package(gazebo REQUIRED)

catkin_package(
  CATKIN_DEPENDS 
    gazebo_ros
    gazebo_ros_control
    robodog_description
    robodog_msgs
    roscpp
    sensor_msgs
)

include_directories(
  ${catkin_INCLUDE_DIRS}
  ${GAZEBO_INCLUDE_DIRS}
)

link_directories(${GAZEBO_LIBRARY_DIRS})

add_library(contact_sensor src/contact_sensor.cpp)
target_link_libraries(contact_sensor ${catkin_LIBRARIES} ${GAZEBO_LIBRARIES})

install(DIRECTORY launch worlds
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)