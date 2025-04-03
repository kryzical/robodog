#!/usr/bin/env python3
"""
PuppyPi Velocity Walker

This module implements a ROS node that converts velocity commands (linear and angular)
from the cmd_vel topic into joint movements that make the PuppyPi robot walk or rotate.
It implements a simple walking gait using diagonal leg pairs and a statically stable
rotation method.

Features:
- Translation between velocity commands and joint movements
- Diagonal gait walking pattern for efficient movement
- Status monitoring and connection management
- Rotation control for turning the robot
- Simple standing position for stability

Usage:
  rosrun puppy_description velocity_walker.py

Published Topics:
  /puppy/joint{1-8}_position_controller/command (std_msgs/Float64): 
    Joint position commands for each of the 8 joints of the robot

Subscribed Topics:
  /cmd_vel (geometry_msgs/Twist): 
    Velocity commands for the robot
  /joint_states (sensor_msgs/JointState): 
    Current joint positions for verification
  /gazebo/model_states (gazebo_msgs/ModelStates): 
    Robot position in the simulation

Parameters:
  None (all parameters are hardcoded in the class)

Author: PuppyPi Development Team
License: MIT
"""

import rospy
from std_msgs.msg import Float64
from geometry_msgs.msg import Twist
from sensor_msgs.msg import JointState
from gazebo_msgs.msg import ModelStates
import time
import numpy as np
import signal
import sys
import math

