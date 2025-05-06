#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
from sensor_msgs.msg import JointState
import math
import time

class PuppyWalkNode(Node):
    def __init__(self):
        super().__init__('puppy_walk')
        
        # Create publisher for position controller
        self.position_publisher = self.create_publisher(
            Float64MultiArray,
            '/position_controller/commands',
            10
        )
        
        # Define joint order (must match controller configuration)
        self.joints = [
            'lf_joint1', 'lf_joint2',  # Left front
            'lb_joint1', 'lb_joint2',  # Left back
            'rf_joint1', 'rf_joint2',  # Right front
            'rb_joint1', 'rb_joint2'   # Right back
        ]
        
        # Subscribe to joint states
        self.joint_sub = self.create_subscription(
            JointState,
            '/joint_states',
            self.joint_callback,
            10
        )
        
        # Store current joint positions
        self.current_positions = {joint: 0.0 for joint in self.joints}
        
        # Walking parameters
        self.step_height = 0.1  # Reduced height for more stability
        self.step_length = 0.15  # Reduced length for more stability
        self.step_duration = 1.0  # Increased duration for smoother motion
        self.walking_duration = 5.0  # Total walking time in seconds
        
        # Create timer for walking sequence
        self.walk_timer = self.create_timer(0.1, self.walk_sequence)
        self.start_time = time.time()
        
        self.get_logger().info('Puppy walk node started')
    
    def joint_callback(self, msg):
        # Update current joint positions
        for i, name in enumerate(msg.name):
            if name in self.joints:
                self.current_positions[name] = msg.position[i]
                self.get_logger().debug(f'Joint {name} position: {msg.position[i]}')
    
    def walk_sequence(self):
        current_time = time.time() - self.start_time
        
        if current_time >= self.walking_duration:
            # Return to standing position
            self.return_to_stand()
            self.walk_timer.cancel()
            return
        
        # Calculate step phase (0 to 1)
        step_phase = (current_time % self.step_duration) / self.step_duration
        
        # Define walking positions for each joint
        positions = self.calculate_walking_positions(step_phase)
        
        # Create and send command message
        msg = Float64MultiArray()
        msg.data = [positions[joint] for joint in self.joints]
        self.position_publisher.publish(msg)
        self.get_logger().debug(f'Sending command: {msg.data}')
    
    def calculate_walking_positions(self, phase):
        # Base standing positions (matching stand_command.py)
        positions = {
            'lf_joint1': 0.8,  # Front left shoulder
            'lf_joint2': 0.0,  # Front left knee
            'lb_joint1': 0.8,  # Back left shoulder
            'lb_joint2': 0.0,  # Back left knee
            'rf_joint1': 0.8,  # Front right shoulder
            'rf_joint2': 0.0,  # Front right knee
            'rb_joint1': 0.8,  # Back right shoulder
            'rb_joint2': 0.0   # Back right knee
        }
        
        # Calculate step offsets
        step_offset = math.sin(phase * 2 * math.pi)
        
        # Knee bending offset (90 degrees out of phase with step)
        knee_offset = math.sin((phase + 0.25) * 2 * math.pi)
        
        # Apply walking motion to diagonal pairs
        # Left front and right back move together
        positions['lf_joint1'] += self.step_length * step_offset
        positions['lf_joint2'] = self.step_height * knee_offset  # Knee bends during step
        positions['rb_joint1'] += self.step_length * step_offset
        positions['rb_joint2'] = self.step_height * knee_offset  # Knee bends during step
        
        # Right front and left back move together (opposite phase)
        positions['rf_joint1'] += self.step_length * (-step_offset)
        positions['rf_joint2'] = self.step_height * (-knee_offset)  # Knee bends during step
        positions['lb_joint1'] += self.step_length * (-step_offset)
        positions['lb_joint2'] = self.step_height * (-knee_offset)  # Knee bends during step
        
        return positions
    
    def return_to_stand(self):
        # Return to standing position (matching stand_command.py)
        standing_positions = {
            'lf_joint1': 0.8,
            'lf_joint2': 0.0,
            'lb_joint1': 0.8,
            'lb_joint2': 0.0,
            'rf_joint1': 0.8,
            'rf_joint2': 0.0,
            'rb_joint1': 0.8,
            'rb_joint2': 0.0
        }
        
        # Create and send command message
        msg = Float64MultiArray()
        msg.data = [standing_positions[joint] for joint in self.joints]
        self.position_publisher.publish(msg)
        self.get_logger().info(f'Returning to standing position: {msg.data}')
        
        # Wait for joints to reach position
        time.sleep(2.0)
        
        # Verify positions and send correction if needed
        needs_correction = False
        for joint, target_position in standing_positions.items():
            current_position = self.current_positions[joint]
            if abs(current_position - target_position) > 0.1:  # If more than 0.1 radian off
                needs_correction = True
                self.get_logger().info(f'Joint {joint} needs correction: current={current_position}, target={target_position}')
        
        if needs_correction:
            self.get_logger().info('Sending position correction...')
            self.position_publisher.publish(msg)
        
        self.get_logger().info('Returned to standing position')

def main(args=None):
    rclpy.init(args=args)
    node = PuppyWalkNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()