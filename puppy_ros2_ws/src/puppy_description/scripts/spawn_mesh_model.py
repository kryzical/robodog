#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from ros_gz_interfaces.srv import SpawnEntity
import os
from ament_index_python.packages import get_package_share_directory

class RobotSpawner(Node):
    def __init__(self):
        super().__init__('robot_spawner')
        self.get_logger().info('Robot spawner node started')
        
        # Create a client for the SpawnEntity service
        self.spawn_client = self.create_client(SpawnEntity, '/spawn_entity')
        
        # Wait for the service to be available
        while not self.spawn_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, waiting...')
            
        self.get_logger().info('Service is now available')
        
        # Define robot model with all STL meshes
        self.model_xml = """<?xml version="1.0" ?>
<sdf version="1.6">
  <model name="puppy_robot">
    <pose>0 0 0.1 0 0 0</pose>
    
    <!-- Base link -->
    <link name="base_link">
      <pose>0 0 0.05 0 0 0</pose>
      <visual name="visual">
        <geometry>
          <mesh>
            <uri>model://puppy_description/meshes/base_link.STL</uri>
            <scale>0.01 0.01 0.01</scale>
          </mesh>
        </geometry>
        <material>
          <ambient>0.5 0.5 0.5 1</ambient>
          <diffuse>0.7 0.7 0.7 1</diffuse>
        </material>
      </visual>
      <collision name="collision">
        <geometry>
          <box>
            <size>0.3 0.2 0.05</size>
          </box>
        </geometry>
      </collision>
      <inertial>
        <mass>2.0</mass>
        <inertia>
          <ixx>0.1</ixx>
          <ixy>0.0</ixy>
          <ixz>0.0</ixz>
          <iyy>0.1</iyy>
          <iyz>0.0</iyz>
          <izz>0.1</izz>
        </inertia>
      </inertial>
    </link>
    
    <!-- Camera link -->
    <link name="camera_link">
      <pose>0.12 0 0.07 0 0 0</pose>
      <visual name="visual">
        <geometry>
          <mesh>
            <uri>model://puppy_description/meshes/camera_link.STL</uri>
            <scale>0.01 0.01 0.01</scale>
          </mesh>
        </geometry>
        <material>
          <ambient>0.2 0.2 0.2 1</ambient>
          <diffuse>0.2 0.2 0.2 1</diffuse>
        </material>
      </visual>
      <collision name="collision">
        <geometry>
          <box>
            <size>0.05 0.05 0.05</size>
          </box>
        </geometry>
      </collision>
      <inertial>
        <mass>0.1</mass>
        <inertia>
          <ixx>0.001</ixx>
          <ixy>0.0</ixy>
          <ixz>0.0</ixz>
          <iyy>0.001</iyy>
          <iyz>0.0</iyz>
          <izz>0.001</izz>
        </inertia>
      </inertial>
    </link>
    
    <!-- Right front leg - upper link -->
    <link name="rf_link1">
      <pose>0.12 -0.08 0.03 0 0 0</pose>
      <visual name="visual">
        <geometry>
          <mesh>
            <uri>model://puppy_description/meshes/rf_link1.STL</uri>
            <scale>0.01 0.01 0.01</scale>
          </mesh>
        </geometry>
        <material>
          <ambient>0.7 0.5 0.3 1</ambient>
          <diffuse>0.7 0.5 0.3 1</diffuse>
        </material>
      </visual>
      <collision name="collision">
        <geometry>
          <box>
            <size>0.03 0.03 0.10</size>
          </box>
        </geometry>
      </collision>
      <inertial>
        <mass>0.3</mass>
        <inertia>
          <ixx>0.001</ixx>
          <ixy>0.0</ixy>
          <ixz>0.0</ixz>
          <iyy>0.001</iyy>
          <iyz>0.0</iyz>
          <izz>0.001</izz>
        </inertia>
      </inertial>
    </link>
    
    <!-- Right front leg - lower link -->
    <link name="rf_link2">
      <pose>0.12 -0.08 -0.08 0 0 0</pose>
      <visual name="visual">
        <geometry>
          <mesh>
            <uri>model://puppy_description/meshes/rf_link2.STL</uri>
            <scale>0.01 0.01 0.01</scale>
          </mesh>
        </geometry>
        <material>
          <ambient>0.3 0.3 0.7 1</ambient>
          <diffuse>0.3 0.3 0.7 1</diffuse>
        </material>
      </visual>
      <collision name="collision">
        <geometry>
          <box>
            <size>0.02 0.02 0.10</size>
          </box>
        </geometry>
      </collision>
      <inertial>
        <mass>0.2</mass>
        <inertia>
          <ixx>0.001</ixx>
          <ixy>0.0</ixy>
          <ixz>0.0</ixz>
          <iyy>0.001</iyy>
          <iyz>0.0</iyz>
          <izz>0.001</izz>
        </inertia>
      </inertial>
    </link>
    
    <!-- Left front leg - upper link -->
    <link name="lf_link1">
      <pose>0.12 0.08 0.03 0 0 0</pose>
      <visual name="visual">
        <geometry>
          <mesh>
            <uri>model://puppy_description/meshes/lf_link1.STL</uri>
            <scale>0.01 0.01 0.01</scale>
          </mesh>
        </geometry>
        <material>
          <ambient>0.7 0.5 0.3 1</ambient>
          <diffuse>0.7 0.5 0.3 1</diffuse>
        </material>
      </visual>
      <collision name="collision">
        <geometry>
          <box>
            <size>0.03 0.03 0.10</size>
          </box>
        </geometry>
      </collision>
      <inertial>
        <mass>0.3</mass>
        <inertia>
          <ixx>0.001</ixx>
          <ixy>0.0</ixy>
          <ixz>0.0</ixz>
          <iyy>0.001</iyy>
          <iyz>0.0</iyz>
          <izz>0.001</izz>
        </inertia>
      </inertial>
    </link>
    
    <!-- Left front leg - lower link -->
    <link name="lf_link2">
      <pose>0.12 0.08 -0.08 0 0 0</pose>
      <visual name="visual">
        <geometry>
          <mesh>
            <uri>model://puppy_description/meshes/lf_link2.STL</uri>
            <scale>0.01 0.01 0.01</scale>
          </mesh>
        </geometry>
        <material>
          <ambient>0.3 0.3 0.7 1</ambient>
          <diffuse>0.3 0.3 0.7 1</diffuse>
        </material>
      </visual>
      <collision name="collision">
        <geometry>
          <box>
            <size>0.02 0.02 0.10</size>
          </box>
        </geometry>
      </collision>
      <inertial>
        <mass>0.2</mass>
        <inertia>
          <ixx>0.001</ixx>
          <ixy>0.0</ixy>
          <ixz>0.0</ixz>
          <iyy>0.001</iyy>
          <iyz>0.0</iyz>
          <izz>0.001</izz>
        </inertia>
      </inertial>
    </link>
    
    <!-- Right back leg - upper link -->
    <link name="rb_link1">
      <pose>-0.12 -0.08 0.03 0 0 0</pose>
      <visual name="visual">
        <geometry>
          <mesh>
            <uri>model://puppy_description/meshes/rb_link1.STL</uri>
            <scale>0.01 0.01 0.01</scale>
          </mesh>
        </geometry>
        <material>
          <ambient>0.7 0.5 0.3 1</ambient>
          <diffuse>0.7 0.5 0.3 1</diffuse>
        </material>
      </visual>
      <collision name="collision">
        <geometry>
          <box>
            <size>0.03 0.03 0.10</size>
          </box>
        </geometry>
      </collision>
      <inertial>
        <mass>0.3</mass>
        <inertia>
          <ixx>0.001</ixx>
          <ixy>0.0</ixy>
          <ixz>0.0</ixz>
          <iyy>0.001</iyy>
          <iyz>0.0</iyz>
          <izz>0.001</izz>
        </inertia>
      </inertial>
    </link>
    
    <!-- Right back leg - lower link -->
    <link name="rb_link2">
      <pose>-0.12 -0.08 -0.08 0 0 0</pose>
      <visual name="visual">
        <geometry>
          <mesh>
            <uri>model://puppy_description/meshes/rb_link2.STL</uri>
            <scale>0.01 0.01 0.01</scale>
          </mesh>
        </geometry>
        <material>
          <ambient>0.3 0.3 0.7 1</ambient>
          <diffuse>0.3 0.3 0.7 1</diffuse>
        </material>
      </visual>
      <collision name="collision">
        <geometry>
          <box>
            <size>0.02 0.02 0.10</size>
          </box>
        </geometry>
      </collision>
      <inertial>
        <mass>0.2</mass>
        <inertia>
          <ixx>0.001</ixx>
          <ixy>0.0</ixy>
          <ixz>0.0</ixz>
          <iyy>0.001</iyy>
          <iyz>0.0</iyz>
          <izz>0.001</izz>
        </inertia>
      </inertial>
    </link>
    
    <!-- Left back leg - upper link -->
    <link name="lb_link1">
      <pose>-0.12 0.08 0.03 0 0 0</pose>
      <visual name="visual">
        <geometry>
          <mesh>
            <uri>model://puppy_description/meshes/lb_link1.STL</uri>
            <scale>0.01 0.01 0.01</scale>
          </mesh>
        </geometry>
        <material>
          <ambient>0.7 0.5 0.3 1</ambient>
          <diffuse>0.7 0.5 0.3 1</diffuse>
        </material>
      </visual>
      <collision name="collision">
        <geometry>
          <box>
            <size>0.03 0.03 0.10</size>
          </box>
        </geometry>
      </collision>
      <inertial>
        <mass>0.3</mass>
        <inertia>
          <ixx>0.001</ixx>
          <ixy>0.0</ixy>
          <ixz>0.0</ixz>
          <iyy>0.001</iyy>
          <iyz>0.0</iyz>
          <izz>0.001</izz>
        </inertia>
      </inertial>
    </link>
    
    <!-- Left back leg - lower link -->
    <link name="lb_link2">
      <pose>-0.12 0.08 -0.08 0 0 0</pose>
      <visual name="visual">
        <geometry>
          <mesh>
            <uri>model://puppy_description/meshes/lb_link2.STL</uri>
            <scale>0.01 0.01 0.01</scale>
          </mesh>
        </geometry>
        <material>
          <ambient>0.3 0.3 0.7 1</ambient>
          <diffuse>0.3 0.3 0.7 1</diffuse>
        </material>
      </visual>
      <collision name="collision">
        <geometry>
          <box>
            <size>0.02 0.02 0.10</size>
          </box>
        </geometry>
      </collision>
      <inertial>
        <mass>0.2</mass>
        <inertia>
          <ixx>0.001</ixx>
          <ixy>0.0</ixy>
          <ixz>0.0</ixz>
          <iyy>0.001</iyy>
          <iyz>0.0</iyz>
          <izz>0.001</izz>
        </inertia>
      </inertial>
    </link>
    
    <!-- Joint connections -->
    <!-- Camera joint -->
    <joint name="camera_joint" type="fixed">
      <parent>base_link</parent>
      <child>camera_link</child>
    </joint>
    
    <!-- Right front leg joints -->
    <joint name="rf_joint1" type="revolute">
      <parent>base_link</parent>
      <child>rf_link1</child>
      <axis>
        <xyz>0 1 0</xyz>
        <limit>
          <lower>-0.5</lower>
          <upper>0.5</upper>
        </limit>
      </axis>
    </joint>
    
    <joint name="rf_joint2" type="revolute">
      <parent>rf_link1</parent>
      <child>rf_link2</child>
      <axis>
        <xyz>0 1 0</xyz>
        <limit>
          <lower>-1.0</lower>
          <upper>1.0</upper>
        </limit>
      </axis>
    </joint>
    
    <!-- Left front leg joints -->
    <joint name="lf_joint1" type="revolute">
      <parent>base_link</parent>
      <child>lf_link1</child>
      <axis>
        <xyz>0 1 0</xyz>
        <limit>
          <lower>-0.5</lower>
          <upper>0.5</upper>
        </limit>
      </axis>
    </joint>
    
    <joint name="lf_joint2" type="revolute">
      <parent>lf_link1</parent>
      <child>lf_link2</child>
      <axis>
        <xyz>0 1 0</xyz>
        <limit>
          <lower>-1.0</lower>
          <upper>1.0</upper>
        </limit>
      </axis>
    </joint>
    
    <!-- Right back leg joints -->
    <joint name="rb_joint1" type="revolute">
      <parent>base_link</parent>
      <child>rb_link1</child>
      <axis>
        <xyz>0 1 0</xyz>
        <limit>
          <lower>-0.5</lower>
          <upper>0.5</upper>
        </limit>
      </axis>
    </joint>
    
    <joint name="rb_joint2" type="revolute">
      <parent>rb_link1</parent>
      <child>rb_link2</child>
      <axis>
        <xyz>0 1 0</xyz>
        <limit>
          <lower>-1.0</lower>
          <upper>1.0</upper>
        </limit>
      </axis>
    </joint>
    
    <!-- Left back leg joints -->
    <joint name="lb_joint1" type="revolute">
      <parent>base_link</parent>
      <child>lb_link1</child>
      <axis>
        <xyz>0 1 0</xyz>
        <limit>
          <lower>-0.5</lower>
          <upper>0.5</upper>
        </limit>
      </axis>
    </joint>
    
    <joint name="lb_joint2" type="revolute">
      <parent>lb_link1</parent>
      <child>lb_link2</child>
      <axis>
        <xyz>0 1 0</xyz>
        <limit>
          <lower>-1.0</lower>
          <upper>1.0</upper>
        </limit>
      </axis>
    </joint>
    
  </model>
</sdf>"""
        
        # Spawn the model after a short delay
        self.timer = self.create_timer(2.0, self.spawn_model)
        
    def spawn_model(self):
        # Cancel the timer to ensure we only spawn once
        self.timer.cancel()
        
        # Create the request
        request = SpawnEntity.Request()
        request.name = 'puppy_robot'
        request.xml = self.model_xml
        request.robot_namespace = ''
        request.initial_pose.position.x = 0.0
        request.initial_pose.position.y = 0.0
        request.initial_pose.position.z = 0.2
        
        # Send the request
        future = self.spawn_client.call_async(request)
        future.add_done_callback(self.spawn_callback)
        
    def spawn_callback(self, future):
        try:
            response = future.result()
            self.get_logger().info(f'Robot model spawned: {response.success}')
            if not response.success:
                self.get_logger().error(f'Error: {response.status_message}')
        except Exception as e:
            self.get_logger().error(f'Service call failed: {e}')

def main(args=None):
    rclpy.init(args=args)
    node = RobotSpawner()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main() 