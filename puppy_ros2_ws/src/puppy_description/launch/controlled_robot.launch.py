#!/usr/bin/env python3

import os
import xacro
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, RegisterEventHandler
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.event_handlers import OnProcessExit
from launch_ros.actions import Node

def generate_launch_description():
    # Get the package directory
    pkg_dir = get_package_share_directory('puppy_description')
    urdf_dir = os.path.join(pkg_dir, 'urdf')
    config_dir = os.path.join(pkg_dir, 'config')
    xacro_file = os.path.join(urdf_dir, 'puppy.urdf.xacro')
    
    # Load the controller configuration
    controller_config = os.path.join(config_dir, 'gazebo_controllers.yaml')
    
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
    
    # Bridge for clock synchronization and joint states
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock]',
            '/model/puppy/joint_state@sensor_msgs/msg/JointState[gz.msgs.Model]'
        ],
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
    
    # Controller manager
    controller_manager = Node(
        package='controller_manager',
        executable='ros2_control_node',
        parameters=[
            {'robot_description': robot_description_content},
            controller_config
        ],
        output='screen'
    )
    
    # Joint state broadcaster
    joint_state_broadcaster_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_state_broadcaster', '--controller-manager', '/controller_manager'],
        output='screen'
    )
    
    # Joint trajectory controller
    joint_trajectory_controller_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_trajectory_controller', '--controller-manager', '/controller_manager'],
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
            '-z', '0.2'
        ],
        output='screen'
    )
    
    # Launch controllers after the robot is spawned
    controller_spawner_handler = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=spawn_entity,
            on_exit=[
                joint_state_broadcaster_spawner,
                joint_trajectory_controller_spawner
            ]
        )
    )
    
    return LaunchDescription([
        gazebo,
        bridge,
        robot_state_publisher,
        joint_state_publisher,
        controller_manager,
        spawn_entity,
        controller_spawner_handler
    ]) 