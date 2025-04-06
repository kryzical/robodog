#!/usr/bin/env python3

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    # Simple robot description (basic cubes for the body and legs)
    robot_description = """<?xml version="1.0"?>
<robot name="puppy_primitive">
  <link name="base_link">
    <visual>
      <geometry>
        <box size="0.3 0.15 0.05"/>
      </geometry>
      <material name="blue">
        <color rgba="0 0 0.8 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <box size="0.3 0.15 0.05"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.0"/>
      <inertia ixx="0.1" ixy="0.0" ixz="0.0" iyy="0.1" iyz="0.0" izz="0.1"/>
    </inertial>
  </link>
  
  <!-- Front Right Leg -->
  <link name="fr_leg">
    <visual>
      <geometry>
        <box size="0.02 0.02 0.1"/>
      </geometry>
      <material name="red">
        <color rgba="0.8 0 0 1"/>
      </material>
    </visual>
  </link>
  <joint name="fr_joint" type="fixed">
    <parent link="base_link"/>
    <child link="fr_leg"/>
    <origin xyz="0.1 -0.05 -0.05"/>
  </joint>
  
  <!-- Front Left Leg -->
  <link name="fl_leg">
    <visual>
      <geometry>
        <box size="0.02 0.02 0.1"/>
      </geometry>
      <material name="red"/>
    </visual>
  </link>
  <joint name="fl_joint" type="fixed">
    <parent link="base_link"/>
    <child link="fl_leg"/>
    <origin xyz="0.1 0.05 -0.05"/>
  </joint>
  
  <!-- Back Right Leg -->
  <link name="br_leg">
    <visual>
      <geometry>
        <box size="0.02 0.02 0.1"/>
      </geometry>
      <material name="red"/>
    </visual>
  </link>
  <joint name="br_joint" type="fixed">
    <parent link="base_link"/>
    <child link="br_leg"/>
    <origin xyz="-0.1 -0.05 -0.05"/>
  </joint>
  
  <!-- Back Left Leg -->
  <link name="bl_leg">
    <visual>
      <geometry>
        <box size="0.02 0.02 0.1"/>
      </geometry>
      <material name="red"/>
    </visual>
  </link>
  <joint name="bl_joint" type="fixed">
    <parent link="base_link"/>
    <child link="bl_leg"/>
    <origin xyz="-0.1 0.05 -0.05"/>
  </joint>
  
  <!-- Camera -->
  <link name="camera_link">
    <visual>
      <geometry>
        <box size="0.02 0.05 0.02"/>
      </geometry>
      <material name="black">
        <color rgba="0 0 0 1"/>
      </material>
    </visual>
  </link>
  <joint name="camera_joint" type="fixed">
    <parent link="base_link"/>
    <child link="camera_link"/>
    <origin xyz="0.12 0 0.025"/>
  </joint>
</robot>"""
    
    # Launch Gazebo
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')
        ]),
        launch_arguments={'gz_args': '-r -v 4 empty.sdf'}.items()
    )
    
    # Robot state publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description, 'use_sim_time': True}]
    )
    
    # Joint state publisher
    joint_state_publisher = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        output='screen'
    )
    
    # Spawn robot
    spawn = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-topic', '/robot_description',
            '-entity', 'puppy_primitive',
            '-x', '0.0',
            '-y', '0.0',
            '-z', '0.1'
        ],
        output='screen'
    )
    
    # Bridge for clock synchronization
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=['/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock'],
        output='screen'
    )
    
    return LaunchDescription([
        gazebo,
        bridge,
        robot_state_publisher,
        joint_state_publisher,
        spawn
    ]) 