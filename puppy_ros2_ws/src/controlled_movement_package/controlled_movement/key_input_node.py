#import rclpy
#from rclpy.node import Node
#import pygame
#import threading
#from std_msgs.msg import Int32MultiArray
#
#class Talker(Node):
#    def __init__(self):
#        super().__init__('pygame_node')
#        self.publisher_ = self.create_publisher(Int32MultiArray, 'command_topic', 10)
#        self.timer = self.create_timer(.00005, self.publish_callback)
#
#    def publish_callback(self):
#        msg = Int32MultiArray()
#        msg.data = movement_states
#        self.publisher_.publish(msg)
#        self.get_logger().info(f"Publishing: {msg.data}")
#
#class KeyHandler(threading.Thread):
#    def __init__(self):
#        threading.Thread.__init__(self)
#
#    def run(self):
#        while True:
#            for event in pygame.event.get():
#                if event.type == pygame.QUIT:
#                    running = False
#                elif event.type == pygame.KEYDOWN:
#                    if event.key == pygame.K_w:
#                        movement_states[0] = 1
#                    if event.key == pygame.K_a:
#                        movement_states[2] = 1
#                    if event.key == pygame.K_d:
#                        movement_states[3] = 1
#                    if event.key == pygame.K_s:
#                        movement_states[1] = 1
#                elif event.type == pygame.KEYUP:
#                    if event.key == pygame.K_w:
#                        movement_states[0] = 0
#                    if event.key == pygame.K_a:
#                        movement_states[2] = 0
#                    if event.key == pygame.K_d:
#                        movement_states[3] = 0
#                    if event.key == pygame.K_s:
#                        movement_states[1] = 0
#                # print(movement_states)
#                
#class Node_thread(threading.Thread):
#    def __init__(self):
#        threading.Thread.__init__(self)
#    def run(self):
#        args=None
#        rclpy.init(args=args)
#        movement_node = Talker()
#        rclpy.spin(movement_node)
#        movement_node.destroy_node()
#        rclpy.shutdown()
#
#def main():
#    global WIDTH
#    global HEIGHT
#    global movement_states
#    WIDTH = 800
#    HEIGHT = 800
#    movement_states = [0,0,0,0] #[up, down, left, right]
#
#    pygame.display.set_mode((WIDTH,HEIGHT))
#
#    key_handler_thread = KeyHandler()
#    node = Node_thread()
#
#    key_handler_thread.start()
#    node.start()
#
#    key_handler_thread.join()
#    node.join()
#
#if __name__ == "__main__":
#    main()



import rclpy
from rclpy.node import Node
import pygame
import multiprocessing
from std_msgs.msg import Int32MultiArray

class Talker(Node):
    def __init__(self, shared_array):
        super().__init__('pygame_node')
        self.shared_array = shared_array
        self.publisher_ = self.create_publisher(Int32MultiArray, 'command_topic', 10)
        self.timer = self.create_timer(0.05, self.publish_callback)  # 20Hz

    def publish_callback(self):
        msg = Int32MultiArray()
        msg.data = list(self.shared_array)
        self.publisher_.publish(msg)
        self.get_logger().info(f"Publishing: {msg.data}")

def ros_process(shared_array):
    rclpy.init()
    node = Talker(shared_array)
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

def pygame_process(shared_array):
    pygame.init()
    pygame.joystick.init()
    WIDTH, HEIGHT = 800, 800
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pygame ROS2 Joystick Controller")

    clock = pygame.time.Clock()
    running = True

    # Initialize joystick if available
    joystick = None
    if pygame.joystick.get_count() > 0:
        joystick = pygame.joystick.Joystick(0) #initializes joystick, 0 is for left, 1 is for right
        joystick.init()
        print(f"Joystick connected: {joystick.get_name()}")

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            #Keyboard input fallback
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    shared_array[0] = 1
                if event.key == pygame.K_s:
                    shared_array[1] = 1
                if event.key == pygame.K_a:
                    shared_array[2] = 1
                if event.key == pygame.K_d:
                    shared_array[3] = 1

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    shared_array[0] = 0
                if event.key == pygame.K_s:
                    shared_array[1] = 0
                if event.key == pygame.K_a:
                    shared_array[2] = 0
                if event.key == pygame.K_d:
                    shared_array[3] = 0
        # Joystick input
        if joystick:
            axis_0 = joystick.get_axis(0)  # Left-right
            axis_1 = joystick.get_axis(1)  # Up-down

            threshold = 0.2

            # Apply only if joystick movement detected
            if abs(axis_1) > threshold:
                shared_array[0] = 1 if axis_1 < -threshold else 0
                shared_array[1] = 1 if axis_1 > threshold else 0
            else:
                shared_array[0] = 0
                shared_array[1] = 0

            if abs(axis_0) > threshold:
                shared_array[2] = 1 if axis_0 < -threshold else 0
                shared_array[3] = 1 if axis_0 > threshold else 0
            else:
                shared_array[2] = 0
                shared_array[3] = 0

        screen.fill((0, 0, 0))
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

def main():
    shared_array = multiprocessing.Array('i', [0, 0, 0, 0])  # [up, down, left, right]

    ros_node = multiprocessing.Process(target=ros_process, args=(shared_array,))
    pygame_node = multiprocessing.Process(target=pygame_process, args=(shared_array,))

    ros_node.start()
    pygame_node.start()

    pygame_node.join()
    ros_node.terminate()

if __name__ == '__main__':
    multiprocessing.set_start_method('spawn')
    main()
