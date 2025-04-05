import os
import xacro
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    # Get the package directory
    pkg_dir = get_package_share_directory('puppy_description')
    
    # Set up the use_sim_time parameter
    use_sim_time = LaunchConfiguration('use_sim_time', default='false')
    
    # Process the XACRO file
    robot_description_path = os.path.join(pkg_dir, 'urdf', 'puppy.urdf.xacro')
    robot_description = xacro.process_file(robot_description_path).toxml()
    
    # Joint state publisher with GUI
    joint_state_publisher = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        output='screen'
    )
    
    # Robot state publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description, 'use_sim_time': use_sim_time}]
    )
    
    # RViz
    rviz_config_file = os.path.join(pkg_dir, 'config', 'display.rviz')
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config_file] if os.path.exists(rviz_config_file) else [],
        parameters=[{'use_sim_time': use_sim_time}]
    )
    
    # Return the launch description
    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='false',
                              description='Use simulation time if true'),
        joint_state_publisher,
        robot_state_publisher,
        rviz
    ]) 