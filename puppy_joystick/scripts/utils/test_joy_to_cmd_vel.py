#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist

class JoyToCmdVelTest:
    """Test node to directly map joystick inputs to cmd_vel commands"""
    
    def __init__(self):
        rospy.init_node('joy_to_cmd_vel_test', anonymous=True)
        
        # Initialize variables 
        self.speed = 1.0
        self.joy_received = False
        self.joy_count = 0
        self.cmd_count = 0
        
        # Define velocity publisher
        self.vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        rospy.loginfo("Publishing to /cmd_vel topic")
        
        # Subscribe to joystick input
        rospy.Subscriber('/joy', Joy, self.joy_callback)
        rospy.loginfo("Subscribed to /joy topic")
        
        # Setup a timer to check status periodically
        rospy.Timer(rospy.Duration(2), self.status_callback)
        
        rospy.loginfo("JoyToCmdVel test node initialized - Press buttons on joystick or virtual joystick")
        rospy.loginfo("Known joystick message format: axes[0]=forward/back, axes[4]=rotation")
    
    def status_callback(self, event):
        """Periodic status check"""
        if self.joy_received:
            rospy.loginfo("Joy to Cmd_Vel Test Status: Received %d joy messages, sent %d cmd_vel messages", 
                        self.joy_count, self.cmd_count)
        else:
            rospy.logwarn("No joystick messages received yet!")
    
    def joy_callback(self, data):
        """Process joystick inputs and publish cmd_vel commands"""
        # Log first message
        if not self.joy_received:
            self.joy_received = True
            rospy.loginfo("First joystick message received!")
            rospy.loginfo("Joy message has %d axes and %d buttons", len(data.axes), len(data.buttons))
        
        self.joy_count += 1
        
        # Create velocity command
        twist = Twist()
        
        # Simplified direct axis mapping - check if we have enough axes
        if len(data.axes) >= 5:
            # Forward/backward: First axis (index 0)
            if abs(data.axes[0]) > 0.1:
                twist.linear.x = data.axes[0] * self.speed
                rospy.loginfo("Joy axis 0: %.2f -> linear.x = %.2f", data.axes[0], twist.linear.x)
            
            # Rotation: Fifth axis (index 4)
            if abs(data.axes[4]) > 0.1:
                twist.angular.z = data.axes[4] * self.speed
                rospy.loginfo("Joy axis 4: %.2f -> angular.z = %.2f", data.axes[4], twist.angular.z)
        else:
            rospy.logwarn("Joy message has too few axes! Expected at least 5, got %d", len(data.axes))
        
        # Also check for buttons (if available)
        if len(data.buttons) >= 4:
            # Simple button mapping: buttons 0-3 for basic directions
            if data.buttons[0] == 1:  # X/A button - backward
                twist.linear.x = -self.speed
                rospy.loginfo("Button 0 pressed -> backward")
            elif data.buttons[1] == 1:  # Circle/B button - right
                twist.angular.z = -self.speed
                rospy.loginfo("Button 1 pressed -> turn right")
            elif data.buttons[2] == 1:  # Square/X button - left
                twist.angular.z = self.speed
                rospy.loginfo("Button 2 pressed -> turn left")
            elif data.buttons[3] == 1:  # Triangle/Y button - forward
                twist.linear.x = self.speed
                rospy.loginfo("Button 3 pressed -> forward")
        
        # Publish velocity command if there's movement
        if abs(twist.linear.x) > 0.01 or abs(twist.angular.z) > 0.01:
            self.vel_pub.publish(twist)
            self.cmd_count += 1
            rospy.loginfo("Published cmd_vel: linear.x=%.2f, angular.z=%.2f", 
                        twist.linear.x, twist.angular.z)
        elif self.joy_count % 10 == 0:
            # Periodically publish zero velocity to keep connection active
            self.vel_pub.publish(twist)
            rospy.loginfo("Published zero velocity command to maintain connection")


if __name__ == '__main__':
    try:
        test_node = JoyToCmdVelTest()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass 