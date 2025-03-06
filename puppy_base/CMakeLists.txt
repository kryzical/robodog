cmake_minimum_required(VERSION 3.0.2)
project(puppy_base)

find_package(catkin REQUIRED)

catkin_package()

include_directories(
  ${catkin_INCLUDE_DIRS}
)

install(DIRECTORY launch scripts config
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)