class VelocityWalker:
    def __init__(self):
        """Initialize the velocity-based walker node"""
        rospy.init_node('velocity_walker', anonymous=True)
        rospy.loginfo("Starting Velocity Walker - controls robot via cmd_vel...")
        
        # Set control rate - 20 Hz for smoother motion
        self.rate = rospy.Rate(20)
        
        # Initialize deadzone first
        self.deadzone = 0.01
        rospy.loginfo(f"Initialized deadzone: {self.deadzone}")
        
        # Create joint publishers
        self.joint_pubs = {}
        joint_mapping = {
            'rf_joint1': 1,  # Right front hip
            'lf_joint1': 2,  # Left front hip
            'rb_joint1': 3,  # Right back hip
            'lb_joint1': 4,  # Left back hip
            'rf_joint2': 5,  # Right front knee
            'lf_joint2': 6,  # Left front knee
            'rb_joint2': 7,  # Right back knee
            'lb_joint2': 8   # Left back knee
        }
        
        for joint_name, controller_num in joint_mapping.items():
            pub = rospy.Publisher(f'/puppy/joint{controller_num}_position_controller/command', Float64, queue_size=1)
            self.joint_pubs[joint_name] = pub
            
        # Subscribe to joint states for verification
        rospy.Subscriber('/joint_states', JointState, self.joint_states_callback)
        
        # Subscribe to model states for position tracking
        rospy.Subscriber('/gazebo/model_states', ModelStates, self.model_states_callback)
        
        # Subscribe to cmd_vel topic for velocity commands with a large queue size
        self.cmd_vel_sub = rospy.Subscriber('/cmd_vel', Twist, self.cmd_vel_callback, queue_size=10)
        
        # Load IK module if available
        try:
            from puppy_ik import PuppyIK
            self.ik = PuppyIK()
            rospy.loginfo("PuppyIK module loaded")
        except ImportError:
            rospy.logwarn("Could not import PuppyIK module. Using simple joint angle control.")
            self.ik = None
        
        # Walking parameters - optimized for smooth, level circular gait
        self.STAND_HEIGHT = 0.12  # Height from ground to body
        self.STAND_WIDTH = 0.05   # Width between legs
        self.STAND_LENGTH = 0.07  # Length offset for standing position
        self.STEP_HEIGHT = 0.02   # Moderate step height for smooth walking
        self.STEP_LENGTH = 0.04   # Moderate step length for smooth walking
        self.TRANSITION_STEPS = 6  # More transitions for smoother movement
        
        # Time intervals for walking cycle phases - balanced for smooth movement
        self.PHASE_1_TIME = 0.1  # Lift phase
        self.PHASE_2_TIME = 0.1  # Forward phase
        self.PHASE_3_TIME = 0.1  # Lower phase
        self.PHASE_4_TIME = 0.1  # Push phase
        
        # Flags and state variables
        self.walking = False
        self.rotating = False
        self.direction = 0  # -1 backward, 0 stopped, 1 forward
        self.rotation_direction = 0  # -1 right, 0 none, 1 left
        self.current_phase = 0  # Current phase of the walking cycle
        self.phase_start_time = rospy.Time.now()
        self.cycle_count = 0
        self.consecutive_errors = 0
        self.max_consecutive_errors = 3
        
        # Movement parameters - adjusted for better stability
        self.LIFT_HEIGHT = 0.08  # How high to lift the legs (meters)
        self.ROTATION_ANGLE = 0.12  # Increased rotation angle for better turning
        
        # Standing position offsets - optimized for better stability
        self.stand_offsets = {
            "shoulders": 0.0,
            "legs": 0.7,
            "feet": -1.4
        }
        
        # Create publishers for each joint
        self.publishers = {}
        for joint_name in self.joint_pubs:
            topic = f"/puppy/{joint_name}"
            self.publishers[joint_name] = rospy.Publisher(topic, Float64, queue_size=10)
        
        # Timer for walking cycle
        self.timer = rospy.Timer(rospy.Duration(0.01), self.walk_cycle)
        
        # Current joint positions
        self.current_positions = self.get_standing_position()
        
        # Initial position - stand up
        rospy.sleep(1.0)  # Wait for publishers to connect
        self.stand_up()
        rospy.loginfo("Robot is ready and in standing position")
        
        # Setup signal handler for clean shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        
        # Add status timer
        rospy.Timer(rospy.Duration(2.0), self.status_timer_callback)
    
    def status_timer_callback(self, event):
        """Output status information periodically"""
        if self.cycle_count > 0:
            rospy.loginfo("✓ Receiving velocity commands - cycle count: %d", self.cycle_count)
        else:
            rospy.logwarn("✗ No new velocity commands - last command %.2f seconds ago", 
                      (rospy.Time.now() - self.phase_start_time).to_sec())
        
        # Re-subscribe to cmd_vel to ensure connection is active
        self.cmd_vel_sub.unregister()
        self.cmd_vel_sub = rospy.Subscriber('/cmd_vel', Twist, self.cmd_vel_callback, queue_size=10)
        rospy.loginfo("Re-subscribed to /cmd_vel topic")
        
    def joint_states_callback(self, msg):
        """Process joint state updates from Gazebo"""
        # This function receives joint state messages but doesn't need to do anything with them
        # It's primarily for monitoring joint states if needed for debugging
        pass
        
    def model_states_callback(self, msg):
        """Process model state updates from Gazebo"""
        # Find our robot's index in the model_states array
        try:
            puppy_index = msg.name.index('puppy')
            # Store robot position and orientation if needed
            # Can be used for position tracking and velocity calculation
        except ValueError:
            # Robot model not found in the message
            pass
        
    def signal_handler(self, sig, frame):
        """Handle SIGINT for clean shutdown"""
        rospy.loginfo("Shutting down...")
        self.stand_up()
        sys.exit(0)
        
    def cmd_vel_callback(self, msg):
        """Handle incoming velocity commands"""
        try:
            # Extract linear and angular velocities
            linear_x = msg.linear.x
            angular_z = msg.angular.z
            
            # Debug logging
            rospy.loginfo(f"Velocity Walker: Received cmd_vel linear.x={linear_x:.2f}, angular.z={angular_z:.2f}")
            rospy.loginfo(f"Current deadzone value: {self.deadzone}")
            
            # Apply deadzone
            if abs(linear_x) < self.deadzone:
                linear_x = 0.0
            if abs(angular_z) < self.deadzone:
                angular_z = 0.0
                
            # Update target velocities
            self.target_linear_x = linear_x
            self.target_angular_z = angular_z
            
            # Reset command timeout
            self.last_cmd_time = rospy.Time.now()
            
            # Determine if we should be walking (forward or backward)
            if abs(linear_x) > 0.01:
                self.walking = True
                self.direction = 1 if linear_x > 0 else -1
                rospy.loginfo(f"WALKING {self.direction}: {'FORWARD' if self.direction > 0 else 'BACKWARD'}")
                # Log joint positions when walking starts
                rospy.loginfo(f"Current joint positions: {self.current_positions}")
            else:
                self.walking = False
                self.direction = 0
                
            # Determine if we should be rotating
            if abs(angular_z) > 0.01:
                self.rotating = True
                self.rotation_direction = 1 if angular_z > 0 else -1
                rospy.loginfo(f"ROTATING {self.rotation_direction}: {'LEFT' if self.rotation_direction > 0 else 'RIGHT'}")
            else:
                self.rotating = False
                self.rotation_direction = 0
                
            # If nothing is happening, make sure the robot is standing
            if not self.walking and not self.rotating:
                # Only reset to standing if we were previously moving
                if self.current_phase != 0 or self.cycle_count > 0:
                    rospy.loginfo("STANDING STILL - resetting to standing position")
                    self.stand_up()
                    self.current_phase = 0
                    self.cycle_count = 0
        except Exception as e:
            rospy.logerr(f"Error in cmd_vel_callback: {str(e)}")
            import traceback
            rospy.logerr(traceback.format_exc())
    
    def calculate_leg_positions(self, phase, leg):
        """Calculate leg positions based on phase and leg"""
        # Base standing position
        if leg == 'rf':  # Right front
            x = self.STAND_LENGTH
            y = -self.STAND_WIDTH
        elif leg == 'lf':  # Left front
            x = self.STAND_LENGTH
            y = self.STAND_WIDTH
        elif leg == 'rb':  # Right back
            x = -self.STAND_LENGTH
            y = -self.STAND_WIDTH
        elif leg == 'lb':  # Left back
            x = -self.STAND_LENGTH
            y = self.STAND_WIDTH
        else:
            rospy.logerr(f"Unknown leg: {leg}")
            return 0, 0, 0
        
        z = -self.STAND_HEIGHT  # Default height
        
        # Smooth circular walking pattern with coordinated leg motion
        if phase == 'lift':
            # Moderate lift with forward movement
            z = -(self.STAND_HEIGHT - self.STEP_HEIGHT * 0.7)  # Moderate lift
            # Add forward movement during lift
            x += self.STEP_LENGTH * self.direction * 0.2
        elif phase == 'forward':
            # Smooth forward movement
            z = -(self.STAND_HEIGHT - self.STEP_HEIGHT * 0.5)  # Keep leg lifted
            x += self.STEP_LENGTH * self.direction * 0.8  # Strong forward movement
        elif phase == 'lower':
            # Smooth lowering with forward motion
            x += self.STEP_LENGTH * self.direction * 0.8  # Keep forward position
            z = -self.STAND_HEIGHT  # Lower leg
        elif phase == 'push':
            # Moderate push phase
            x += self.STEP_LENGTH * 0.4 * self.direction  # Moderate push
            z = -self.STAND_HEIGHT  # Keep leg down
        
        # Add circular motion - legs move in a smooth arc
        if self.walking and phase != 'stand':
            # Add circular motion for more natural dog-like walking
            if phase == 'lift':
                # Move leg outward during lift
                y_offset = 0.015 * (1 if 'r' in leg else -1)
            elif phase == 'forward':
                # Move leg inward during forward motion
                y_offset = -0.015 * (1 if 'r' in leg else -1)
            elif phase == 'lower':
                # Keep leg inward during lower
                y_offset = -0.015 * (1 if 'r' in leg else -1)
            elif phase == 'push':
                # Move leg outward during push
                y_offset = 0.015 * (1 if 'r' in leg else -1)
            else:
                y_offset = 0.0
                
            y += y_offset
        
        return x, y, z
    
    def set_leg_position(self, leg_name, phase, transition_time=None):
        """Set a leg to a specific position with IK or direct angle control"""
        # Direct joint angle control for smooth, level walking
        if phase == 'stand':
            # Standing position - all legs straight down
            hip_angle = 0.8  # Approximately 45 degrees
            knee_angle = 0.0  # Straight legs
        elif phase == 'lift':
            # Lift phase - lift leg moderately
            if leg_name in ['rf', 'lf']:  # Front legs
                hip_angle = 1.0  # Moderate hip angle for lift
                knee_angle = -0.3  # Moderate knee bend for lift
            else:  # Back legs
                hip_angle = 0.6  # Lower hip angle
                knee_angle = -0.3  # Moderate knee bend for lift
        elif phase == 'forward':
            # Forward phase - move leg forward smoothly
            if leg_name in ['rf', 'lf']:  # Front legs
                hip_angle = 0.4  # Lower hip angle for forward motion
                knee_angle = -0.3  # Keep knee bent
            else:  # Back legs
                hip_angle = 1.2  # Higher hip angle for forward motion
                knee_angle = -0.3  # Keep knee bent
        elif phase == 'lower':
            # Lower phase - lower leg to ground
            if leg_name in ['rf', 'lf']:  # Front legs
                hip_angle = 0.4  # Keep hip angle for forward motion
                knee_angle = -0.2  # Start straightening knee
            else:  # Back legs
                hip_angle = 1.2  # Keep hip angle for forward motion
                knee_angle = -0.2  # Start straightening knee
        elif phase == 'push':
            # Push phase - push against ground moderately
            if leg_name in ['rf', 'lf']:  # Front legs
                hip_angle = 1.3  # Higher hip angle for push
                knee_angle = 0.3  # Moderate backward bend for push
            else:  # Back legs
                hip_angle = 0.3  # Lower hip angle for push
                knee_angle = 0.3  # Moderate backward bend for push
        
        # Apply direction-specific adjustments
        if self.direction > 0:  # Forward
            # No adjustments needed for forward motion
            pass
        elif self.direction < 0:  # Backward
            # Reverse the hip angles for backward motion
            if phase in ['forward', 'lower', 'push']:
                hip_angle = 1.6 - hip_angle  # Mirror the hip angle
        
        # Apply rotation-specific adjustments
        if self.rotating:
            if self.rotation_direction > 0:  # Left rotation
                if leg_name in ['lf', 'rb']:  # Left front and right back
                    hip_angle += 0.25  # Increased hip angle for rotation
                elif leg_name in ['rf', 'lb']:  # Right front and left back
                    hip_angle -= 0.25  # Decreased hip angle for rotation
            else:  # Right rotation
                if leg_name in ['lf', 'rb']:  # Left front and right back
                    hip_angle -= 0.25  # Decreased hip angle for rotation
                elif leg_name in ['rf', 'lb']:  # Right front and left back
                    hip_angle += 0.25  # Increased hip angle for rotation
        
        # Publish to joint controllers
        self.joint_pubs[f'{leg_name}_joint1'].publish(hip_angle)
        self.joint_pubs[f'{leg_name}_joint2'].publish(knee_angle)
        
        # Debug logging
        if self.cycle_count % 20 == 0:
            rospy.loginfo(f"Setting {leg_name} leg: hip={hip_angle:.2f}, knee={knee_angle:.2f}")
    
    def smooth_transition(self, leg_name, start_phase, end_phase, transition_time):
        """Make a smooth transition between two leg positions"""
        # This is a simplified smoothing - for a real implementation, we would interpolate
        # between the start and end positions over multiple small steps
        rospy.sleep(transition_time * 0.5)
        self.set_leg_position(leg_name, end_phase)
    
    def walk_cycle(self, event):
        """Execute one step of the walking cycle"""
        try:
            if not self.walking and not self.rotating:
                return
                
            current_time = rospy.Time.now()
            cycle_time = (current_time - self.phase_start_time).to_sec()
            
            # Smooth walking cycle with coordinated leg pairs
            if self.current_phase == 0:  # Lift first diagonal pair
                if cycle_time < self.PHASE_1_TIME:  # Lift phase
                    for leg in ['rf', 'lb']:
                        self.set_leg_position(leg, 'lift')
                    return
                else:
                    self.current_phase = 1
                    self.phase_start_time = current_time
                    return
                    
            elif self.current_phase == 1:  # Move lifted legs forward
                if cycle_time < self.PHASE_2_TIME:  # Forward phase
                    for leg in ['rf', 'lb']:
                        self.set_leg_position(leg, 'forward')
                    return
                else:
                    self.current_phase = 2
                    self.phase_start_time = current_time
                    return
                    
            elif self.current_phase == 2:  # Lower first diagonal pair
                if cycle_time < self.PHASE_3_TIME:  # Lower phase
                    for leg in ['rf', 'lb']:
                        self.set_leg_position(leg, 'lower')
                    return
                else:
                    self.current_phase = 3
                    self.phase_start_time = current_time
                    return
                    
            elif self.current_phase == 3:  # Lift second diagonal pair
                if cycle_time < self.PHASE_1_TIME:  # Lift phase
                    for leg in ['lf', 'rb']:
                        self.set_leg_position(leg, 'lift')
                    return
                else:
                    self.current_phase = 4
                    self.phase_start_time = current_time
                    return
                    
            elif self.current_phase == 4:  # Move second diagonal pair forward
                if cycle_time < self.PHASE_2_TIME:  # Forward phase
                    for leg in ['lf', 'rb']:
                        self.set_leg_position(leg, 'forward')
                    return
                else:
                    self.current_phase = 5
                    self.phase_start_time = current_time
                    return
                    
            elif self.current_phase == 5:  # Lower second diagonal pair
                if cycle_time < self.PHASE_3_TIME:  # Lower phase
                    for leg in ['lf', 'rb']:
                        self.set_leg_position(leg, 'lower')
                    return
                else:
                    self.current_phase = 0
                    self.phase_start_time = current_time
                    self.cycle_count += 1
                    
                    # Log cycle completion for debugging
                    if self.cycle_count % 10 == 0:
                        rospy.loginfo(f"Completed {self.cycle_count} walking cycles")
                    return
                    
        except Exception as e:
            rospy.logerr(f"Error in walk cycle: {str(e)}")
            import traceback
            rospy.logerr(traceback.format_exc())
            self.stand_up()
            self.current_phase = 0
            self.cycle_count = 0
    
    def publish_joint_positions(self, leg_name, pos):
        """Publish joint positions to the controllers"""
        try:
            x, y, z = pos
            
            # Smooth joint angle calculations for dog motion
            if leg_name in ['rf', 'lf', 'rb', 'lb']:
                # Hip angle - based on x and y position with improved calculation
                hip_angle = np.arctan2(y, x)
                
                # Knee angle - based on leg length and height with improved calculation
                leg_length = np.sqrt(x*x + y*y)
                knee_angle = -np.arctan2(z, leg_length)
                
                # Apply direction-specific adjustments for smooth motion
                if self.direction > 0:  # Forward
                    hip_angle *= 0.9  # Moderate hip angle for forward motion
                    knee_angle *= 0.9  # Moderate knee angle for motion
                elif self.direction < 0:  # Backward
                    hip_angle *= 0.9  # Moderate hip angle for backward motion
                    knee_angle *= 0.9  # Moderate knee angle for motion
                
                # Add subtle oscillation for more natural motion
                if self.walking:
                    oscillation = 0.05 * np.sin(self.cycle_count * 0.5)  # Subtle oscillation
                    hip_angle += oscillation
                
                # Publish to joint controllers
                self.joint_pubs[f'{leg_name}_joint1'].publish(hip_angle)
                self.joint_pubs[f'{leg_name}_joint2'].publish(knee_angle)
                
                # Debug logging
                if self.cycle_count % 20 == 0:
                    rospy.loginfo(f"Setting {leg_name} leg: hip={hip_angle:.2f}, knee={knee_angle:.2f}")
        except Exception as e:
            rospy.logerr(f"Error publishing joint positions for {leg_name}: {str(e)}")
            import traceback
            rospy.logerr(traceback.format_exc())
    
    def get_standing_position(self):
        """Get the standing position for the robot"""
        return {
            "front_left_shoulder": self.stand_offsets["shoulders"],
            "front_left_leg": self.stand_offsets["legs"],
            "front_left_foot": self.stand_offsets["feet"],
            "front_right_shoulder": self.stand_offsets["shoulders"],
            "front_right_leg": self.stand_offsets["legs"],
            "front_right_foot": self.stand_offsets["feet"],
            "rear_left_shoulder": self.stand_offsets["shoulders"],
            "rear_left_leg": self.stand_offsets["legs"],
            "rear_left_foot": self.stand_offsets["feet"],
            "rear_right_shoulder": self.stand_offsets["shoulders"],
            "rear_right_leg": self.stand_offsets["legs"],
            "rear_right_foot": self.stand_offsets["feet"]
        }
    
    def stand_up(self):
        """Set the robot to a standing position"""
        rospy.loginfo("Setting standing position...")
        
        for leg in ['rf', 'lf', 'rb', 'lb']:
            self.set_leg_position(leg, 'stand')
        
        rospy.sleep(0.5)  # Give time for the robot to reach standing position
        rospy.loginfo("Standing position achieved")
    
    def run(self):
        """Main control loop"""
        self.stand_up()
        rospy.loginfo("Velocity Walker is running - listening for cmd_vel messages...")
        
        # Wait for the first cmd_vel message
        rospy.loginfo("Waiting for joystick commands - press buttons or move joystick")
        
        while not rospy.is_shutdown():
            # Check for timeout
            time_since_last_cmd = (rospy.Time.now() - self.phase_start_time).to_sec()
            
            # If we're walking and velocity commands are still valid
            if self.walking and time_since_last_cmd < self.PHASE_1_TIME:
                # Execute a walking cycle
                self.walk_cycle(None)
            else:
                # Wait for the next command
                self.rate.sleep()


if __name__ == '__main__':
    try:
        walker = VelocityWalker()
        walker.run()
    except rospy.ROSInterruptException:
        pass 