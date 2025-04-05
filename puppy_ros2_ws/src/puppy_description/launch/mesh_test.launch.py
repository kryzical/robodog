#!/usr/bin/env python3

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    # Launch Gazebo with empty world
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')
        ]),
        launch_arguments={'gz_args': '-r empty.sdf'}.items()
    )
    
    # Run the base mesh spawner script
    spawn_base = Node(
        package='puppy_description',
        executable='spawn_mesh.py',
        name='spawn_base',
        output='screen'
    )
    
    # Run the leg mesh spawner script
    spawn_leg = Node(
        package='puppy_description',
        executable='spawn_leg.py',
        name='spawn_leg',
        output='screen'
    )
    
    # Bridge for clock synchronization
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=['/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock'],
        output='screen'
    )
    
    return LaunchDescription([
        gazebo,
        bridge,
        spawn_base,
        spawn_leg
    ]) 