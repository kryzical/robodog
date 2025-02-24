cmake_minimum_required(VERSION 2.8.3)

project(puppy_description)

find_package(catkin REQUIRED)

catkin_package()

find_package(roslaunch)

# Add scripts to the directories to install
foreach(dir config launch meshes urdf scripts)
	install(DIRECTORY ${dir}/
		DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/${dir})
endforeach(dir)

# Install Python scripts
catkin_install_python(PROGRAMS
  scripts/walking.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
