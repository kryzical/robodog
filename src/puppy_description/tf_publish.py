#!/usr/bin/python3
# coding=utf8
# Date:2022/02/17
# Author:Aiden
import rospy
import tf2_ros
from math import *
import numpy as np
from std_msgs.msg import Header
from geometry_msgs.msg import PoseStamped

if __name__ == '__main__':
    rospy.init_node('obj2base')
    tfBuffer = tf2_ros.Buffer()
    listener = tf2_ros.TransformListener(tfBuffer)
    pose_publish = rospy.Publisher('/target/pose', PoseStamped, queue_size=1)
    
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        try:
            trans = tfBuffer.lookup_transform('base_link', 'lf_link3', rospy.Time())
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
            rate.sleep()
            continue
        
        msg = PoseStamped()
        msg.header = Header(stamp=rospy.Time.now())
        msg.header.frame_id = 'target_frame'
        msg.pose.position = trans.transform.translation
        msg.pose.orientation = trans.transform.rotation
        pose_publish.publish(msg)
        rate.sleep()
