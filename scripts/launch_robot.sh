#!/bin/bash

# Script to launch the robot in Gazebo

# Make sure there are no existing containers running
echo "Cleaning up any existing containers..."
docker-compose -f docker-compose-gazebo-full.yml down
docker rm -f gazebo_garden gazebo_test 2>/dev/null || true

# Set X11 permissions
echo "Setting X11 permissions..."
xhost +local:docker

# Start the container with docker-compose
echo "Starting Gazebo container with docker-compose..."
docker-compose -f docker-compose-gazebo-full.yml up -d

# Wait for the container to initialize
echo "Waiting for container to initialize..."
sleep 5

# Create a launch script to use the processed URDF
echo "Creating launch script..."
docker exec -it gazebo_garden bash -c "
cat > /tmp/launch_robot.py << 'EOF'
#!/usr/bin/env python3

import os
import sys
import xacro
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    # Get the package directory
    pkg_dir = '/workspace/src/puppy_description'
    urdf_dir = os.path.join(pkg_dir, 'urdf')
    xacro_file_path = os.path.join(urdf_dir, 'puppy.urdf.xacro')
    
    if not os.path.exists(xacro_file_path):
        print(f'Error: {xacro_file_path} does not exist')
        sys.exit(1)
        
    # Process the XACRO file to generate URDF
    os.environ['PYTHONPATH'] = os.path.dirname(xacro.__file__) + ':' + os.environ.get('PYTHONPATH', '')
    robot_description_content = xacro.process_file(xacro_file_path).toxml()
    
    # Create the robot_state_publisher node
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description_content,
                    'use_sim_time': True}]
    )
    
    # Create the joint_state_publisher node
    joint_state_publisher = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        output='screen'
    )
    
    # Create a Gazebo spawn node to spawn the robot
    gazebo_spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        name='spawn_robot',
        arguments=['-topic', 'robot_description',
                  '-entity', 'puppy',
                  '-x', '0.0',
                  '-y', '0.0',
                  '-z', '0.1'],
        output='screen'
    )
    
    # Return the launch description
    return LaunchDescription([
        robot_state_publisher,
        joint_state_publisher,
        gazebo_spawn_entity
    ])
EOF

chmod +x /tmp/launch_robot.py
"

# Start Gazebo with the robot
echo "Starting Gazebo simulator..."
docker exec -d gazebo_garden bash -c "source /opt/ros/humble/setup.bash && gz sim -r empty.sdf"
echo "Gazebo started in background. Waiting for simulator to initialize..."
sleep 5

# Now launch the robot
echo "Launching robot..."
docker exec -it gazebo_garden bash -c "source /opt/ros/humble/setup.bash && source /workspace/install/setup.bash && ros2 launch /tmp/launch_robot.py" 