# #!/usr/bin/env python3

# import rclpy
# from rclpy.node import Node
# from std_msgs.msg import String
# import movement

# class MotionCommandNode(Node):
#     def __init__(self):
#         super().__init__('puppy_motion_node')
#         self.subscriber = self.create_subscription(
#             String,
#             '/puppy_motion_command',
#             self.command_callback,
#             10
#         )
#         self.get_logger().info('Motion Command Node ready.')

#     def command_callback(self, msg):
#         command = msg.data.lower()
#         self.get_logger().info(f'Received command: {command}')

#         if command == 'walk':
#             movement.trot_forward()
#         elif command == 'turn_left':
#             movement.turn_left()
#         elif command == 'stand':
#             movement.stand()
#         else:
#             self.get_logger().warn(f'Unknown command: {command}')

# def main():
#     rclpy.init()
#     node = MotionCommandNode()
#     rclpy.spin(node)
#     node.destroy_node()
#     rclpy.shutdown()

# if __name__ == '__main__':
#     main()
        
        