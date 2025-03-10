#!/usr/bin/env python3
# coding=utf8
"""
Script to make the puppy robot stand up on all four legs.
Uses the common robot controller library for joint control.
"""

import rospy
import math
from robot_controller_lib import PuppyJointController

class PuppyStander(PuppyJointController):
    def __init__(self):
        """Initialize the stander controller"""
        super().__init__(node_name='puppy_stand')
    
    def stand(self):
        """Execute standing sequence using inverse kinematics"""
        print("Starting stand up sequence...")
        
        # Initial position - legs slightly tucked
        x = -0.05  # Slightly back
        y = 0
        z = -0.15  # Start with legs extended down
        
        # Calculate angles for front and back legs separately
        front_hip, front_knee = self.calculate_leg_ik(x, y, z, is_front=True)
        back_hip, back_knee = self.calculate_leg_ik(x, y, z, is_front=False)
        
        # Create positions dictionary with different angles for front/back
        initial_positions = {
            'rf_hip': front_hip, 'rf_knee': front_knee,
            'lf_hip': front_hip, 'lf_knee': front_knee,
            'rb_hip': back_hip, 'rb_knee': back_knee,
            'lb_hip': back_hip, 'lb_knee': back_knee
        }
        
        # Reset to neutral position first
        print("Resetting to neutral position...")
        self.reset_pose()
        rospy.sleep(1.0)
        
        # Move to initial position
        print("Moving to initial position...")
        self.send_joint_commands(initial_positions)
        rospy.sleep(2.0)
        
        # Define final standing position coordinates
        final_x = -0.08  # Move legs under body
        final_z = -0.12  # Lift body higher
        
        # Calculate final angles
        final_front_hip, final_front_knee = self.calculate_leg_ik(final_x, y, final_z, is_front=True)
        final_back_hip, final_back_knee = self.calculate_leg_ik(final_x, y, final_z, is_front=False)
        
        # Final position dictionary
        final_positions = {
            'rf_hip': final_front_hip, 'rf_knee': final_front_knee,
            'lf_hip': final_front_hip, 'lf_knee': final_front_knee,
            'rb_hip': final_back_hip, 'rb_knee': final_back_knee,
            'lb_hip': final_back_hip, 'lb_knee': final_back_knee
        }
        
        # Smoothly transition to standing position
        print("Standing up...")
        self.move_smoothly(initial_positions, final_positions, duration=2.0, steps=20)
        
        print("Standing position reached")
        
        # Maintain standing position until shutdown
        rate = rospy.Rate(10)
        try:
            while not rospy.is_shutdown():
                self.send_joint_commands(final_positions)
                rate.sleep()
        except rospy.ROSInterruptException:
            pass

def main():
    try:
        stander = PuppyStander()
        stander.stand()
    except Exception as e:
        rospy.logerr(f"Error: {e}")

if __name__ == '__main__':
    main()