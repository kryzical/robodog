#!/usr/bin/env python3
# coding=utf8
"""
Position Stabilizer for Puppy Robot

This script maintains a stable standing position for the puppy robot
by continuously publishing joint positions to prevent drift.

Usage:
    rosrun puppy_base position_stabilizer.py
"""
import rospy
import time
from std_msgs.msg import Float64

# Import standardized joint definitions
from puppy_base.scripts import JOINT_CONTROLLERS, DEFAULT_STAND_POSITION

class PositionStabilizer:
    def __init__(self):
        rospy.init_node('position_stabilizer')
        
        # Define joint publishers using standardized controllers
        self.pubs = {}
        for joint_name, controller in JOINT_CONTROLLERS.items():
            self.pubs[joint_name] = rospy.Publisher(controller, Float64, queue_size=1)
        
        # Wait for publishers to connect
        rospy.sleep(1.0)
        
        # Use the standardized default stand position
        self.positions = DEFAULT_STAND_POSITION.copy()
        
    def run(self):
        """Run the stabilizer to maintain position"""
        rate = rospy.Rate(20)  # 20Hz to maintain position
        
        rospy.loginfo("Starting position stabilization")
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