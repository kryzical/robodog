#!/usr/bin/env python3
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
        
        # Subscribe to cmd_vel topic for velocity commands
        rospy.Subscriber('/cmd_vel', Twist, self.cmd_vel_callback)
        
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
        
        # State tracking
        self.joint_positions = {}
        self.initial_position = None
        self.current_position = None
        
        # Setup signal handler for clean shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        
        # Start in standing position
        self.stand()
        
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
        
        # Start walking if not already walking and linear velocity is non-zero
        if abs(self.linear_vel_x) > 0.01 and not self.walking:
            self.walking = True
            rospy.loginfo(f"Starting to walk with linear velocity: {self.linear_vel_x:.2f} m/s")
        
        # Stop walking if linear velocity is zero
        if abs(self.linear_vel_x) < 0.01 and self.walking:
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
            
            # Phase 7: Second diagonal pair lower
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
    
    def stand(self):
        """Put the robot in a standing position"""
        rospy.loginfo("Setting standing position...")
        
        # Move all legs to standing position with a slight delay for stability
        for leg in ['rf', 'lf', 'rb', 'lb']:
            self.set_leg_position(leg, 'stand')
            rospy.sleep(0.1)
        
        rospy.loginfo("Standing position achieved")
    
    def joint_states_callback(self, msg):
        """Store joint positions for verification"""
        joint_name_to_position = {}
        for i, name in enumerate(msg.name):
            joint_name_to_position[name] = msg.position[i]
            
        # Map Gazebo joint names to our joint names
        joint_mapping = {
            'rf_joint1': 'puppy::rf_joint1',
            'lf_joint1': 'puppy::lf_joint1',
            'rb_joint1': 'puppy::rb_joint1',
            'lb_joint1': 'puppy::lb_joint1',
            'rf_joint2': 'puppy::rf_joint2',
            'lf_joint2': 'puppy::lf_joint2',
            'rb_joint2': 'puppy::rb_joint2',
            'lb_joint2': 'puppy::lb_joint2'
        }
        
        for our_name, gazebo_name in joint_mapping.items():
            if gazebo_name in joint_name_to_position:
                self.joint_positions[our_name] = joint_name_to_position[gazebo_name]
        
    def model_states_callback(self, msg):
        """Track robot position using model states"""
        try:
            # Find the puppy model in the model_states message
            if 'puppy' in msg.name:
                idx = msg.name.index('puppy')
                pose = msg.pose[idx]
                
                # Update current position
                self.current_position = pose.position
                
                # Initialize start position if not set
                if self.initial_position is None:
                    self.initial_position = pose.position
                    rospy.loginfo(f"Initial position set: x={pose.position.x:.3f}, y={pose.position.y:.3f}, z={pose.position.z:.3f}")
        except:
            rospy.logwarn("Error processing model states")
    
    def run(self):
        """Main loop to process commands and control the robot"""
        rospy.loginfo("Velocity Walker is running - listening for cmd_vel messages...")
        
        while not rospy.is_shutdown():
            current_time = rospy.Time.now()
            
            # Check for timeout - stop if no commands received recently
            if (current_time - self.last_cmd_time) > self.cmd_timeout and self.walking:
                rospy.loginfo("Command timeout - stopping and returning to stand")
                self.walking = False
                self.stand()
            
            # If we should be walking, execute a walk cycle
            if self.walking:
                self.walk_cycle()
            
            self.rate.sleep()

if __name__ == '__main__':
    try:
        walker = VelocityWalker()
        walker.run()
    except rospy.ROSInterruptException:
        pass 