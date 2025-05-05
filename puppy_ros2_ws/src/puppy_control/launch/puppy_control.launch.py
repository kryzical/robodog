#!/usr/bin/env python3

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    # Get package directories
    puppy_description_dir = get_package_share_directory('puppy_description')

    # Include the controlled robot launch file
    controlled_robot_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(puppy_description_dir, 'launch', 'controlled_robot.launch.py')
        )
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
        period=5.0,  # Wait for controllers to be ready
        actions=[stand_command_node]
    )

    return LaunchDescription([
        controlled_robot_launch,
        delay_stand_command
    ]) 