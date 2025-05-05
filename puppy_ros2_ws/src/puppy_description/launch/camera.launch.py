import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    # Get the package directory
    pkg_dir = get_package_share_directory('puppy_description')

    # Define the launch configuration
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    # Define the launch actions
    spawn_camera = ExecuteProcess(
        cmd=['ros2', 'run', 'gazebo_ros', 'spawn_entity.py',
             '-entity', 'camera',
             '-file', os.path.join(pkg_dir, 'urdf', 'camera.urdf.xacro'),
             '-x', '0.0',
             '-y', '0.0',
             '-z', '0.0'],
        output='screen'
    )

    # Define the launch description
    return LaunchDescription([
        spawn_camera
    ]) 