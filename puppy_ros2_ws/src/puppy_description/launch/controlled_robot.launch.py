#!/usr/bin/env python3

import os
import xacro
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    # Get package paths
    pkg_dir = get_package_share_directory('puppy_description')
    # Use the known absolute path for src within the container
    src_dir = '/workspace/puppy_ros2_ws/src/puppy_description'
    
    # Print debug info
    print(f"Package directory: {pkg_dir}")
    print(f"Source directory: {src_dir}")
    
    # Process the XACRO file to get the URDF
    robot_description_content = xacro.process_file(
        os.path.join(src_dir, 'urdf', 'puppy.urdf.xacro')
    ).toxml()
    
    # Set environment variables specifically for the Gazebo launch context
    # Point to the parent directories where the 'puppy_description' model folder can be found
    gazebo_model_path = SetEnvironmentVariable(
        name='IGN_GAZEBO_MODEL_PATH',
        value=f"/workspace/puppy_ros2_ws/src:/workspace/puppy_ros2_ws/install/puppy_description/share"
    )
    gazebo_resource_path = SetEnvironmentVariable(
        name='IGN_GAZEBO_RESOURCE_PATH',
        value=f"/workspace/puppy_ros2_ws/src:/workspace/puppy_ros2_ws/install/puppy_description/share"
    )
    
    # Launch Ignition Gazebo with empty world
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')
        ]),
        launch_arguments={
            'gz_args': '-r -v 4 empty.sdf',
            'on_exit_shutdown': 'true'
        }.items()
    )
    
    # Bridge (Clock is useful)
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=['/clock@rosgraph_msgs/msg/Clock[ignition.msgs.Clock'],
        output='screen'
    )
    
    # Robot State Publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'use_sim_time': True,
            'robot_description': robot_description_content
        }]
    )
    
    # Joint State Publisher (for visualization transforms)
    joint_state_publisher = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        output='screen',
        parameters=[{'use_sim_time': True}]
    )
    
    # Spawn robot entity in Gazebo
    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-topic', '/robot_description', '-entity', 'puppy'],
        output='screen'
    )

    # --- Launch Description ---
    return LaunchDescription([
        # Set Environment variables first
        gazebo_model_path,
        gazebo_resource_path,
        # Launch Gazebo
        gazebo,
        # Bridges (Clock is useful)
        bridge,
        # Robot Description and State Publisher (Needed for TF and visual links)
        robot_state_publisher,
        joint_state_publisher,
        # Spawn Robot
        spawn_entity,
        # --- Controllers Removed ---
    ]) 