# import rclpy 
# from rclpy.node import Node 
# import cv2
# import numpy as np 
# import pygame

# def main():
#     # print('hello')
#     cap = cv2.VideoCapture(0)
#     global WIDTH
#     global HEIGHT
#     global movement_states
#     WIDTH = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#     HEIGHT = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#     window = pygame.display.set_mode((WIDTH,HEIGHT))
#     pygame.display.set_caption("Camera Feed")

#     while True:
#         ret, frame = cap.read()
#         frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0,1))
#         window.blit(frame_surface, (0, 0))
#         pygame.display.update()

# if __name__ == "__main__":
#     main()

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
from ultralytics import YOLO

class CameraInputNode(Node):
    def __init__(self):
        super().__init__('camera_input_node')
        self.subscription = self.create_subscription(
            Image,
            '/image_raw',
            self.listener_callback,
            10
        )
        self.bridge = CvBridge()
        self.model = YOLO('yolov8n.pt')  # Use 'yolov5s.pt' or custom model if needed
        self.get_logger().info('YOLO camera input node started.')

    def listener_callback(self, msg):
        # Convert ROS Image to OpenCV image
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        small_frame = cv2.resize(frame, (320, 240))
        results = self.model(frame)

        # Draw detections
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                label = result.names[int(box.cls[0])]
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
                cv2.putText(frame, label, (x1, y1-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)

        # (Optional) Show result in debug
        cv2.imshow('YOLO Detection', frame)
        cv2.waitKey(1)

def main(args=None):
    rclpy.init(args=args)
    node = CameraInputNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
