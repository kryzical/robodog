cmake_minimum_required(VERSION 3.0.2)
project(robodog_config)

find_package(catkin REQUIRED)

catkin_package()

install(DIRECTORY config launch maps worlds
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)