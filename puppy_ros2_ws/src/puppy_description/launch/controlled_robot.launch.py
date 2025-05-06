# #!/usr/bin/env python3

# import os
# import xacro
# from ament_index_python.packages import get_package_share_directory
# from launch import LaunchDescription
# from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable, TimerAction
# from launch.launch_description_sources import PythonLaunchDescriptionSource
# from launch_ros.actions import Node

# def generate_launch_description():
#     # Get package paths
#     pkg_dir = get_package_share_directory('puppy_description')
#     # Use the known absolute path for src within the container
#     src_dir = os.path.join(pkg_dir, 'urdf')

    
#     # Print debug info
#     print(f"Package directory: {pkg_dir}")
#     print(f"Source directory: {src_dir}")
    
#     # Process the XACRO file to get the URDF
#     robot_description_content = xacro.process_file(
#     os.path.join(src_dir, 'puppy.urdf.xacro')
#     ).toxml()

    
#     # Set environment variables specifically for the Gazebo launch context
#     # Point to the parent directories where the 'puppy_description' model folder can be found
#     gazebo_model_path = SetEnvironmentVariable(
#         name='IGN_GAZEBO_MODEL_PATH',
#         value=f"/workspace/puppy_ros2_ws/src:/workspace/puppy_ros2_ws/install/puppy_description/share"
#     )
#     gazebo_resource_path = SetEnvironmentVariable(
#         name='IGN_GAZEBO_RESOURCE_PATH',
#         value=f"/workspace/puppy_ros2_ws/src:/workspace/puppy_ros2_ws/install/puppy_description/share"
#     )
    
#     # Launch Ignition Gazebo with empty world
#     gazebo = IncludeLaunchDescription(
#         PythonLaunchDescriptionSource([
#             os.path.join(get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')
#         ]),
#         launch_arguments={
#             'gz_args': '-r -v 4 empty.sdf',
#             'on_exit_shutdown': 'true'
#         }.items()
#     )
    
#     # Bridge (Clock is useful)
#     bridge = Node(
#         package='ros_gz_bridge',
#         executable='parameter_bridge',
#         arguments=['/clock@rosgraph_msgs/msg/Clock[ignition.msgs.Clock'],
#         output='screen'
#     )
    
#     # Robot State Publisher
#     robot_state_publisher = Node(
#         package='robot_state_publisher',
#         executable='robot_state_publisher',
#         name='robot_state_publisher',
#         output='screen',
#         parameters=[{
#             'use_sim_time': True,
#             'robot_description': robot_description_content
#         }]
#     )
    
#     # Joint State Publisher (for visualization transforms)
#     joint_state_publisher = Node(
#         package='joint_state_publisher',
#         executable='joint_state_publisher',
#         name='joint_state_publisher',
#         output='screen',
#         parameters=[{'use_sim_time': True}]
#     )
    
#     # Spawn robot entity in Gazebo
#     #spawn_entity = Node(
#     #    package='ros_gz_sim',
#     #    executable='create',
#     #    arguments=['-topic', '/robot_description', '-entity', 'puppy'],
#     #    output='screen'
#     #)

#     spawn_entity = TimerAction(
#         period=5.0,
#         actions=[Node(
#         package='ros_gz_sim',
#         executable='create',
#         arguments=['-topic', '/robot_description', '-entity', 'puppy'],
#         output='screen'
#         )]
#     )

#     # --- Launch Description ---
#     return LaunchDescription([
#         # Set Environment variables first
#         gazebo_model_path,
#         gazebo_resource_path,
#         # Launch Gazebo
#         gazebo,
#         # Bridges (Clock is useful)
#         bridge,
#         # Robot Description and State Publisher (Needed for TF and visual links)
#         robot_state_publisher,
#         joint_state_publisher,
#         # Spawn Robot
#         spawn_entity,
#         # --- Controllers Removed ---
#     ]) 


#!/usr/bin/env python3

import os
import xacro
from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    SetEnvironmentVariable,
    TimerAction
)
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import IncludeLaunchDescription

def generate_launch_description():
    # Launch arguments
    use_sim = LaunchConfiguration('use_sim')

    # Declare launch argument
    declare_use_sim = DeclareLaunchArgument(
        'use_sim',
        default_value='true',
        description='Whether to launch Ignition Gazebo simulation'
    )

    # Get package paths
    pkg_dir = get_package_share_directory('puppy_description')
    urdf_path = os.path.join(pkg_dir, 'urdf', 'puppy.urdf.xacro')

    # Process the XACRO file
    robot_description_content = xacro.process_file(urdf_path).toxml()

    # Environment variables (only needed for Gazebo)
    gazebo_model_path = SetEnvironmentVariable(
        name='IGN_GAZEBO_MODEL_PATH',
        value="/workspace/puppy_ros2_ws/install/share:/workspace/puppy_ros2_ws/src"
    )
    gazebo_resource_path = SetEnvironmentVariable(
        name='IGN_GAZEBO_RESOURCE_PATH',
        value="/workspace/puppy_ros2_ws/install/share:/workspace/puppy_ros2_ws/src"
    )

    # Gazebo launch
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')
        ]),
        launch_arguments={
            'gz_args': '-r -v 4 empty.sdf',
            'on_exit_shutdown': 'true'
        }.items(),
        condition=IfCondition(use_sim)
    )

    # Bridge between Gazebo and ROS
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/clock@rosgraph_msgs/msg/Clock[ignition.msgs.Clock',
            '/model/puppy/joint_state@sensor_msgs/msg/JointState[ignition.msgs.Model',
            '/model/puppy/cmd_vel@geometry_msgs/msg/Twist[ignition.msgs.Twist',
            '/model/puppy/odometry@nav_msgs/msg/Odometry[ignition.msgs.Odometry',
            '/model/puppy/command@std_msgs/msg/Float64MultiArray[ignition.msgs.Double_V'
        ],
        output='screen',
        parameters=[{'use_sim_time': True}],
        condition=IfCondition(use_sim)
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

    # Joint State Publisher
    joint_state_publisher = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        output='screen',
        parameters=[{'use_sim_time': True}]
    )

    # Spawn robot into Gazebo
    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-topic', '/robot_description', '-entity', 'puppy'],
        output='screen',
        condition=IfCondition(use_sim)
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

    # Spawners
    joint_state_broadcaster_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_state_broadcaster'],
        output='screen',
        name='joint_state_broadcaster_spawner',
        prefix=['stdbuf -o L']
    )

    position_controller_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['position_controller'],
        output='screen',
        name='position_controller_spawner',
        prefix=['stdbuf -o L']
    )

    # Delay actions
    delay_joint_state_broadcaster = TimerAction(
        period=5.0,
        actions=[joint_state_broadcaster_spawner]
    )

    delay_position_controller = TimerAction(
        period=6.0,
        actions=[position_controller_spawner]
    )

    return LaunchDescription([
        declare_use_sim,
        gazebo_model_path,
        gazebo_resource_path,
        gazebo,
        bridge,
        robot_state_publisher,
        joint_state_publisher,
        spawn_entity,
        controller_manager,
        delay_joint_state_broadcaster,
        delay_position_controller
    ])
