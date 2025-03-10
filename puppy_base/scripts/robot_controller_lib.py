#!/usr/bin/env python3
# coding=utf8
"""
Common controller library for the puppy robot.
This provides shared functionality for walking, standing, and other robot movements.
"""

import rospy
import math
import numpy as np
from std_msgs.msg import Float64

class PuppyJointController:
    """Base class for controlling the puppy robot joints"""
    
    def __init__(self, node_name='puppy_controller'):
        """Initialize a new controller"""
        if not rospy.core.is_initialized():
            rospy.init_node(node_name, log_level=rospy.INFO)
        
        # Standard joint publisher mapping
        self.joint_pubs = {
            'rf_hip': rospy.Publisher('/puppy/joint1_position_controller/command', Float64, queue_size=1),
            'rf_knee': rospy.Publisher('/puppy/joint5_position_controller/command', Float64, queue_size=1),
            'lf_hip': rospy.Publisher('/puppy/joint2_position_controller/command', Float64, queue_size=1),
            'lf_knee': rospy.Publisher('/puppy/joint6_position_controller/command', Float64, queue_size=1),
            'rb_hip': rospy.Publisher('/puppy/joint3_position_controller/command', Float64, queue_size=1),
            'rb_knee': rospy.Publisher('/puppy/joint7_position_controller/command', Float64, queue_size=1),
            'lb_hip': rospy.Publisher('/puppy/joint4_position_controller/command', Float64, queue_size=1),
            'lb_knee': rospy.Publisher('/puppy/joint8_position_controller/command', Float64, queue_size=1)
        }
        
        # Give publishers time to connect
        rospy.sleep(0.5)
    
    def send_joint_commands(self, positions):
        """Send commands to all specified joints"""
        for joint, pos in positions.items():
            if joint in self.joint_pubs:
                self.joint_pubs[joint].publish(Float64(pos))
    
    def reset_pose(self):
        """Reset all joints to zero position"""
        zero_pos = {joint: 0.0 for joint in self.joint_pubs.keys()}
        self.send_joint_commands(zero_pos)
    
    def calculate_leg_ik(self, x, y, z, leg_length=0.15, is_front=True):
        """
        Calculate inverse kinematics for a 2-DOF leg
        
        Args:
            x (float): X coordinate (forward/backward)
            y (float): Y coordinate (left/right)
            z (float): Z coordinate (up/down)
            leg_length (float): Length of each leg segment in meters
            is_front (bool): Whether this is a front leg
            
        Returns:
            tuple: (hip_angle, knee_angle) in radians
        """
        # Adjust x offset for front/back legs for better balance
        x_offset = 0.02 if is_front else -0.02
        x = x + x_offset
        
        try:
            # Calculate distance from hip to foot
            r = math.sqrt(x*x + z*z)
            if r > 2 * leg_length:
                r = 2 * leg_length
            
            # Calculate knee angle using law of cosines
            knee_angle = math.acos((2 * leg_length * leg_length - r * r) / 
                                   (2 * leg_length * leg_length))
            
            # Calculate hip angle
            hip_angle = -math.atan2(x, -z) - math.atan2(
                leg_length * math.sin(knee_angle),
                leg_length + leg_length * math.cos(knee_angle)
            )
            
            # Apply different offsets for front and back legs
            if is_front:
                hip_angle += 0.1  # Small forward tilt for front legs
            else:
                hip_angle -= 0.1  # Small backward tilt for back legs
                
            return hip_angle, knee_angle
        except:
            # If calculation fails, return safe default
            return 0, 0

    def move_smoothly(self, start_positions, end_positions, duration=1.0, steps=20):
        """
        Move smoothly from start to end positions
        
        Args:
            start_positions (dict): Starting joint positions
            end_positions (dict): Ending joint positions
            duration (float): Duration of movement in seconds
            steps (int): Number of interpolation steps
        """
        rate = rospy.Rate(steps / duration)
        
        for i in range(steps):
            # Calculate interpolation ratio
            ratio = (i + 1) / steps
            
            # Interpolate between positions
            current_positions = {}
            for joint in end_positions.keys():
                if joint in start_positions:
                    start = start_positions[joint]
                    end = end_positions[joint]
                    current_positions[joint] = start + (end - start) * ratio
                else:
                    current_positions[joint] = end_positions[joint]
            
            # Send the interpolated position
            self.send_joint_commands(current_positions)
            rate.sleep()