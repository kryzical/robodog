#!/usr/bin/env python3

import os
import xacro
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable, TimerAction, LogInfo, RegisterEventHandler
from launch.event_handlers import OnProcessStart
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    # Get package paths
    pkg_dir = get_package_share_directory('puppy_description')
    
    # Print debug info
    print(f"Package directory: {pkg_dir}")
    print(f"Current working directory: {os.getcwd()}")
    
    # Process the XACRO file to get the URDF
    urdf_path = os.path.join(pkg_dir, 'urdf', 'puppy.urdf.xacro')
    print(f"URDF path: {urdf_path}")
    print(f"URDF exists: {os.path.exists(urdf_path)}")
    
    robot_description_content = xacro.process_file(urdf_path).toxml()
    
    # Set environment variables specifically for the Gazebo launch context
    # Point to the parent directories where the 'puppy_description' model folder can be found
    gazebo_model_path = SetEnvironmentVariable(
        name='IGN_GAZEBO_MODEL_PATH',
        value=f"/workspace/puppy_ros2_ws/install/share:/workspace/puppy_ros2_ws/src"
    )
    gazebo_resource_path = SetEnvironmentVariable(
        name='IGN_GAZEBO_RESOURCE_PATH',
        value=f"/workspace/puppy_ros2_ws/install/share:/workspace/puppy_ros2_ws/src"
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
        arguments=[
            '/clock@rosgraph_msgs/msg/Clock[ignition.msgs.Clock',
            '/model/puppy/joint_state@sensor_msgs/msg/JointState[ignition.msgs.Model',
            '/model/puppy/cmd_vel@geometry_msgs/msg/Twist[ignition.msgs.Twist',
            '/model/puppy/odometry@nav_msgs/msg/Odometry[ignition.msgs.Odometry',
            '/model/puppy/command@std_msgs/msg/Float64MultiArray[ignition.msgs.Double_V',
            '/camera/image_raw@sensor_msgs/msg/Image[ignition.msgs.Image',
            '/camera/camera_info@sensor_msgs/msg/CameraInfo[ignition.msgs.CameraInfo'
        ],
        output='screen',
        parameters=[{'use_sim_time': True}]
    )
    
    # Robot State Publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'use_sim_time': True,
            'robot_description': robot_description_content,
            'publish_frequency': 50.0,
            'ignore_timestamp': True
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
        arguments=[
            '-topic', '/robot_description',
            '-entity', 'puppy',
            '-x', '0.0',
            '-y', '0.0',
            '-z', '0.2',  # Lift the robot slightly to avoid ground collision
            '-R', '0.0',
            '-P', '0.0',
            '-Y', '0.0'
        ],
        output='screen'
    )

    # Controller Manager
    controller_manager = Node(
        package='controller_manager',
        executable='ros2_control_node',
        parameters=[
            {
                'robot_description': robot_description_content,
                'use_sim_time': True,
                'update_rate': 100
            },
            os.path.join(pkg_dir, 'config', 'ros2_control.yaml')
        ],
        output='screen',
        name='controller_manager',
        prefix=['stdbuf -o L']
    )

    # Load joint state broadcaster
    joint_state_broadcaster_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_state_broadcaster'],
        output='screen',
        name='joint_state_broadcaster_spawner',
        prefix=['stdbuf -o L']
    )

    # Load position controller
    position_controller_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['position_controller'],
        output='screen',
        name='position_controller_spawner',
        prefix=['stdbuf -o L']
    )

    # Add delay to ensure controller manager is ready
    delay_joint_state_broadcaster = TimerAction(
        period=5.0,  # Increased delay to ensure proper initialization
        actions=[joint_state_broadcaster_spawner]
    )

    delay_position_controller = TimerAction(
        period=6.0,  # Increased delay to ensure proper initialization
        actions=[position_controller_spawner]
    )

    # Launch the stand command node
    stand_command_node = Node(
        package='puppy_control',
        executable='stand_command',
        name='stand_command',
        output='screen'
    )

    # Add delay to ensure controllers are ready before starting stand command
    delay_stand_command = TimerAction(
        period=7.0,  # Increased delay to ensure controllers are fully initialized
        actions=[stand_command_node]
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
        # Controller Manager and Controllers
        controller_manager,
        delay_joint_state_broadcaster,
        delay_position_controller,
        delay_stand_command
    ]) 