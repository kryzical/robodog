# #!/usr/bin/env python3
# import rclpy
# from rclpy.node import Node
# from std_msgs.msg import Float64
# import time

# class PuppyWalker(Node):
#     def __init__(self):
#         super().__init__('puppy_walker')

#         self.joints = {
#             'lf_joint1': self.create_publisher(Float64, '/lf_joint1_position_controller/command', 10),
#             'lf_joint2': self.create_publisher(Float64, '/lf_joint2_position_controller/command', 10),
#             'lb_joint1': self.create_publisher(Float64, '/lb_joint1_position_controller/command', 10),
#             'lb_joint2': self.create_publisher(Float64, '/lb_joint2_position_controller/command', 10),
#             'rf_joint1': self.create_publisher(Float64, '/rf_joint1_position_controller/command', 10),
#             'rf_joint2': self.create_publisher(Float64, '/rf_joint2_position_controller/command', 10),
#             'rb_joint1': self.create_publisher(Float64, '/rb_joint1_position_controller/command', 10),
#             'rb_joint2': self.create_publisher(Float64, '/rb_joint2_position_controller/command', 10),
#         }

#         self.timer = self.create_timer(5.0, self.trot_forward)  # Run once after 5s startup

#     def publish(self, joint, pos):
#         msg = Float64()
#         msg.data = pos
#         self.joints[joint].publish(msg)

#     def trot_forward(self):
#         self.get_logger().info('Starting trot sequence...')

#         # Example positions -- these should be tuned to your robot's motion range
#         positions = {
#             'lf_joint1': 0.5,
#             'lf_joint2': -0.5,
#             'lb_joint1': 0.5,
#             'lb_joint2': -0.5,
#             'rf_joint1': -0.5,
#             'rf_joint2': 0.5,
#             'rb_joint1': -0.5,
#             'rb_joint2': 0.5,
#         }

#         for joint, pos in positions.items():
#             self.publish(joint, pos)
#         self.get_logger().info('Published trot pose.')

#         # Optionally reset after delay
#         time.sleep(2.0)
#         for joint in self.joints:
#             self.publish(joint, 0.0)
#         self.get_logger().info('Returned to neutral pose.')


# def main(args=None):
#     rclpy.init(args=args)
#     node = PuppyWalker()
#     rclpy.spin(node)
#     node.destroy_node()
#     rclpy.shutdown()


# if __name__ == '__main__':
#     main()
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import movement

class MotionCommandNode(Node):
    def __init__(self):
        super().__init__('puppy_motion_node')
        self.subscriber = self.create_subscription(
            String,
            '/puppy_motion_command',
            self.command_callback,
            10
        )
        self.get_logger().info('Motion Command Node ready.')

    def command_callback(self, msg):
        command = msg.data.lower()
        self.get_logger().info(f'Received command: {command}')

        if command == 'walk':
            movement.trot_forward()
        elif command == 'turn_left':
            movement.turn_left()
        elif command == 'stand':
            movement.stand()
        else:
            self.get_logger().warn(f'Unknown command: {command}')

def main():
    rclpy.init()
    node = MotionCommandNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
        
        