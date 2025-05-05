from launch import LaunchDescription
from launch.actions import ExecuteProcess, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.actions import RegisterEventHandler
from launch.event_handlers import OnProcessStart
import os
import xacro
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # Get the package directories
    puppy_control_dir = get_package_share_directory('puppy_control')
    puppy_description_dir = get_package_share_directory('puppy_description')
    
    # Process the XACRO file to get the URDF
    urdf_path = os.path.join(puppy_description_dir, 'urdf', 'puppy.urdf.xacro')
    robot_description_content = xacro.process_file(urdf_path).toxml()
    
    # Launch Gazebo
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')]),
    )
    
    # Robot State Publisher
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
    
    # Spawn the robot in Gazebo
    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-topic', '/robot_description',
            '-entity', 'puppy',
            '-x', '0.0',
            '-y', '0.0',
            '-z', '0.1'
        ],
        output='screen'
    )
    
    # Launch the controller manager
    controller_manager = Node(
        package='controller_manager',
        executable='ros2_control_node',
        parameters=[
            {
                'robot_description': robot_description_content,
                'use_sim_time': True
            },
            os.path.join(puppy_control_dir, 'config', 'controllers.yaml')
        ],
        output='screen',
        name='controller_manager'
    )
    
    # Load joint state broadcaster
    joint_state_broadcaster_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_state_broadcaster'],
        output='screen',
        name='joint_state_broadcaster_spawner'
    )
    
    # Load position controllers
    position_controllers_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['position_controller'],
        output='screen',
        name='position_controllers_spawner'
    )
    
    # Register event handlers to ensure proper startup order
    joint_state_broadcaster_event = RegisterEventHandler(
        event_handler=OnProcessStart(
            target_action=controller_manager,
            on_start=[joint_state_broadcaster_spawner]
        )
    )
    
    position_controllers_event = RegisterEventHandler(
        event_handler=OnProcessStart(
            target_action=joint_state_broadcaster_spawner,
            on_start=[position_controllers_spawner]
        )
    )
    
    # Launch our motion node
    motion_node = Node(
        package='puppy_control',
        executable='puppy_motion_node',
        name='puppy_motion',
        output='screen'
    )
    
    return LaunchDescription([
        gazebo,
        robot_state_publisher,
        spawn_entity,
        controller_manager,
        joint_state_broadcaster_event,
        position_controllers_event,
        motion_node
    ]) 