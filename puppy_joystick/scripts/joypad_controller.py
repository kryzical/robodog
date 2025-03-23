#!/usr/bin/env python3
"""
PuppyPi Joypad Controller

This module implements a ROS node for controlling the PuppyPi robot using
joystick/gamepad input. It translates joystick messages from the joy topic
into velocity commands that are published to the cmd_vel topic.

Features:
- Support for both button-based and analog stick control
- Configurable button and axis mappings through ROS parameters
- Automatic connection maintenance with heartbeat messages
- Detailed status reporting

Usage:
  rosrun puppy_joystick joypad_controller.py

ROS Parameters:
  ~forward_button (int, default: 4): Button index for forward movement
  ~backward_button (int, default: 6): Button index for backward movement
  ~left_button (int, default: 7): Button index for left rotation
  ~right_button (int, default: 5): Button index for right rotation
  ~stop_button (int, default: 2): Button index for stopping all movement
  ~linear_axis (int, default: 1): Axis index for forward/backward control
  ~angular_axis (int, default: 0): Axis index for left/right rotation
  ~linear_scale (float, default: 0.2): Max linear velocity in m/s
  ~angular_scale (float, default: 0.8): Max angular velocity in rad/s
  ~dead_zone (float, default: 0.05): Deadzone threshold for analog sticks
  ~analog_mode (bool, default: true): Whether to use analog sticks

Published Topics:
  cmd_vel (geometry_msgs/Twist): Velocity commands for the robot

Subscribed Topics:
  joy (sensor_msgs/Joy): Joystick input messages

Author: PuppyPi Development Team
License: MIT
"""

import rospy
import subprocess
from sensor_msgs.msg import Joy
from std_msgs.msg import Float64
from geometry_msgs.msg import Twist
import os

