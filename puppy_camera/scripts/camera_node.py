#!/usr/bin/env python3

import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import numpy as np

class CameraNode:
    def __init__(self):
        # Initialize the ROS node
        rospy.init_node('camera_node', anonymous=True)
        
        # Get parameters
        self.camera_device_id = rospy.get_param('~camera_device_id', 0)
        self.frame_rate = rospy.get_param('~frame_rate', 30)
        self.frame_id = rospy.get_param('~frame_id', 'camera_link')
        
        # Initialize OpenCV video capture
        self.cap = cv2.VideoCapture(self.camera_device_id)
        if not self.cap.isOpened():
            rospy.logerr(f"Could not open camera with device ID {self.camera_device_id}")
            return
        
        # Set camera properties
        self.cap.set(cv2.CAP_PROP_FPS, self.frame_rate)
        
        # Initialize the CvBridge
        self.bridge = CvBridge()
        
        # Create an image publisher
        self.image_pub = rospy.Publisher('camera/image_raw', Image, queue_size=1)
        
        rospy.loginfo("Camera node started. Publishing to camera/image_raw topic.")
        
        # Create a timer to capture and publish frames
        self.timer = rospy.Timer(rospy.Duration(1.0/self.frame_rate), self.capture_and_publish)
        
    def capture_and_publish(self, event):
        # Capture a frame
        ret, frame = self.cap.read()
        
        if ret:
            try:
                # Convert OpenCV image to ROS message
                img_msg = self.bridge.cv2_to_imgmsg(frame, "bgr8")
                img_msg.header.stamp = rospy.Time.now()
                img_msg.header.frame_id = self.frame_id
                
                # Publish the image
                self.image_pub.publish(img_msg)
            except CvBridgeError as e:
                rospy.logerr(f"CvBridge Error: {e}")
    
    def __del__(self):
        # Clean up
        if hasattr(self, 'cap') and self.cap.isOpened():
            self.cap.release()

if __name__ == '__main__':
    try:
        camera_node = CameraNode()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass