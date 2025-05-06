# puppy_description/launch/camera_node.launch.py

from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='v4l2_camera',
            executable='v4l2_camera_node',
            name='v4l2_camera_node',
            output='screen',
            parameters=[{
                'video_device': '/dev/video0',
                'image_size': [640, 480],
                'camera_frame_id': 'camera_link',
                'pixel_format': 'YUYV',
                'use_sensor_data_qos': True
            }]
        )
    ])
