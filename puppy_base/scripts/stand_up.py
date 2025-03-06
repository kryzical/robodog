#!/usr/bin/env python3
# coding=utf-8
# filepath: /home/brian/robodog2/puppy_base/scripts/stand_up.py

import rospy
import sys
import time
import math
from std_msgs.msg import Float64

class PuppyStander:
    def __init__(self):
        rospy.init_node('puppy_stand', log_level=rospy.INFO)
        
        # Define joint publishers - arranged by leg
        self.pubs = {}
        
        # Right front leg
        self.pubs['rf_hip'] = rospy.Publisher('/puppy/joint1_position_controller/command', Float64, queue_size=1)
        self.pubs['rf_knee'] = rospy.Publisher('/puppy/joint5_position_controller/command', Float64, queue_size=1)
        
        # Left front leg
        self.pubs['lf_hip'] = rospy.Publisher('/puppy/joint2_position_controller/command', Float64, queue_size=1)
        self.pubs['lf_knee'] = rospy.Publisher('/puppy/joint6_position_controller/command', Float64, queue_size=1)
        
        # Right back leg
        self.pubs['rb_hip'] = rospy.Publisher('/puppy/joint3_position_controller/command', Float64, queue_size=1)
        self.pubs['rb_knee'] = rospy.Publisher('/puppy/joint7_position_controller/command', Float64, queue_size=1)
        
        # Left back leg
        self.pubs['lb_hip'] = rospy.Publisher('/puppy/joint4_position_controller/command', Float64, queue_size=1)
        self.pubs['lb_knee'] = rospy.Publisher('/puppy/joint8_position_controller/command', Float64, queue_size=1)
        
        # Wait for publishers to connect
        rospy.sleep(1.0)
    
    def send_commands(self, positions):
        """Send commands to all joints"""
        for joint, pos in positions.items():
            if joint in self.pubs:
                self.pubs[joint].publish(Float64(pos))

    def stand(self):
        """RADICAL NEW APPROACH - Front-first strategy"""
        print("Starting RADICAL stand up sequence...")
        rate = rospy.Rate(10)
        
        # FRONT PLANT POSITION
        # Get front legs far forward, back legs tucked
        front_plant = {
            'rf_hip': -1.0, 'rf_knee': 0.6,  # Way forward, moderate bend
            'lf_hip': -1.0, 'lf_knee': 0.6,  # Way forward, moderate bend
            'rb_hip': 1.0, 'rb_knee': 1.5,   # Way back, very bent
            'lb_hip': 1.0, 'lb_knee': 1.5    # Way back, very bent
        }
        
        print("Setting front plant position...")
        steps = 20
        for i in range(steps):
            # Start from neutral and move to front plant
            positions = {}
            for joint in self.pubs:
                if i == 0:  # First step - neutral position
                    if 'hip' in joint:
                        positions[joint] = 0.0
                    else:  # knee
                        positions[joint] = 0.7
                else:  # Moving to front plant
                    current = positions[joint] if joint in positions else 0.0
                    target = front_plant[joint]
                    positions[joint] = current + (target - current) * i/(steps-1)
                
            self.send_commands(positions)
            rate.sleep()
        
        # Hold front plant position
        for _ in range(15):
            self.send_commands(front_plant)
            rate.sleep()
            
        print("INITIATING CRAWL-FORWARD MOTION...")
        
        # CRAWL FORWARD - Extreme front leg push
        crawl_forward = {
            'rf_hip': -0.8, 'rf_knee': 0.1,  # Very forward, almost straight
            'lf_hip': -0.8, 'lf_knee': 0.1,  # Very forward, almost straight
            'rb_hip': 1.0, 'rb_knee': 1.5,   # No change
            'lb_hip': 1.0, 'lb_knee': 1.5    # No change
        }
        
        steps = 15
        for i in range(steps):
            positions = {}
            for joint in front_plant:
                current = front_plant[joint]
                target = crawl_forward[joint]
                positions[joint] = current + (target - current) * i/steps
                
            self.send_commands(positions)
            rate.sleep()
        
        print("PUSHING UP WITH BACK LEGS...")
        
        # BACK LEG PUSH - Now push with back legs
        back_push = {
            'rf_hip': -0.8, 'rf_knee': 0.1,  # No change
            'lf_hip': -0.8, 'lf_knee': 0.1,  # No change
            'rb_hip': 0.8, 'rb_knee': 0.2,   # Straighter, still back
            'lb_hip': 0.8, 'lb_knee': 0.2    # Straighter, still back
        }
        
        steps = 20 
        for i in range(steps):
            positions = {}
            for joint in crawl_forward:
                current = crawl_forward[joint]
                target = back_push[joint]
                positions[joint] = current + (target - current) * i/steps
                
            self.send_commands(positions)
            rate.sleep()
        
        print("ALIGNING TO STANDING POSITION...")
        
        # FINAL ALIGNMENT
        final_positions = {
            'rf_hip': -0.5, 'rf_knee': 0.4,  # More balanced position
            'lf_hip': -0.5, 'lf_knee': 0.4,  # More balanced position
            'rb_hip': 0.5, 'rb_knee': 0.4,   # More balanced position
            'lb_hip': 0.5, 'lb_knee': 0.4    # More balanced position
        }
        
        steps = 20
        for i in range(steps):
            positions = {}
            for joint in back_push:
                current = back_push[joint]
                target = final_positions[joint]
                positions[joint] = current + (target - current) * i/steps
                
            self.send_commands(positions)
            rate.sleep()
        
        print("Standing position reached - maintaining...")
        
        # Maintain this position indefinitely
        while not rospy.is_shutdown():
            self.send_commands(final_positions)
            rate.sleep()


def main():
    try:
        stander = PuppyStander()
        stander.stand()
    except Exception as e:
        rospy.logerr(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()