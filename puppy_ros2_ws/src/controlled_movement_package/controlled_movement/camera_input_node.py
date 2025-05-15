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
            '/camera/image_raw',  # <-- correct topic name
            self.listener_callback,
            10
        )
        self.publisher = self.create_publisher(Image, '/camera/yolo_annotated', 10)
        self.bridge = CvBridge()
        self.model = YOLO('yolov8n.pt')
        self.get_logger().info('YOLO camera input node started.')

    def listener_callback(self, msg):
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        results = self.model(frame)

        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                label = result.names[int(box.cls[0])]
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Show locally for debug
        cv2.imshow('YOLO Detection', frame)
        cv2.waitKey(1)

        # Publish to topic
        msg_out = self.bridge.cv2_to_imgmsg(frame, encoding='bgr8')
        self.publisher.publish(msg_out)

def main(args=None):
    rclpy.init(args=args)
    node = CameraInputNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()



# import rclpy
# from rclpy.node import Node
# from sensor_msgs.msg import Image
# from cv_bridge import CvBridge, CvBridgeError
# import cv2
# from ultralytics import YOLO
# from multiprocessing import Process, Queue
# import numpy as np
# import signal
# import sys

# class YOLOProcessor(Process):
#     def __init__(self, input_queue, output_queue):
#         super().__init__()
#         self.input_queue = input_queue
#         self.output_queue = output_queue
#         self.model = YOLO('yolov8n.pt')
#         self.bridge = CvBridge()

#     def run(self):
#         while True:
#             frame = self.input_queue.get()
#             if frame is None:
#                 break

#             results = self.model(frame, verbose=False)
#             for result in results:
#                 for box in result.boxes:
#                     x1, y1, x2, y2 = map(int, box.xyxy[0])
#                     label = result.names[int(box.cls[0])]
#                     cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
#                     cv2.putText(frame, label, (x1, y1 - 10),
#                                 cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

#             self.output_queue.put(frame)


# class CameraInputNode(Node):
#     def __init__(self):
#         super().__init__('camera_input_node')

#         # Queues for multiprocessing
#         self.input_queue = Queue(maxsize=1)
#         self.output_queue = Queue(maxsize=1)

#         # Start YOLO processor
#         self.processor = YOLOProcessor(self.input_queue, self.output_queue)
#         self.processor.start()

#         # ROS subscribers and publishers
#         from rclpy.qos import QoSProfile, QoSReliabilityPolicy
#         qos = QoSProfile(depth=1, reliability=QoSReliabilityPolicy.BEST_EFFORT)

#         self.subscription = self.create_subscription(
#             Image,
#             '/camera/image_raw',
#             self.listener_callback,
#             qos
#         )

#         self.publisher_ = self.create_publisher(Image, '/camera/yolo_annotated', 10)
#         self.bridge = CvBridge()
#         self.timer = self.create_timer(0.05, self.publish_annotated_image)  # ~20Hz
#         self.get_logger().info('CameraInputNode with multiprocessing YOLO started.')

#     def listener_callback(self, msg):
#         try:
#             frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
#             small_frame = cv2.resize(frame, (320, 240))
#             if self.input_queue.full():
#                 return  # Skip if busy
#             self.input_queue.put_nowait(small_frame)
#         except CvBridgeError as e:
#             self.get_logger().error(f'CvBridge Error: {e}')

#     def publish_annotated_image(self):
#         if not self.output_queue.empty():
#             frame = self.output_queue.get_nowait()
#             try:
#                 msg = self.bridge.cv2_to_imgmsg(frame, encoding='bgr8')
#                 self.publisher_.publish(msg)
#             except CvBridgeError as e:
#                 self.get_logger().error(f'Publish Error: {e}')

#     def destroy_node(self):
#         self.input_queue.put(None)  # Stop the process
#         self.processor.join()
#         super().destroy_node()


# def main(args=None):
#     rclpy.init(args=args)
#     node = CameraInputNode()
    
#     try:
#         rclpy.spin(node)
#     except KeyboardInterrupt:
#         node.get_logger().info('Shutting down...')
#     finally:
#         node.destroy_node()
#         rclpy.shutdown()
