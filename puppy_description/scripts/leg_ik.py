#!/usr/bin/env python3

import math
import numpy as np

class LegIK:
    def __init__(self):
        # Leg dimensions (in meters)
        self.hip_length = 0.0525  # Distance from hip joint to knee joint
        self.knee_length = 0.053  # Distance from knee joint to foot
        
        # Joint limits (in radians) - adjusted for smoother movement
        self.hip_min = -1.5   # Reduced from -2.0 to prevent overextension
        self.hip_max = 1.5    # Reduced from 2.0 to prevent overextension
        self.knee_min = -1.5  # Reduced from -2.0 to prevent overextension
        self.knee_max = 1.5   # Reduced from 2.0 to prevent overextension
        
        # Logging
        self.debug = True
        self.last_angles = None  # Track last angles for smoothness
        
    def calculate_angles(self, target_x, target_y, target_z):
        """
        Calculate hip and knee angles for a given foot position
        Returns: (hip_angle, knee_angle) in radians
        """
        # Calculate distance to target
        distance = math.sqrt(target_x**2 + target_y**2 + target_z**2)
        
        # Check if target is reachable
        max_reach = self.hip_length + self.knee_length
        if distance > max_reach:
            if self.debug:
                print(f"Warning: Target {distance:.3f}m is beyond maximum reach of {max_reach:.3f}m")
            return None, None
            
        # Calculate angles using law of cosines
        # First, calculate knee angle
        cos_knee = (distance**2 - self.hip_length**2 - self.knee_length**2) / (2 * self.hip_length * self.knee_length)
        if cos_knee > 1:
            cos_knee = 1
        elif cos_knee < -1:
            cos_knee = -1
        knee_angle = math.acos(cos_knee)
        
        # Then calculate hip angle
        cos_hip = (self.hip_length**2 + distance**2 - self.knee_length**2) / (2 * self.hip_length * distance)
        if cos_hip > 1:
            cos_hip = 1
        elif cos_hip < -1:
            cos_hip = -1
        hip_angle = math.acos(cos_hip)
        
        # Add angle for target position
        hip_angle += math.atan2(target_y, target_x)
        
        # Check joint limits
        if hip_angle < self.hip_min:
            hip_angle = self.hip_min
        elif hip_angle > self.hip_max:
            hip_angle = self.hip_max
            
        if knee_angle < self.knee_min:
            knee_angle = self.knee_min
        elif knee_angle > self.knee_max:
            knee_angle = self.knee_max
            
        # Smooth transitions if we have previous angles
        if self.last_angles is not None:
            last_hip, last_knee = self.last_angles
            # Limit maximum angle change per step
            max_angle_change = 0.1  # radians
            
            hip_diff = hip_angle - last_hip
            knee_diff = knee_angle - last_knee
            
            # Normalize angle differences to [-pi, pi]
            hip_diff = math.atan2(math.sin(hip_diff), math.cos(hip_diff))
            knee_diff = math.atan2(math.sin(knee_diff), math.cos(knee_diff))
            
            # Limit changes
            hip_diff = max(min(hip_diff, max_angle_change), -max_angle_change)
            knee_diff = max(min(knee_diff, max_angle_change), -max_angle_change)
            
            hip_angle = last_hip + hip_diff
            knee_angle = last_knee + knee_diff
            
        self.last_angles = (hip_angle, knee_angle)
            
        if self.debug:
            print(f"Target: ({target_x:.3f}, {target_y:.3f}, {target_z:.3f})")
            print(f"Angles: hip={math.degrees(hip_angle):.1f}°, knee={math.degrees(knee_angle):.1f}°")
            if self.last_angles is not None:
                print(f"Angle Changes: hip={math.degrees(hip_diff):.1f}°, knee={math.degrees(knee_diff):.1f}°")
            
        return hip_angle, knee_angle
        
    def calculate_foot_position(self, hip_angle, knee_angle):
        """
        Calculate foot position given joint angles
        Returns: (x, y, z) in meters
        """
        # Calculate first link end position
        x1 = self.hip_length * math.cos(hip_angle)
        y1 = self.hip_length * math.sin(hip_angle)
        
        # Calculate second link end position
        x2 = x1 + self.knee_length * math.cos(hip_angle + knee_angle)
        y2 = y1 + self.knee_length * math.sin(hip_angle + knee_angle)
        
        if self.debug:
            print(f"Foot position: ({x2:.3f}, {y2:.3f}, 0.0)")
            
        return x2, y2, 0.0 