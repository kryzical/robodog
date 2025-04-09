#!/usr/bin/env python3

import os
import xacro
import tempfile
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess, RegisterEventHandler
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.event_handlers import OnProcessExit
from launch_ros.actions import Node

def generate_launch_description():
    # Get the package directory
    pkg_dir = get_package_share_directory('puppy_description')
    urdf_dir = os.path.join(pkg_dir, 'urdf')
    xacro_file = os.path.join(urdf_dir, 'puppy.urdf.xacro')
    
    # Process the XACRO file to get the URDF
    robot_description_content = xacro.process_file(xacro_file).toxml()
    
    # For debugging: Save the processed URDF to a file
    with open('/tmp/puppy_processed.urdf', 'w') as f:
        f.write(robot_description_content)
    
    # Launch Gazebo with empty world
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')
        ]),
        launch_arguments={'gz_args': '-r -v 4 empty.sdf'}.items()
    )
    
    # Bridge for clock synchronization
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=['/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock'],
        output='screen'
    )
    
    # Robot state publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': robot_description_content,
            'use_sim_time': True
        }]
    )
    
    # Joint state publisher
    joint_state_publisher = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        output='screen'
    )
    
    # Spawn robot in Gazebo
    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        name='spawn_puppy',
        arguments=[
            '-topic', 'robot_description',
            '-entity', 'puppy',
            '-x', '0.0',
            '-y', '0.0',
            '-z', '0.1'
        ],
        output='screen'
    )
    
    # Spawn test model to verify mesh loading
    spawn_test_model = ExecuteProcess(
        cmd=['gz', 'service', '-s', '/world/empty/create',
             '--reqtype', 'ignition.msgs.EntityFactory',
             '--reptype', 'ignition.msgs.Boolean',
             '--timeout', '1000',
             '--req', 'sdf_filename: "/tmp/test_model.sdf", name: "test_model", pose: {position: {x: 1.0, y: 0.0, z: 0.5}}'],
        output='screen'
    )
    
    # Launch test_model after the world is loaded
    spawn_test_handler = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=spawn_entity,
            on_exit=[spawn_test_model],
        )
    )
    
    return LaunchDescription([
        gazebo,
        bridge,
        robot_state_publisher,
        joint_state_publisher,
        spawn_entity,
        spawn_test_handler
    ]) 