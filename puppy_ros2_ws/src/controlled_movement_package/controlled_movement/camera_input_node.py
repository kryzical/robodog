# import rclpy
# from rclpy.node import Node
# from sensor_msgs.msg import Image
# from cv_bridge import CvBridge
# import cv2
# from ultralytics import YOLO

# class CameraInputNode(Node):
#     def __init__(self):
#         super().__init__('camera_input_node')

#         self.bridge = CvBridge()
#         self.model = YOLO('yolov8n.pt')

#         # Subscribe to the original working topic name
#         self.subscription = self.create_subscription(
#             Image,
#             '/image_raw',  
#             self.listener_callback,
#             10
#         )

#         # Publisher to annotated topic
#         self.publisher = self.create_publisher(Image, '/yolo_annotated', 10)

#         self.get_logger().info('YOLO camera input node started.')

#     def listener_callback(self, msg):
#         # Convert incoming ROS image to OpenCV format
#         frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

#         # Run YOLO inference
#         results = self.model(frame)

#         # Draw detection boxes and labels
#         for result in results:
#             for box in result.boxes:
#                 x1, y1, x2, y2 = map(int, box.xyxy[0])
#                 label = result.names[int(box.cls[0])]
#                 cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
#                 cv2.putText(frame, label, (x1, y1 - 10),
#                             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

#         # Convert to RGB for rqt_image_view
#         frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         msg_out = self.bridge.cv2_to_imgmsg(frame_rgb, encoding='rgb8')
#         msg_out.header.stamp = msg.header.stamp
#         msg_out.header.frame_id = 'camera_frame'

#         # Publish annotated image
#         self.publisher.publish(msg_out)

#         # (Optional) Visualize locally
#         cv2.imshow('YOLO Detection', frame)
#         cv2.waitKey(1)

# def main(args=None):
#     rclpy.init(args=args)
#     node = CameraInputNode()
#     rclpy.spin(node)
#     node.destroy_node()
#     rclpy.shutdown()


import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
from multiprocessing import Process, Queue
import numpy as np
from ultralytics import YOLO
import time

# === Child Process: YOLO + Annotator ===
def yolo_worker(input_queue: Queue, output_queue: Queue):
    model = YOLO('yolov8n.pt')
    while True:
        try:
            frame = input_queue.get()
            if frame is None:
                break  # Graceful shutdown
            results = model(frame)

            for result in results:
                for box in result.boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    label = result.names[int(box.cls[0])]
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, label, (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            output_queue.put(frame)

        except Exception as e:
            print(f"[YOLO Worker] Error: {e}")

# === ROS Node ===
class CameraInputNode(Node):
    def __init__(self, input_queue, output_queue):
        super().__init__('camera_input_node')
        self.bridge = CvBridge()
        self.input_queue = input_queue
        self.output_queue = output_queue

        self.subscription = self.create_subscription(
            Image,
            '/image_raw',
            self.listener_callback,
            10
        )

        self.publisher = self.create_publisher(Image, '/yolo_annotated', 10)

        # Timer to poll the output queue and publish
        self.timer = self.create_timer(0.05, self.publish_from_queue)

        self.get_logger().info('YOLO camera input node with multiprocessing started.')

    def listener_callback(self, msg):
        try:
            frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
            if not self.input_queue.full():
                self.input_queue.put(frame)
        except Exception as e:
            self.get_logger().error(f"Failed to process frame: {e}")

    def publish_from_queue(self):
        if not self.output_queue.empty():
            try:
                frame = self.output_queue.get()
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                msg_out = self.bridge.cv2_to_imgmsg(frame_rgb, encoding='rgb8')
                msg_out.header.stamp = self.get_clock().now().to_msg()
                msg_out.header.frame_id = 'camera_frame'
                self.publisher.publish(msg_out)

                # Optional local visualization
                cv2.imshow('YOLO Detection (Multiprocessing)', frame)
                cv2.waitKey(1)
            except Exception as e:
                self.get_logger().error(f"Failed to publish frame: {e}")

def main(args=None):
    import multiprocessing as mp
    mp.set_start_method('spawn')  # Important for YOLO

    input_queue = mp.Queue(maxsize=2)
    output_queue = mp.Queue(maxsize=2)

    yolo_process = Process(target=yolo_worker, args=(input_queue, output_queue))
    yolo_process.start()

    rclpy.init(args=args)
    node = CameraInputNode(input_queue, output_queue)
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
        input_queue.put(None)  # Signal child process to stop
        yolo_process.join()
