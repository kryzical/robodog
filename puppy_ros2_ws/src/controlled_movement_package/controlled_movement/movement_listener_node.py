#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32MultiArray
from controlled_movement import movement  # assuming movement.py is correctly inside your controlled_movement_package

import time
start_time = time.time()
time_now = time.time()

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

# class MovementListener(Node):
#     def __init__(self):
#         super().__init__('movement_listener')
#         self.subscription = self.create_subscription(
#             Int32MultiArray,
#             'command_topic',
#             self.listener_callback,
#             10
#         )
#         self.motion_command = [0, 0, 0, 0]  # store the latest command
#         self.start_time = time.time()

#         # Run a timer callback at 50Hz
#         self.timer = self.create_timer(0.02, self.motion_loop)

#         self.get_logger().info('Movement Listener Node has started.')

#     def listener_callback(self, msg):
#         self.motion_command = msg.data

#     def motion_loop(self):
#         time_now = time.time()

#         if self.motion_command[0]:  # Forward
#             movement.trot_forward(time_now, self.start_time)

#         elif self.motion_command[1]:  # Backward
#             movement.walk_back(time_now, self.start_time)

#         elif self.motion_command[2]:  # Left
#             movement.turn_left(time_now, self.start_time)

#         elif self.motion_command[3]:  # Right
#             movement.turn_right(time_now, self.start_time)

#         else:
#             movement.stand()


def main(args=None):
    rclpy.init(args=args)
    node = MovementListener()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
