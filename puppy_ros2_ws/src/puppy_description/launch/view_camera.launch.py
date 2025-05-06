from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', '/workspace/puppy_ros2_ws/src/puppy_description/rviz/puppy_camera.rviz'],
            output='screen'
        ),
        Node(
            package='image_transport',
            executable='republish',
            name='image_republish',
            arguments=['raw', 'compressed'],
            remappings=[('/in', '/camera/image_raw'), ('/out', '/camera/image_raw/compressed')],
            output='screen'
        )
    ])
