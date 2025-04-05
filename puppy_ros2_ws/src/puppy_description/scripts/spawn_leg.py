#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from ros_gz_interfaces.srv import SpawnEntity
import os
from ament_index_python.packages import get_package_share_directory

class LegSpawner(Node):
    def __init__(self):
        super().__init__('leg_spawner')
        self.get_logger().info('Leg spawner node started')
        
        # Create a client for the SpawnEntity service
        self.spawn_client = self.create_client(SpawnEntity, '/spawn_entity')
        
        # Wait for the service to be available
        while not self.spawn_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, waiting...')
            
        self.get_logger().info('Service is now available')
        
        # Define SDF model with multiple STL meshes for a leg
        self.model_xml = """<?xml version="1.0" ?>
<sdf version="1.6">
  <model name="robot_leg">
    <pose>0.2 0.2 0.05 0 0 0</pose>
    
    <!-- Upper leg link -->
    <link name="upper_link">
      <pose>0 0 0 0 0 0</pose>
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
            <size>0.05 0.05 0.15</size>
          </box>
        </geometry>
      </collision>
      <inertial>
        <mass>0.5</mass>
        <inertia>
          <ixx>0.01</ixx>
          <ixy>0.0</ixy>
          <ixz>0.0</ixz>
          <iyy>0.01</iyy>
          <iyz>0.0</iyz>
          <izz>0.005</izz>
        </inertia>
      </inertial>
    </link>
    
    <!-- Lower leg link -->
    <link name="lower_link">
      <pose>0 0 -0.12 0 0 0</pose>
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
            <size>0.03 0.03 0.12</size>
          </box>
        </geometry>
      </collision>
      <inertial>
        <mass>0.3</mass>
        <inertia>
          <ixx>0.005</ixx>
          <ixy>0.0</ixy>
          <ixz>0.0</ixz>
          <iyy>0.005</iyy>
          <iyz>0.0</iyz>
          <izz>0.001</izz>
        </inertia>
      </inertial>
    </link>
    
    <!-- Joint connecting the links -->
    <joint name="leg_joint" type="revolute">
      <parent>upper_link</parent>
      <child>lower_link</child>
      <pose>0 0 0 0 0 0</pose>
      <axis>
        <xyz>0 1 0</xyz>
        <limit>
          <lower>-1.5708</lower>
          <upper>1.5708</upper>
        </limit>
      </axis>
    </joint>
    
  </model>
</sdf>"""
        
        # Spawn the model after a short delay
        self.timer = self.create_timer(3.0, self.spawn_model)
        
    def spawn_model(self):
        # Cancel the timer to ensure we only spawn once
        self.timer.cancel()
        
        # Create the request
        request = SpawnEntity.Request()
        request.name = 'robot_leg'
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
            self.get_logger().info(f'Leg model spawned: {response.success}')
            if not response.success:
                self.get_logger().error(f'Error: {response.status_message}')
        except Exception as e:
            self.get_logger().error(f'Service call failed: {e}')

def main(args=None):
    rclpy.init(args=args)
    node = LegSpawner()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main() 