class JoypadController:
    def __init__(self):
        """Initialize the joypad controller node."""
        # Initialize the node
        rospy.init_node('joypad_controller', anonymous=True)
        
        # Status variables
        self.last_command_sent = rospy.Time.now()
        self.command_count = 0
        self.last_joy_received = rospy.Time.now()
        self.joy_count = 0
        
        # Get parameters for button mappings or use defaults
        self.forward_button = rospy.get_param('~forward_button', 4)    # Triangle/Y button - Up 
        self.backward_button = rospy.get_param('~backward_button', 6)  # Cross/A button - Down
        self.left_button = rospy.get_param('~left_button', 7)          # Square/X button - Left
        self.right_button = rospy.get_param('~right_button', 5)        # Circle/B button - Right
        self.stop_button = rospy.get_param('~stop_button', 2)          # Share/Back button
        self.analog_mode = rospy.get_param('~analog_mode', True)       # Whether to use analog stick
        
        # Get parameters for stick axes
        self.linear_axis = rospy.get_param('~linear_axis', 1)          # Left stick up/down
        self.angular_axis = rospy.get_param('~angular_axis', 0)        # Left stick left/right
        
        # Velocity scaling parameters
        self.linear_scale = rospy.get_param('~linear_scale', 0.2)      # m/s per full stick
        self.angular_scale = rospy.get_param('~angular_scale', 0.8)    # rad/s per full stick
        
        # Dead zone for analog sticks
        self.dead_zone = rospy.get_param('~dead_zone', 0.05)
        
        # Set default velocity values
        self.default_linear_vel = 0.15  # Forward/backward speed in m/s
        self.default_angular_vel = 0.5  # Rotation speed in rad/s
        
        # Movement scripts locations
        script_directory = rospy.get_param('~script_directory', 
            '/ros_ws/src/puppy_description/scripts/movements')
        
        # Check if directory exists
        if not os.path.exists(script_directory):
            rospy.logwarn(f"Script directory {script_directory} not found! Some functionality will be disabled.")
            
        # Map buttons to movement scripts
        self.movement_scripts = {
            self.forward_button: os.path.join(script_directory, "forward.py"),
            self.backward_button: os.path.join(script_directory, "backward.py"),
            self.left_button: os.path.join(script_directory, "left.py"),
            self.right_button: os.path.join(script_directory, "right.py")
        }
        
        # Create velocity publisher for continuous control
        self.vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
        
        # Set up Joy subscriber
        self.joy_sub = rospy.Subscriber('joy', Joy, self.joy_callback, queue_size=10)
        
        # Add status timer
        rospy.Timer(rospy.Duration(1.0), self.status_timer_callback)
        
        rospy.loginfo("Joypad controller initialized with the following mappings:")
        rospy.loginfo(f"  Forward: Button {self.forward_button}")
        rospy.loginfo(f"  Backward: Button {self.backward_button}")
        rospy.loginfo(f"  Left: Button {self.left_button}")
        rospy.loginfo(f"  Right: Button {self.right_button}")
        rospy.loginfo(f"  Stop: Button {self.stop_button}")
        rospy.loginfo(f"  Analog Control: {'Enabled' if self.analog_mode else 'Disabled'}")
        
        # Send a no-op command to initialize communication
        self.send_zero_velocity()
        
    def status_timer_callback(self, event):
        """Output status information periodically"""
        now = rospy.Time.now()
        joy_age = (now - self.last_joy_received).to_sec()
        cmd_age = (now - self.last_command_sent).to_sec()
        
        rospy.loginfo(f"Status: Joy msgs: {self.joy_count}, Cmd msgs: {self.command_count}")
        rospy.loginfo(f"Last joy: {joy_age:.1f}s ago, Last cmd: {cmd_age:.1f}s ago")
        
        # Force a zero velocity command every second to keep connection active
        self.send_zero_velocity()
        
        # Re-subscribe to joy to ensure connection is active
        self.joy_sub.unregister()
        self.joy_sub = rospy.Subscriber('joy', Joy, self.joy_callback, queue_size=10)
        rospy.loginfo("Re-subscribed to Joy topic")
        
    def send_zero_velocity(self):
        """Send a zero velocity command to keep the connection active"""
        zero_vel = Twist()
        zero_vel.linear.x = 0.0
        zero_vel.angular.z = 0.0
        self.vel_pub.publish(zero_vel)
        self.command_count += 1
        self.last_command_sent = rospy.Time.now()
        
    def joy_callback(self, joy_msg):
        """Process incoming joy messages."""
        self.joy_count += 1
        self.last_joy_received = rospy.Time.now()
        
        try:
            # Create Twist message for velocity control
            vel_msg = Twist()
            
            # Check for stop button press
            if len(joy_msg.buttons) > self.stop_button and joy_msg.buttons[self.stop_button]:
                rospy.loginfo("Stop button pressed, halting robot")
                vel_msg.linear.x = 0.0
                vel_msg.angular.z = 0.0
                self.vel_pub.publish(vel_msg)
                self.command_count += 1
                self.last_command_sent = rospy.Time.now()
                return
            
            # Use analog stick values if enabled and sticks are available
            if self.analog_mode and len(joy_msg.axes) > max(self.linear_axis, self.angular_axis):
                # Apply deadzone filtering
                linear_val = joy_msg.axes[self.linear_axis]
                angular_val = joy_msg.axes[self.angular_axis]
                
                if abs(linear_val) < self.dead_zone:
                    linear_val = 0.0
                if abs(angular_val) < self.dead_zone:
                    angular_val = 0.0
                
                # Invert as needed (depending on joystick orientation)
                # For PS4/Xbox, pushing up gives negative value, but we want positive linear velocity
                linear_val = -linear_val
                
                # Scale values
                vel_msg.linear.x = linear_val * self.linear_scale
                vel_msg.angular.z = angular_val * self.angular_scale
                
                # Log the command if it's non-zero
                if abs(vel_msg.linear.x) > 0.01 or abs(vel_msg.angular.z) > 0.01:
                    rospy.loginfo(f"Analog joystick: linear={vel_msg.linear.x:.2f}, angular={vel_msg.angular.z:.2f}")
                
                # Always publish to maintain communication, even if zero
                self.vel_pub.publish(vel_msg)
                self.command_count += 1
                self.last_command_sent = rospy.Time.now()
            
            # Check for button presses
            if len(joy_msg.buttons) > max(self.forward_button, self.backward_button, 
                                          self.left_button, self.right_button):
                # Process directional buttons and send velocity commands
                # Forward button
                if joy_msg.buttons[self.forward_button]:
                    rospy.loginfo("Forward button pressed")
                    vel_msg.linear.x = self.default_linear_vel
                    vel_msg.angular.z = 0.0
                    self.vel_pub.publish(vel_msg)
                    self.command_count += 1
                    self.last_command_sent = rospy.Time.now()
                
                # Backward button
                elif joy_msg.buttons[self.backward_button]:
                    rospy.loginfo("Backward button pressed")
                    vel_msg.linear.x = -self.default_linear_vel
                    vel_msg.angular.z = 0.0
                    self.vel_pub.publish(vel_msg)
                    self.command_count += 1
                    self.last_command_sent = rospy.Time.now()
                
                # Left button
                elif joy_msg.buttons[self.left_button]:
                    rospy.loginfo("Left button pressed")
                    vel_msg.linear.x = 0.0
                    vel_msg.angular.z = self.default_angular_vel
                    self.vel_pub.publish(vel_msg)
                    self.command_count += 1
                    self.last_command_sent = rospy.Time.now()
                
                # Right button
                elif joy_msg.buttons[self.right_button]:
                    rospy.loginfo("Right button pressed")
                    vel_msg.linear.x = 0.0
                    vel_msg.angular.z = -self.default_angular_vel
                    self.vel_pub.publish(vel_msg)
                    self.command_count += 1
                    self.last_command_sent = rospy.Time.now()
                    
        except Exception as e:
            rospy.logerr(f"Error processing joystick input: {e}")
    
    def run(self):
        """Run the controller at a fixed rate."""
        rate = rospy.Rate(10)  # 10 Hz
        
        rospy.loginfo("Joypad controller is running. Use buttons or analog stick to control the robot.")
        
        while not rospy.is_shutdown():
            # Main control loop
            rate.sleep()

if __name__ == '__main__':
    try:
        controller = JoypadController()
        controller.run()
    except rospy.ROSInterruptException:
        pass 