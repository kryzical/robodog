#!/usr/bin/env python3
# encoding: utf-8
# Date:2021/10/25
# Author:aiden
import cv2
import rospy
import numpy as np
from sensor_msgs.msg import Image
from PyQt5.QtCore import QThread, pyqtSignal

class ROS_Camera(QThread):
    raw_data = pyqtSignal(np.ndarray)

    def __init__(self, image_topic):
        super(ROS_Camera, self).__init__()
        
        self.image = None
        self.image_sub = None
        self.running = False
        self.image_topic = image_topic

    def enter(self):
        self.running = True
        self.image_sub = rospy.Subscriber(self.image_topic, Image, self.get_ros_image)  # 订阅目标检测节点(subscribe target detection node)
    
    def exit(self):
        self.running = False
        self.image = None
        if self.image_sub is not None:
            self.image_sub.unregister()

    def get_ros_image(self, ros_image):
        self.image = np.ndarray(shape=(ros_image.height, ros_image.width, 3), dtype=np.uint8, buffer=ros_image.data)  # 将自定义图像消息转化为图像(convert the customized image information to image)
        
    def run(self):
        while self.running:
            if self.image is not None:
                self.raw_data.emit(self.image)
                rospy.sleep(0.03)

class OpenCV_Camera(QThread):
    raw_data = pyqtSignal(np.ndarray)

    def __init__(self, port):
        super(OpenCV_Camera, self).__init__()
        
        self.port = port
        self.running = False
        self.camera = None 

    def open(self):
        self.camera = cv2.VideoCapture(self.port)
        self.running = True
    
    def close(self):
        self.running = False
        rospy.sleep(0.2)
        if self.camera is not None:
            self.camera.release()
    
    def run(self):
        while self.running:
            ret, image = self.camera.read()
            if ret:
                self.raw_data.emit(cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
                rospy.sleep(0.01)
