#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from ros_gz_interfaces.srv import SpawnEntity
import os
from ament_index_python.packages import get_package_share_directory

class MeshSpawner(Node):
    def __init__(self):
        super().__init__('mesh_spawner')
        self.get_logger().info('Mesh spawner node started')
        
        # Create a client for the SpawnEntity service
        self.spawn_client = self.create_client(SpawnEntity, '/spawn_entity')
        
        # Wait for the service to be available
        while not self.spawn_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, waiting...')
            
        self.get_logger().info('Service is now available')
        
        # Define SDF model with mesh - using an STL file
        self.model_xml = """<?xml version="1.0" ?>
<sdf version="1.6">
  <model name="robot_base">
    <pose>0 0 0.1 0 0 0</pose>
    <link name="base_link">
      <visual name="visual">
        <geometry>
          <mesh>
            <uri>model://puppy_description/meshes/base_link.STL</uri>
            <scale>0.01 0.01 0.01</scale>
          </mesh>
        </geometry>
        <material>
          <ambient>0.5 0.5 0.5 1</ambient>
          <diffuse>0.8 0.8 0.8 1</diffuse>
          <specular>0.8 0.8 0.8 1</specular>
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
        <mass>1.0</mass>
        <inertia>
          <ixx>0.083</ixx>
          <ixy>0.0</ixy>
          <ixz>0.0</ixz>
          <iyy>0.083</iyy>
          <iyz>0.0</iyz>
          <izz>0.083</izz>
        </inertia>
      </inertial>
    </link>
  </model>
</sdf>"""
        
        # Spawn the model after a short delay
        self.timer = self.create_timer(2.0, self.spawn_model)
        
    def spawn_model(self):
        # Cancel the timer to ensure we only spawn once
        self.timer.cancel()
        
        # Create the request
        request = SpawnEntity.Request()
        request.name = 'robot_base'
        request.xml = self.model_xml
        request.robot_namespace = ''
        request.initial_pose.position.x = 0.0
        request.initial_pose.position.y = 0.0
        request.initial_pose.position.z = 0.0
        
        # Send the request
        future = self.spawn_client.call_async(request)
        future.add_done_callback(self.spawn_callback)
        
    def spawn_callback(self, future):
        try:
            response = future.result()
            self.get_logger().info(f'Model spawned: {response.success}')
            if not response.success:
                self.get_logger().error(f'Error: {response.status_message}')
        except Exception as e:
            self.get_logger().error(f'Service call failed: {e}')

def main(args=None):
    rclpy.init(args=args)
    node = MeshSpawner()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main() 