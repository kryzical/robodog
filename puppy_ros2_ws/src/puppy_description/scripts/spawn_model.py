#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from ros_gz_interfaces.srv import SpawnEntity
import time
from std_msgs.msg import String

class ModelSpawner(Node):
    def __init__(self):
        super().__init__('model_spawner')
        self.get_logger().info('Model spawner node started')
        
        # Create a client for the SpawnEntity service
        self.spawn_client = self.create_client(SpawnEntity, '/spawn_entity')
        
        # Wait for the service to be available
        while not self.spawn_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, waiting...')
            
        self.get_logger().info('Service is now available')
        
        # Define a simple SDF model (a red cube)
        self.model_xml = """<?xml version="1.0" ?>
<sdf version="1.6">
  <model name="my_cube">
    <pose>0 0 0.5 0 0 0</pose>
    <link name="link">
      <visual name="visual">
        <geometry>
          <box>
            <size>0.5 0.5 0.5</size>
          </box>
        </geometry>
        <material>
          <ambient>1 0 0 1</ambient>
          <diffuse>1 0 0 1</diffuse>
          <specular>1 1 1 1</specular>
        </material>
      </visual>
      <collision name="collision">
        <geometry>
          <box>
            <size>0.5 0.5 0.5</size>
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
        request.name = 'my_cube'
        request.xml = self.model_xml
        request.robot_namespace = ''
        request.initial_pose.position.x = 0.0
        request.initial_pose.position.y = 0.0
        request.initial_pose.position.z = 0.5
        
        # Send the request
        future = self.spawn_client.call_async(request)
        future.add_done_callback(self.spawn_callback)
        
    def spawn_callback(self, future):
        try:
            response = future.result()
            self.get_logger().info(f'Model spawned: {response.success}')
        except Exception as e:
            self.get_logger().error(f'Service call failed: {e}')

def main(args=None):
    rclpy.init(args=args)
    node = ModelSpawner()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main() 