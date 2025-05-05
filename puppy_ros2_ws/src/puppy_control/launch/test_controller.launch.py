#!/usr/bin/env python3

from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    # Get the package directory
    pkg_dir = get_package_share_directory('puppy_control')
    
    # Robot description with ros2_control tags
    robot_description = """<?xml version="1.0"?>
    <robot name="test_robot">
        <link name="base_link"/>
        <joint name="test_joint" type="revolute">
            <parent link="base_link"/>
            <child link="test_link"/>
            <axis xyz="0 0 1"/>
            <limit lower="-2.0" upper="2.0" effort="100" velocity="1.0"/>
        </joint>
        <link name="test_link"/>

        <ros2_control name="GazeboSystem" type="system">
            <hardware>
                <plugin>gazebo_ros2_control/GazeboSystem</plugin>
            </hardware>
            <joint name="test_joint">
                <command_interface name="position"/>
                <state_interface name="position"/>
                <state_interface name="velocity"/>
                <state_interface name="effort"/>
            </joint>
        </ros2_control>
    </robot>"""

    # Robot State Publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': robot_description
        }]
    )
    
    # Controller Manager Node
    controller_manager = Node(
        package='controller_manager',
        executable='ros2_control_node',
        parameters=[
            {
                'robot_description': robot_description
            },
            os.path.join(pkg_dir, 'config', 'controllers.yaml')
        ],
        output='screen',
        name='controller_manager'
    )

    # Joint State Broadcaster
    joint_state_broadcaster = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_state_broadcaster'],
        output='screen'
    )

    # Position Controllers
    position_controllers = [
        'lf_joint1_position_controller',
        'lf_joint2_position_controller',
        'lb_joint1_position_controller',
        'lb_joint2_position_controller',
        'rf_joint1_position_controller',
        'rf_joint2_position_controller',
        'rb_joint1_position_controller',
        'rb_joint2_position_controller'
    ]

    position_controller_spawners = []
    for controller in position_controllers:
        position_controller_spawners.append(
            Node(
                package='controller_manager',
                executable='spawner',
                arguments=[controller],
                output='screen'
            )
        )

    return LaunchDescription([
        robot_state_publisher,
        controller_manager,
        joint_state_broadcaster,
        *position_controller_spawners
    ]) 