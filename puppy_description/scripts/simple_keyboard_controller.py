#!/usr/bin/env python3
import rospy
from std_msgs.msg import Float64, String
import sys
import signal

class KeyboardLegController:
    def __init__(self):
        rospy.init_node('keyboard_leg_controller')
        
        # Parameters
        self.max_angle_change = rospy.get_param('~max_angle_change', 0.7)  # radians
        self.standing_hip_angle = 0.8  # Standing position from gazebo.launch
        self.standing_knee_angle = 0.0  # Standing position from gazebo.launch
        self.step_size = 0.05  # Amount to change per keystroke
        
        # Set up publishers for right front leg joints
        self.hip_pub = rospy.Publisher(
            '/puppy/joint1_position_controller/command',  # RF hip joint
            Float64, 
            queue_size=1
        )
        self.knee_pub = rospy.Publisher(
            '/puppy/joint5_position_controller/command',  # RF knee joint
            Float64, 
            queue_size=1
        )
        
        # Subscribe to keyboard commands
        rospy.Subscriber('/keyboard_commands', String, self.keyboard_callback)
        
        # Initialize variables for current joint positions
        self.current_knee_angle = self.standing_knee_angle
        
        # Set initial position
        rospy.sleep(1)  # Wait for publishers to initialize
        self.publish_positions()
        
        rospy.loginfo("==============================================")
        rospy.loginfo("KEYBOARD LEG CONTROLLER STARTED")
        rospy.loginfo("==============================================")
        rospy.loginfo("USE SEPARATE TERMINAL TO SEND COMMANDS:")
        rospy.loginfo("rostopic pub /keyboard_commands std_msgs/String \"w\" --once")
        rospy.loginfo("rostopic pub /keyboard_commands std_msgs/String \"s\" --once")
        rospy.loginfo("rostopic pub /keyboard_commands std_msgs/String \"r\" --once")
        rospy.loginfo("==============================================")
        
    def keyboard_callback(self, msg):
        key = msg.data.strip().lower()
        
        rospy.loginfo(f"Received command: {key}")
        
        if key == 'w':  # Move leg up
            self.current_knee_angle = min(self.current_knee_angle + self.step_size, 
                                         self.standing_knee_angle + self.max_angle_change)
            self.publish_positions()
            rospy.loginfo(f"Leg UP   | Knee angle: {self.current_knee_angle:.2f}")
        
        elif key == 's':  # Move leg down
            self.current_knee_angle = max(self.current_knee_angle - self.step_size, 
                                         self.standing_knee_angle - self.max_angle_change)
            self.publish_positions()
            rospy.loginfo(f"Leg DOWN | Knee angle: {self.current_knee_angle:.2f}")
        
        elif key == 'r':  # Reset position
            self.current_knee_angle = self.standing_knee_angle
            self.publish_positions()
            rospy.loginfo(f"RESET    | Knee angle: {self.current_knee_angle:.2f}")
    
    def publish_positions(self):
        # Keep hip at standing angle, only adjust knee
        self.hip_pub.publish(Float64(self.standing_hip_angle))
        self.knee_pub.publish(Float64(self.current_knee_angle))

if __name__ == '__main__':
    try:
        controller = KeyboardLegController()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass