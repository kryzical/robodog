#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import LaserScan
import math

class ScanSimulator:
    def __init__(self,name):
    
    
        self.name = name
        rospy.init_node(self.name, anonymous=True)
        self.scan_msg = LaserScan()
        self.scan_msg.ranges = [0]*360
        self.scan_msg.intensities = [0]*360
        self.scan_msg.header.frame_id = 'base_link'  

        self.scan_msg.angle_min = -1.57
        self.scan_msg.angle_max = 1.57
        self.scan_msg.angle_increment = 3.14*2 / 360
        self.scan_msg.time_increment = (1 / 100) / (360)
        self.scan_msg.range_min = 0.0
        self.scan_msg.range_max = 100.0  

    def pub(self):
        self.scan_msg.header.stamp=rospy.Time.now()
        for x in range(0,360):
            self.scan_msg.ranges[x]=1
            self.scan_msg.intensities[x]=1
        scan_publisher.publish(self.scan_msg)
    
if __name__ == '__main__':
    
    try:
        
        scan_publisher = rospy.Publisher('/scan', LaserScan, queue_size=10)
        
        
        while not rospy.is_shutdown():
            ScanSimulator('radar_simulator').pub()
            rospy.sleep(0.01)
    except rospy.ROSInterruptException:
        pass