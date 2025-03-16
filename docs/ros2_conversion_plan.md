# ROS 2 Conversion Plan

## Current Status
- The project is currently using ROS 1 (catkin build system, XML launch files)
- Need to convert to ROS 2 (ament build system, Python launch files)

## Package Conversion Steps

### 1. puppy_gazebo Package

#### package.xml
- Change format from "2" to "3"
- Replace `<buildtool_depend>catkin</buildtool_depend>` with `<buildtool_depend>ament_cmake</buildtool_depend>`
- Update dependencies:
  - gazebo_ros → ros2 version (gazebo_ros)
  - gazebo_ros_control → ros2 version (gazebo_ros_pkgs)
  - roscpp → rclcpp
  - Add necessary ROS 2 dependencies (rclcpp, ament_cmake, etc.)
- Update exec_depends:
  - roslaunch → ros2launch
  - controller_manager → ros2_control
  - joint_state_controller → joint_state_broadcaster
  - Add ros2 specific dependencies

#### CMakeLists.txt
- Update to ament_cmake
- Replace catkin_package() with ament_package()
- Update find_package() calls for ROS 2
- Update install paths for ROS 2 style

#### Launch files
- Convert XML launch files to Python format
- Update package references and namespaces
- Replace launch tags with Python launch API
- Update service and node spawning to use ROS 2 equivalents

### 2. puppy_description Package

#### package.xml
- Update to format="3"
- Replace catkin with ament_cmake
- Update dependencies for ROS 2

#### CMakeLists.txt
- Update to ament_cmake build system
- Update install rules for ROS 2

#### URDF/XACRO
- Update ROS 1 specific tags to ROS 2 equivalents
- Update ROS controllers to ros2_control format

### 3. Other Packages

Similarly update:
- puppy_msgs
- puppy_navigation
- puppy_base
- puppy_bringup

## Testing Strategy

1. First convert core packages (description, msgs)
2. Then convert simulation (gazebo)
3. Finally convert operation packages (navigation, bringup)
4. Test each stage before proceeding

## Implementation Order

1. Start with simple package conversion (puppy_msgs)
2. Then convert puppy_description for robot model
3. Convert puppy_gazebo for simulation
4. Finally convert navigation and other packages

## Special Considerations

1. ros2_control is different from ros_control in ROS 1
2. Navigation stack uses different APIs in ROS 2
3. Launch files syntax is completely different
4. Parameters handling is different in ROS 2 