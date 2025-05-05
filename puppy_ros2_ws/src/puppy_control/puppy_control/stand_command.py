#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
from sensor_msgs.msg import JointState
import time

class StandCommand(Node):
    def __init__(self):
        super().__init__('stand_command')
        
        # Create publisher for position controller
        self.position_publisher = self.create_publisher(
            Float64MultiArray,
            '/position_controller/commands',
            10
        )
        
        # Subscribe to joint states
        self.joint_sub = self.create_subscription(
            JointState,
            '/joint_states',
            self.joint_callback,
            10
        )
        
        # Define joint order
        self.joints = [
            'lf_joint1', 'lf_joint2',
            'lb_joint1', 'lb_joint2',
            'rf_joint1', 'rf_joint2',
            'rb_joint1', 'rb_joint2'
        ]
        
        # Store current joint positions
        self.current_positions = {joint: 0.0 for joint in self.joints}
        
        # Stand positions (in radians)
        self.stand_positions = {
            'lf_joint1': 0.8,  # Front left shoulder
            'lf_joint2': 0.0,  # Front left knee
            'lb_joint1': 0.8,  # Back left shoulder
            'lb_joint2': 0.0,  # Back left knee
            'rf_joint1': 0.8,  # Front right shoulder
            'rf_joint2': 0.0,  # Front right knee
            'rb_joint1': 0.8,  # Back right shoulder
            'rb_joint2': 0.0   # Back right knee
        }
        
        # Initialize state
        self.initialized = False
        self.command_sent = False
        self.retry_count = 0
        self.max_retries = 3
        
        # Create timer for initialization check
        self.init_timer = self.create_timer(0.5, self.check_initialization)
        
        self.get_logger().info('Stand command node initialized')
    
    def joint_callback(self, msg):
        # Update current joint positions
        for i, name in enumerate(msg.name):
            if name in self.current_positions:
                self.current_positions[name] = msg.position[i]
    
    def check_initialization(self):
        # Check if we have received joint states for all joints
        if not self.initialized and all(abs(self.current_positions[joint]) > 0.0 for joint in self.current_positions):
            self.initialized = True
            self.get_logger().info('All joints initialized')
            # Send stand command
            self.send_stand_command()
            # Cancel the initialization timer
            self.init_timer.cancel()
        elif not self.initialized and self.retry_count < self.max_retries:
            self.retry_count += 1
            self.get_logger().warn(f'Waiting for joint initialization... (Attempt {self.retry_count}/{self.max_retries})')
        elif not self.initialized:
            self.get_logger().error('Failed to initialize joints after maximum retries')
            self.init_timer.cancel()
    
    def send_stand_command(self):
        if not self.command_sent:
            self.get_logger().info('Starting stand up sequence...')
            
            # Create message with all joint positions in order
            msg = Float64MultiArray()
            msg.data = [self.stand_positions[joint] for joint in self.joints]
            
            # Send command
            self.position_publisher.publish(msg)
            self.get_logger().info(f'Sent stand command: {msg.data}')
            
            # Wait for joints to reach position
            time.sleep(2.0)
            
            # Verify positions and send correction if needed
            needs_correction = False
            for joint, target_position in self.stand_positions.items():
                current_position = self.current_positions[joint]
                if abs(current_position - target_position) > 0.1:  # If more than 0.1 radian off
                    needs_correction = True
                    self.get_logger().info(f'Joint {joint} needs correction: current={current_position}, target={target_position}')
            
            if needs_correction:
                self.get_logger().info('Sending position correction...')
                self.position_publisher.publish(msg)
            
            self.command_sent = True
            self.get_logger().info('Stand up sequence completed')

def main(args=None):
    rclpy.init(args=args)
    node = StandCommand()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main() 