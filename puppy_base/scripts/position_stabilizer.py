#!/usr/bin/env python3
# coding=utf8

import rospy
import time
from std_msgs.msg import Float64

class PositionStabilizer:
    def __init__(self):
        rospy.init_node('position_stabilizer')
        
        # Define joint publishers
        self.pubs = {}
        self.pubs['rf_hip'] = rospy.Publisher('/puppy/joint1_position_controller/command', Float64, queue_size=1)
        self.pubs['rf_knee'] = rospy.Publisher('/puppy/joint5_position_controller/command', Float64, queue_size=1)
        self.pubs['lf_hip'] = rospy.Publisher('/puppy/joint2_position_controller/command', Float64, queue_size=1)
        self.pubs['lf_knee'] = rospy.Publisher('/puppy/joint6_position_controller/command', Float64, queue_size=1)
        self.pubs['rb_hip'] = rospy.Publisher('/puppy/joint3_position_controller/command', Float64, queue_size=1)
        self.pubs['rb_knee'] = rospy.Publisher('/puppy/joint7_position_controller/command', Float64, queue_size=1)
        self.pubs['lb_hip'] = rospy.Publisher('/puppy/joint4_position_controller/command', Float64, queue_size=1)
        self.pubs['lb_knee'] = rospy.Publisher('/puppy/joint8_position_controller/command', Float64, queue_size=1)
        
        # Wait for publishers to connect
        rospy.sleep(1.0)
        
        self.positions = {
            'rf_hip': -0.4, 'rf_knee': 1.2,
            'lf_hip': -0.4, 'lf_knee': 1.2,
            'rb_hip': 0.4, 'rb_knee': 1.2,
            'lb_hip': 0.4, 'lb_knee': 1.2
        }
        
    def run(self):
        rate = rospy.Rate(20)  # 20Hz to maintain position
        
        print("Starting position stabilization")
        while not rospy.is_shutdown():
            # Continuously publish positions to maintain stability
            for joint, pos in self.positions.items():
                self.pubs[joint].publish(Float64(pos))
            rate.sleep()

if __name__ == '__main__':
    try:
        stabilizer = PositionStabilizer()
        stabilizer.run()
    except rospy.ROSInterruptException:
        pass