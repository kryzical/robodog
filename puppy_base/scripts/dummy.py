#!/usr/bin/env python3
# coding=utf8

import sys
import math
import rospy
from std_msgs.msg import Float64
import time

class PuppyController:
    def __init__(self):
        rospy.init_node('puppy_demo', anonymous=True)
        
        # Initialize publishers for each joint
        self.joints = {
            'lf_1': rospy.Publisher('/puppy/joint2_position_controller/command', Float64, queue_size=1),
            'lf_2': rospy.Publisher('/puppy/joint6_position_controller/command', Float64, queue_size=1),
            'rf_1': rospy.Publisher('/puppy/joint1_position_controller/command', Float64, queue_size=1),
            'rf_2': rospy.Publisher('/puppy/joint5_position_controller/command', Float64, queue_size=1),
            'lb_1': rospy.Publisher('/puppy/joint4_position_controller/command', Float64, queue_size=1),
            'lb_2': rospy.Publisher('/puppy/joint8_position_controller/command', Float64, queue_size=1),
            'rb_1': rospy.Publisher('/puppy/joint3_position_controller/command', Float64, queue_size=1),
            'rb_2': rospy.Publisher('/puppy/joint7_position_controller/command', Float64, queue_size=1)
        }
        
        # Initial standing position (less aggressive angles to prevent flipping)
        self.stand_pos = {
            'lf_1': -0.1,
            'lf_2': 0.3,
            'rf_1': -0.1,
            'rf_2': 0.3,
            'lb_1': -0.1,
            'lb_2': 0.3,
            'rb_1': -0.1,
            'rb_2': 0.3
        }
        
        # Different gait configurations
        self.gaits = {
            'Trot': {
                'overlap_time': 0.2,
                'swing_time': 0.3,
                'pairs': [
                    {'up': ['rf_1', 'lb_1'], 'down': ['lf_1', 'rb_1']},
                    {'up': ['lf_1', 'rb_1'], 'down': ['rf_1', 'lb_1']}
                ],
                'step_height': 0.2
            },
            'Walk': {
                'overlap_time': 0.1,
                'swing_time': 0.2,
                'pairs': [
                    {'up': ['rf_1'], 'down': ['lf_1', 'rb_1', 'lb_1']},
                    {'up': ['lf_1'], 'down': ['rf_1', 'rb_1', 'lb_1']},
                    {'up': ['rb_1'], 'down': ['rf_1', 'lf_1', 'lb_1']},
                    {'up': ['lb_1'], 'down': ['rf_1', 'lf_1', 'rb_1']}
                ],
                'step_height': 0.15
            }
        }
        
        self.current_gait = 'Trot'
        rospy.sleep(1)  # Allow publishers to initialize

    def move_joints(self, positions, duration=0.5):
        """Smoothly move joints to target positions"""
        steps = 10
        rate = rospy.Rate(steps/duration)
        
        start_pos = self.get_current_positions()
        
        for i in range(steps + 1):
            if rospy.is_shutdown():
                return
                
            # Interpolate between start and target positions
            ratio = i / steps
            current = {}
            for joint in self.joints.keys():
                if joint in positions:
                    current[joint] = start_pos[joint] + (positions[joint] - start_pos[joint]) * ratio
                else:
                    current[joint] = start_pos[joint]
            
            # Publish positions
            for joint, pos in current.items():
                self.joints[joint].publish(Float64(pos))
            
            rate.sleep()

    def get_current_positions(self):
        """Get current joint positions (simplified - returns standing position)"""
        return self.stand_pos.copy()

    def stand(self):
        """Move to standing position"""
        rospy.loginfo("Standing up...")
        self.move_joints(self.stand_pos, duration=1.0)
        rospy.sleep(0.5)

    def step_cycle(self, gait_config):
        """Execute one step cycle of the selected gait"""
        for pair in gait_config['pairs']:
            positions = self.stand_pos.copy()
            
            # Lift legs
            for joint in pair['up']:
                positions[joint] = self.stand_pos[joint] - gait_config['step_height']
                positions[joint.replace('1', '2')] = self.stand_pos[joint.replace('1', '2')] + gait_config['step_height']
            
            # Ground legs
            for joint in pair['down']:
                positions[joint] = self.stand_pos[joint] + 0.05
                positions[joint.replace('1', '2')] = self.stand_pos[joint.replace('1', '2')] - 0.05
            
            self.move_joints(positions, duration=gait_config['swing_time'])
            rospy.sleep(gait_config['overlap_time'])

    def walk(self, steps=4):
        """Perform walking motion with selected gait"""
        rospy.loginfo(f"Starting {self.current_gait} gait...")
        
        try:
            for _ in range(steps):
                if rospy.is_shutdown():
                    return
                self.step_cycle(self.gaits[self.current_gait])
        except KeyboardInterrupt:
            self.stand()
            rospy.signal_shutdown("Manual interrupt")

    def cleanup(self):
        """Return to standing position before shutdown"""
        self.stand()

if __name__ == '__main__':
    try:
        controller = PuppyController()
        controller.stand()
        rospy.sleep(1)  # Ensure stability before walking
        controller.walk(steps=6)
        controller.stand()
    except rospy.ROSInterruptException:
        pass