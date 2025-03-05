cmake_minimum_required(VERSION 3.0.2)
project(robodog_msgs)

find_package(catkin REQUIRED COMPONENTS
  message_generation
  std_msgs
  geometry_msgs
  sensor_msgs
)

add_message_files(
  FILES
  Contacts.msg
  ContactsStamped.msg
  Joints.msg
  Point.msg
  PointArray.msg
  Pose.msg
  Velocities.msg
)

generate_messages(
  DEPENDENCIES
  std_msgs
  geometry_msgs
)

catkin_package(
  CATKIN_DEPENDS message_runtime std_msgs geometry_msgs sensor_msgs
)