import rclpy
from rclpy.node import Node
import pygame
import threading
from std_msgs.msg import Int32MultiArray

class Talker(Node):
    def __init__(self):
        super().__init__('pygame_node')
        self.publisher_ = self.create_publisher(Int32MultiArray, 'command_topic', 10)
        self.timer = self.create_timer(.00005, self.publish_callback)

    def publish_callback(self):
        msg = Int32MultiArray()
        msg.data = movement_states
        self.publisher_.publish(msg)
        self.get_logger().info(f"Publishing: {msg.data}")

class KeyHandler(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        movement_states[0] = 1
                    if event.key == pygame.K_a:
                        movement_states[2] = 1
                    if event.key == pygame.K_d:
                        movement_states[3] = 1
                    if event.key == pygame.K_s:
                        movement_states[1] = 1
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        movement_states[0] = 0
                    if event.key == pygame.K_a:
                        movement_states[2] = 0
                    if event.key == pygame.K_d:
                        movement_states[3] = 0
                    if event.key == pygame.K_s:
                        movement_states[1] = 0
                # print(movement_states)
                
class Node_thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        args=None
        rclpy.init(args=args)
        movement_node = Talker()
        rclpy.spin(movement_node)
        movement_node.destroy_node()
        rclpy.shutdown()

def main():
    global WIDTH
    global HEIGHT
    global movement_states
    WIDTH = 800
    HEIGHT = 800
    movement_states = [0,0,0,0] #[up, down, left, right]

    pygame.display.set_mode((WIDTH,HEIGHT))

    key_handler_thread = KeyHandler()
    node = Node_thread()

    key_handler_thread.start()
    node.start()

    key_handler_thread.join()
    node.join()

if __name__ == "__main__":
    main()
