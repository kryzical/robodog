#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32MultiArray
from controlled_movement import movement  # assuming movement.py is correctly inside your controlled_movement_package

class MovementListener(Node):
    def __init__(self):
        super().__init__('movement_listener')
        self.subscription = self.create_subscription(
            Int32MultiArray,
            'command_topic',
            self.listener_callback,
            10
        )
        self.subscription  # prevent unused variable warning
        self.get_logger().info('Movement Listener Node has started.')

    def listener_callback(self, msg):
        # msg.data = [up, down, left, right] (0 or 1 each)
        movement_states = msg.data
        self.get_logger().info(f"Received movement command: {movement_states}")

        if movement_states[0]:  # Up key (W)
            self.get_logger().info('Walking forward...')
            movement.trot_forward()

        elif movement_states[1]:  # Down key (S)
            self.get_logger().info('Walking backward...')
            movement.walk_back()  # Not implemented

        elif movement_states[2]:  # Left key (A)
            self.get_logger().info('Turning left...')
            movement.turn_left()

        elif movement_states[3]:  # Right key (D)
            self.get_logger().info('Turning right...')
            movement.turn_right()

        else:
            self.get_logger().info('Standing still.')
            movement.stand()

def main(args=None):
    rclpy.init(args=args)
    node = MovementListener()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
