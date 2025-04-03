#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import Joy
from std_msgs.msg import Float64
import math

class LegJoystickController:
    def __init__(self):
        rospy.init_node('leg_joystick_controller')
        
        # Parameters - can be adjusted
        self.leg_to_control = rospy.get_param('~leg', 'rf')  # Default to right front leg
        self.joystick_axis = rospy.get_param('~axis', 1)     # Default to vertical axis
        self.max_angle_change = rospy.get_param('~max_angle_change', 0.5)  # radians
        self.standing_hip_angle = 0.8  # Standing position from stand_up.py
        self.standing_knee_angle = 0.0  # Standing position from stand_up.py
        
        # Joint number mapping
        self.leg_joint_map = {
            'rf': {'hip': 1, 'knee': 5},  # Right Front leg
            'lf': {'hip': 2, 'knee': 6},  # Left Front leg
            'rb': {'hip': 3, 'knee': 7},  # Right Back leg
            'lb': {'hip': 4, 'knee': 8}   # Left Back leg
        }
        
        # Set up publishers for selected leg's joints
        if self.leg_to_control not in self.leg_joint_map:
            rospy.logerr(f"Leg '{self.leg_to_control}' not recognized. Options are: rf, lf, rb, lb")
            return
            
        hip_joint = self.leg_joint_map[self.leg_to_control]['hip']
        knee_joint = self.leg_joint_map[self.leg_to_control]['knee']
        
        self.hip_pub = rospy.Publisher(
            f'/puppy/joint{hip_joint}_position_controller/command', 
            Float64, 
            queue_size=1
        )
        self.knee_pub = rospy.Publisher(
            f'/puppy/joint{knee_joint}_position_controller/command', 
            Float64, 
            queue_size=1
        )
        
        # Subscribe to joystick
        self.joy_sub = rospy.Subscriber('/joy', Joy, self.joy_callback)
        
        rospy.loginfo(f"Leg joystick controller initialized for {self.leg_to_control} leg")
        rospy.loginfo(f"Use joystick axis {self.joystick_axis} to move the leg up and down")
        
        # Set initial position
        rospy.sleep(1)  # Wait for publishers to initialize
        self.hip_pub.publish(self.standing_hip_angle)
        self.knee_pub.publish(self.standing_knee_angle)
    
    def joy_callback(self, msg):
        # Check if joy message has enough axes
        if len(msg.axes) <= self.joystick_axis:
            rospy.logwarn(f"Joystick doesn't have axis {self.joystick_axis}")
            return
            
        # Read joystick value (-1 to 1) and calculate joint angles
        # Using negative because joystick typically reports -1 for up, 1 for down
        joy_value = -msg.axes[self.joystick_axis]
        
        # Calculate new knee angle (we'll adjust the knee to move the leg up/down)
        knee_angle = self.standing_knee_angle + (joy_value * self.max_angle_change)
        
        # Publish new joint positions
        self.hip_pub.publish(self.standing_hip_angle)  # Keep hip at standing angle
        self.knee_pub.publish(knee_angle)
        
        # Debug output
        rospy.loginfo_throttle(1.0, f"Joy value: {joy_value:.2f}, Knee angle: {knee_angle:.2f}")

if __name__ == '__main__':
    try:
        controller = LegJoystickController()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass