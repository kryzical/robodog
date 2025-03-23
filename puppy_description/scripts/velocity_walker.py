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

class VelocityWalker:
    def __init__(self):
        """Initialize the velocity-based walker node"""
        rospy.init_node('velocity_walker', anonymous=True)
        rospy.loginfo("Starting Velocity Walker - controls robot via cmd_vel...")
        
        # Set control rate - 10 Hz for smooth motion
        self.rate = rospy.Rate(10)
        
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
        
        # Walking parameters
        self.STAND_HEIGHT = 0.12  # Height from ground to body
        self.STAND_WIDTH = 0.05   # Width between legs
        self.STAND_LENGTH = 0.07  # Length offset for standing position
        self.STEP_HEIGHT = 0.03   # Reduced height for leg lifting to make motion smoother
        self.STEP_LENGTH = 0.05   # Length of forward step
        self.TRANSITION_STEPS = 10  # Number of steps for smooth transitions
        
        # Timing parameters - adjusted for smoother motion
        self.PHASE_1_TIME = 0.12  # Time for lifting leg
        self.PHASE_2_TIME = 0.10  # Time for moving leg forward
        self.PHASE_3_TIME = 0.12  # Time for lowering leg
        self.PHASE_4_TIME = 0.10  # Time for pushing back
        
        # Velocity parameters
        self.linear_vel_x = 0.0
        self.angular_vel_z = 0.0
        self.walking = False
        self.last_cmd_time = rospy.Time.now()
        self.cmd_timeout = rospy.Duration(1.0)  # Stop if no commands received for 1 second
        self.last_cmd_count = 0
        self.cmd_count = 0
        
        # State tracking
        self.joint_positions = {}
        self.initial_position = None
        self.current_position = None
        
        # Setup signal handler for clean shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        
        # Add status timer
        rospy.Timer(rospy.Duration(2.0), self.status_timer_callback)
        
        # Start in standing position
        self.stand()
    
    def status_timer_callback(self, event):
        """Output status information periodically"""
        if self.cmd_count > self.last_cmd_count:
            rospy.loginfo("✓ Receiving velocity commands - count: %d", self.cmd_count)
            self.last_cmd_count = self.cmd_count
        else:
            rospy.logwarn("✗ No new velocity commands - last command %.2f seconds ago", 
                      (rospy.Time.now() - self.last_cmd_time).to_sec())
        
        # Re-subscribe to cmd_vel to ensure connection is active
        self.cmd_vel_sub.unregister()
        self.cmd_vel_sub = rospy.Subscriber('/cmd_vel', Twist, self.cmd_vel_callback, queue_size=10)
        rospy.loginfo("Re-subscribed to /cmd_vel topic")
        
    def signal_handler(self, sig, frame):
        """Handle SIGINT for clean shutdown"""
        rospy.loginfo("Shutting down...")
        self.stand()
        sys.exit(0)
        
    def cmd_vel_callback(self, msg):
        """Process incoming velocity commands"""
        self.linear_vel_x = msg.linear.x
        self.angular_vel_z = msg.angular.z
        self.last_cmd_time = rospy.Time.now()
        self.cmd_count += 1
        
        # Log command reception
        rospy.loginfo("Received velocity command: linear.x=%.2f, angular.z=%.2f", 
                   self.linear_vel_x, self.angular_vel_z)
        
        # Start walking if not already walking and linear velocity is non-zero
        if (abs(self.linear_vel_x) > 0.01 or abs(self.angular_vel_z) > 0.01) and not self.walking:
            self.walking = True
            rospy.loginfo(f"Starting to walk with linear velocity: {self.linear_vel_x:.2f} m/s, " 
                       f"angular velocity: {self.angular_vel_z:.2f} rad/s")
        
        # Stop walking if both velocities are zero
        if abs(self.linear_vel_x) < 0.01 and abs(self.angular_vel_z) < 0.01 and self.walking:
            self.walking = False
            rospy.loginfo("Stopping walk and returning to standing position")
            self.stand()
    
    def calculate_leg_positions(self, phase, leg):
        """Calculate leg positions based on phase and leg"""
        # Default standing position
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
        
        # Apply phase-specific modifications - REVERSED FOR FORWARD MOTION
        if phase == 'stand':
            # No modifications, use default standing position
            pass
        elif phase == 'lift':
            z = -(self.STAND_HEIGHT - self.STEP_HEIGHT)  # Lift leg up
        elif phase == 'forward':
            z = -(self.STAND_HEIGHT - self.STEP_HEIGHT)  # Keep leg up
            # Move leg forward by STEP_LENGTH (reversed direction for forward motion)
            if leg in ['rf', 'lf']:
                x = self.STAND_LENGTH - self.STEP_LENGTH  # Reversed
            else:
                x = -self.STAND_LENGTH - self.STEP_LENGTH  # Reversed
        elif phase == 'lower':
            # Position leg forward before lowering (reversed for forward motion)
            if leg in ['rf', 'lf']:
                x = self.STAND_LENGTH - self.STEP_LENGTH  # Reversed
            else:
                x = -self.STAND_LENGTH - self.STEP_LENGTH  # Reversed
        elif phase == 'push':
            # Push leg back to provide forward force (reversed for forward motion)
            if leg in ['rf', 'lf']:
                x = self.STAND_LENGTH + self.STEP_LENGTH  # Reversed
            else:
                x = -self.STAND_LENGTH + self.STEP_LENGTH  # Reversed
        
        return x, y, z
    
    def set_leg_position(self, leg_name, phase, transition_time=None):
        """Set a leg to a specific position with IK or direct angle control"""
        # Calculate desired position
        x, y, z = self.calculate_leg_positions(phase, leg_name)
        
        if self.ik:
            # Use inverse kinematics if available
            hip_angle, knee_angle = self.ik.calculate_angles(x, y, z)
            if hip_angle is not None and knee_angle is not None:
                self.joint_pubs[f'{leg_name}_joint1'].publish(hip_angle)
                self.joint_pubs[f'{leg_name}_joint2'].publish(knee_angle)
        else:
            # Simple case without IK - approximations for smooth motion
            if phase == 'stand':
                hip_angle = 0.8  # Approximately 45 degrees
                knee_angle = 0.0
            elif phase == 'lift':
                hip_angle = 0.9  # Increase hip angle to lift
                knee_angle = -0.2  # Bend knee slightly
            elif phase == 'forward':
                # REVERSED for forward motion
                hip_angle = 0.7  # Lower hip angle (reversed)
                knee_angle = -0.2  # Keep knee bent
            elif phase == 'lower':
                hip_angle = 0.7  # Keep hip angle (reversed)
                knee_angle = -0.1  # Start straightening knee
            elif phase == 'push':
                # REVERSED for forward motion
                hip_angle = 1.0  # Higher hip angle to push (reversed)
                knee_angle = 0.1  # Slight backward bend for push
            
            # Apply the angles
            self.joint_pubs[f'{leg_name}_joint1'].publish(hip_angle)
            self.joint_pubs[f'{leg_name}_joint2'].publish(knee_angle)
            
    def smooth_transition(self, leg_name, start_phase, end_phase, transition_time):
        """Make a smooth transition between two leg positions"""
        # This is a simplified smoothing - for a real implementation, we would interpolate
        # between the start and end positions over multiple small steps
        rospy.sleep(transition_time * 0.5)
        self.set_leg_position(leg_name, end_phase)
    
    def walk_cycle(self):
        """Execute one walking cycle based on current velocity"""
        try:
            # Scale step size based on linear velocity
            step_scale = min(1.0, abs(self.linear_vel_x) / 0.2)  # Cap at max speed of 0.2 m/s
            self.STEP_LENGTH = 0.05 * step_scale  # Scale step length with velocity
            
            # Begin with a more stable position
            for leg in ['rf', 'lf', 'rb', 'lb']:
                self.set_leg_position(leg, 'stand')
            rospy.sleep(0.05)  # Short pause for stability
            
            # Phase 1: First diagonal pair (LF+RB) lift and prepare
            self.set_leg_position('lf', 'lift')
            self.set_leg_position('rb', 'lift')
            # Adjust other legs for better balance - more subtle movement
            self.set_leg_position('rf', 'push')
            self.set_leg_position('lb', 'push')
            rospy.sleep(self.PHASE_1_TIME * 0.5)  # Shorter wait for smoother motion
            
            # Phase 2: First diagonal pair move forward
            self.set_leg_position('lf', 'forward')
            self.set_leg_position('rb', 'forward')
            rospy.sleep(self.PHASE_2_TIME * 0.5)
            
            # Phase 3: First diagonal pair lower to ground
            self.set_leg_position('lf', 'lower')
            self.set_leg_position('rb', 'lower')
            rospy.sleep(self.PHASE_3_TIME * 0.5)
            
            # Phase 4: First diagonal pair push
            self.set_leg_position('lf', 'push')
            self.set_leg_position('rb', 'push')
            # Prepare second pair for lift - gentle preparation
            self.set_leg_position('rf', 'stand')
            self.set_leg_position('lb', 'stand')
            rospy.sleep(self.PHASE_4_TIME * 0.5)
            
            # Phase 5: Second diagonal pair (RF+LB) lift
            self.set_leg_position('rf', 'lift')
            self.set_leg_position('lb', 'lift')
            # Maintain pressure on first pair - gentler to reduce hopping
            self.set_leg_position('lf', 'push')
            self.set_leg_position('rb', 'push')
            rospy.sleep(self.PHASE_1_TIME * 0.5)
            
            # Phase 6: Second diagonal pair move forward
            self.set_leg_position('rf', 'forward')
            self.set_leg_position('lb', 'forward')
            rospy.sleep(self.PHASE_2_TIME * 0.5)
            
            # Phase 7: Second diagonal pair lower to ground
            self.set_leg_position('rf', 'lower')
            self.set_leg_position('lb', 'lower')
            rospy.sleep(self.PHASE_3_TIME * 0.5)
            
            # Phase 8: Second diagonal pair push
            self.set_leg_position('rf', 'push')
            self.set_leg_position('lb', 'push')
            # Return first pair to neutral - gentler transition
            self.set_leg_position('lf', 'stand')
            self.set_leg_position('rb', 'stand')
            rospy.sleep(self.PHASE_4_TIME * 0.5)
            
            return True
            
        except rospy.ROSInterruptException:
            rospy.loginfo("Walk cycle interrupted")
            return False
    
    def rotate_cycle(self):
        """Execute one rotation cycle based on angular velocity"""
        try:
            # Scale rotation based on angular velocity
            rotation_scale = min(1.0, abs(self.angular_vel_z) / 0.5)  # Cap at max rotation of 0.5 rad/s
            rotation_amount = 0.05 * rotation_scale  # Scale rotation with velocity
            
            # Determine rotation direction
            direction = 1 if self.angular_vel_z > 0 else -1  # 1 for left, -1 for right
            
            # Set all legs in a more compact stance for rotation
            for leg in ['rf', 'lf', 'rb', 'lb']:
                self.set_leg_position(leg, 'stand')
            rospy.sleep(0.1)
            
            # Lift all legs slightly to reduce friction
            # Lift diagonal pairs alternately for stability
            self.set_leg_position('lf', 'lift')
            self.set_leg_position('rb', 'lift')
            rospy.sleep(0.1)
            
            # Adjust position for rotation - move left legs left, right legs right
            if direction > 0:  # Left rotation
                rospy.loginfo("Executing left rotation step")
                # For left turn, right legs move forward, left legs move backward
                self.set_leg_position('rf', 'forward')  # Right front moves forward
                self.set_leg_position('rb', 'push')     # Right back moves back
                self.set_leg_position('lf', 'push')     # Left front moves back
                self.set_leg_position('lb', 'forward')  # Left back moves forward
            else:  # Right rotation
                rospy.loginfo("Executing right rotation step")
                # For right turn, left legs move forward, right legs move backward
                self.set_leg_position('rf', 'push')     # Right front moves back
                self.set_leg_position('rb', 'forward')  # Right back moves forward
                self.set_leg_position('lf', 'forward')  # Left front moves forward
                self.set_leg_position('lb', 'push')     # Left back moves back
            
            rospy.sleep(0.2)
            
            # Lower the first diagonal pair
            self.set_leg_position('lf', 'stand')
            self.set_leg_position('rb', 'stand')
            rospy.sleep(0.1)
            
            # Lift the other diagonal pair
            self.set_leg_position('rf', 'lift')
            self.set_leg_position('lb', 'lift')
            rospy.sleep(0.1)
            
            # Complete the rotation step
            for leg in ['rf', 'lf', 'rb', 'lb']:
                self.set_leg_position(leg, 'stand')
            rospy.sleep(0.1)
            
            # Check if we should continue rotating
            time_since_last_cmd = (rospy.Time.now() - self.last_cmd_time).to_sec()
            if time_since_last_cmd > self.cmd_timeout.to_sec():
                rospy.loginfo("Command timeout reached, stopping rotation")
                self.walking = False
                self.stand()
                
            return True
        except Exception as e:
            rospy.logerr(f"Error in rotation cycle: {e}")
            return False
    
    def joint_states_callback(self, data):
        """Store current joint positions for verification"""
        for i, name in enumerate(data.name):
            if name in self.joint_pubs:
                self.joint_positions[name] = data.position[i]
    
    def model_states_callback(self, data):
        """Track robot position in the world"""
        try:
            robot_idx = data.name.index('puppy')
            pos = data.pose[robot_idx].position
            
            if self.initial_position is None:
                self.initial_position = (pos.x, pos.y, pos.z)
                rospy.loginfo(f"Initial position set: x={pos.x:.3f}, y={pos.y:.3f}, z={pos.z:.3f}")
            
            self.current_position = (pos.x, pos.y, pos.z)
        except ValueError:
            # Robot model not found in list, probably still spawning
            pass
    
    def stand(self):
        """Set the robot to a standing position"""
        rospy.loginfo("Setting standing position...")
        
        for leg in ['rf', 'lf', 'rb', 'lb']:
            self.set_leg_position(leg, 'stand')
        
        rospy.sleep(0.5)  # Give time for the robot to reach standing position
        rospy.loginfo("Standing position achieved")
    
    def run(self):
        """Main control loop"""
        self.stand()
        rospy.loginfo("Velocity Walker is running - listening for cmd_vel messages...")
        
        # Wait for the first cmd_vel message
        rospy.loginfo("Waiting for joystick commands - press buttons or move joystick")
        
        while not rospy.is_shutdown():
            # Check for timeout
            time_since_last_cmd = (rospy.Time.now() - self.last_cmd_time).to_sec()
            
            # If we're walking and velocity commands are still valid
            if self.walking and time_since_last_cmd < self.cmd_timeout.to_sec():
                if abs(self.angular_vel_z) > abs(self.linear_vel_x) * 2:
                    # If angular velocity dominates, execute a rotation cycle
                    self.rotate_cycle()
                else:
                    # Otherwise, execute a walking cycle
                    self.walk_cycle()
            else:
                # Wait for the next command
                self.rate.sleep()


if __name__ == '__main__':
    try:
        walker = VelocityWalker()
        walker.run()
    except rospy.ROSInterruptException:
        pass 