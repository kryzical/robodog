#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import JointState
import numpy as np

class JointPositionChecker:
    def __init__(self):
        rospy.init_node('joint_position_checker', anonymous=True)
        
        # Target positions for standing (from gazebo.launch)
        self.target_positions = {
            'lf_joint1': 0.8,
            'rf_joint1': 0.8,
            'rb_joint1': 0.8,
            'lb_joint1': 0.8,
            'lf_joint2': 0.0,
            'rf_joint2': 0.0,
            'rb_joint2': 0.0,
            'lb_joint2': 0.0
        }
        
        # Tolerance for position matching (in radians)
        self.position_tolerance = 0.1
        
        # Subscribe to joint states
        rospy.Subscriber('/puppy/joint_states', JointState, self.joint_state_callback)
        
        rospy.loginfo("Joint position checker initialized. Monitoring standing position...")
    
    def joint_state_callback(self, msg):
        # Create a dictionary of current positions
        current_positions = dict(zip(msg.name, msg.position))
        
        # Check each joint
        all_joints_in_position = True
        for joint_name, target_pos in self.target_positions.items():
            if joint_name in current_positions:
                current_pos = current_positions[joint_name]
                diff = abs(current_pos - target_pos)
                
                status = "OK" if diff <= self.position_tolerance else "OFF"
                rospy.loginfo(f"{joint_name}: Target={target_pos:.3f}, Current={current_pos:.3f}, Status={status}")
                
                if diff > self.position_tolerance:
                    all_joints_in_position = False
        
        if all_joints_in_position:
            rospy.loginfo("\033[92mAll joints are in standing position!\033[0m")
        else:
            rospy.loginfo("\033[93mSome joints are not in position\033[0m")
        
        rospy.loginfo("----------------------------------------")

if __name__ == '__main__':
    try:
        checker = JointPositionChecker()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass 