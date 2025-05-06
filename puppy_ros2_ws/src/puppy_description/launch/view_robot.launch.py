#!/usr/bin/env python3

import os
import xacro
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    # Declare the launch argument for the RViz config file
    rviz_config_arg = DeclareLaunchArgument(
        'rvizconfig',
        default_value=os.path.join(
            get_package_share_directory('puppy_description'), 
            'config', 
            'display.rviz'
        ),
        description='Absolute path to RViz config file'
    )

    # Get package share directory
    pkg_share = get_package_share_directory('puppy_description')

    # Construct the paths to the config and xacro files within the install space subdirs
    # default_rviz_config_path = os.path.join(pkg_share, 'config', 'display.rviz')
    default_rviz_config_path = os.path.join(pkg_share, 'rviz', 'display.rviz')
    xacro_file = os.path.join(pkg_share, 'urdf', 'puppy.urdf.xacro')

    # Re-declare the rvizconfig argument using the constructed default path
    rviz_config_arg = DeclareLaunchArgument(
        'rvizconfig',
        default_value=default_rviz_config_path,
        description='Absolute path to RViz config file'
    )

    # Ensure the xacro file exists in the install space
    if not os.path.exists(xacro_file):
        print(f"\n\nERROR: Could not find xacro file in install space at {xacro_file}\n       Please ensure the urdf directory is installed correctly via CMakeLists.txt\n\n")
        return LaunchDescription([])

    # Process the XACRO file to get the URDF
    try:
        robot_description_content = xacro.process_file(xacro_file).toxml()
    except Exception as e:
        print(f"\n\nERROR processing xacro file: {e}\n\n")
        return LaunchDescription([]) # Return empty description on error

    # Robot State Publisher Node
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'use_sim_time': False, # Not using sim time
            'robot_description': robot_description_content
        }]
    )

    # Joint State Publisher GUI Node
    joint_state_publisher_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        output='screen'
    )
    
    #attempt at making a camera node launch
    camera_node = Node(
    package='v4l2_camera',
    executable='v4l2_camera_node',
    name='v4l2_camera_node',
    output='screen',
    parameters=[{
        'video_device': '/dev/video0',
        'image_size': [640, 480],
        'camera_frame_id': 'camera_link',
        'pixel_format': 'YUYV',
        'use_sensor_data_qos': True
    }]
    )

    # RViz2 Node
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='log',
        arguments=['-d', LaunchConfiguration('rvizconfig')]
    )

    # --- Launch Description ---
    return LaunchDescription([
        rviz_config_arg,
        robot_state_publisher_node,
        joint_state_publisher_gui_node,
        rviz_node,
        camera_node
    ]) 