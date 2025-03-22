#!/usr/bin/env python3
import rospy
from std_msgs.msg import Float64
from sensor_msgs.msg import JointState
from gazebo_msgs.msg import ModelStates
from geometry_msgs.msg import Twist
import signal
import sys
import time

class ReverseVelocityWalker:
    """
    A controller that makes the robot walk backward by directly implementing
    a reversed version of the original walking gait.
    
    This intentionally copies and exactly reverses the original velocity_walker.py
    to ensure proper backward motion.
    """
    def __init__(self):
        rospy.init_node('reverse_velocity_walker', anonymous=True)
        
        # Initialize joints
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
        
        # Walking parameters - copied from velocity_walker.py
        self.STAND_HEIGHT = 0.12  # Height from ground to body
        self.STAND_WIDTH = 0.05   # Width between legs
        self.STAND_LENGTH = 0.07  # Length offset for standing position
        self.STEP_HEIGHT = 0.03   # Height for leg lifting
        self.STEP_LENGTH = 0.05   # Length of step
        
        # Timing parameters - matching velocity_walker.py
        self.PHASE_1_TIME = 0.12  # Time for lifting leg
        self.PHASE_2_TIME = 0.10  # Time for moving leg
        self.PHASE_3_TIME = 0.12  # Time for lowering leg
        self.PHASE_4_TIME = 0.10  # Time for pushing
        
        # State tracking
        self.joint_positions = {}
        self.initial_position = None
        self.current_position = None
        self.walking = False
        self.speed = 0.2  # Default speed
        
        # Setup signal handler for clean shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        
        rospy.loginfo("Starting Reverse Velocity Walker - walks backward only...")
        
        # Start in standing position
        self.stand()
        
    def signal_handler(self, sig, frame):
        """Handle SIGINT for clean shutdown"""
        rospy.loginfo("Shutting down...")
        self.stand()
        sys.exit(0)
        
    def joint_states_callback(self, msg):
        """Process joint state information"""
        for i, name in enumerate(msg.name):
            self.joint_positions[name] = msg.position[i]
            
    def model_states_callback(self, msg):
        """Track the robot's position in the world"""
        try:
            idx = msg.name.index('puppy')
            pos = msg.pose[idx].position
            
            if self.initial_position is None:
                self.initial_position = (pos.x, pos.y, pos.z)
                rospy.loginfo(f"Initial position set: x={pos.x:.3f}, y={pos.y:.3f}, z={pos.z:.3f}")
                
            self.current_position = (pos.x, pos.y, pos.z)
        except ValueError:
            pass  # puppy model not found yet
            
    def stand(self):
        """Put the robot in standing position"""
        rospy.loginfo("Setting standing position...")
        
        # Set all legs to standing position
        for leg in ['rf', 'lf', 'rb', 'lb']:
            x, y, z = self.calculate_leg_positions('stand', leg)
            self.set_leg_position(leg, 'stand')
            
        rospy.sleep(0.5)  # Allow time to reach position
        rospy.loginfo("Standing position achieved")
        
    def calculate_leg_positions(self, phase, leg):
        """Calculate leg positions based on phase and leg - REVERSED from original"""
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
        
        # Apply phase-specific modifications - COMPLETELY REVERSED from velocity_walker.py
        # The original code had comments saying "REVERSED FOR FORWARD MOTION"
        # So we're reversing those reversals to get backward motion
        if phase == 'stand':
            # No modifications, use default standing position
            pass
        elif phase == 'lift':
            z = -(self.STAND_HEIGHT - self.STEP_HEIGHT)  # Lift leg up
        elif phase == 'forward':
            z = -(self.STAND_HEIGHT - self.STEP_HEIGHT)  # Keep leg up
            # Move leg forward - NOT reversed like in original (reversing the reversal)
            if leg in ['rf', 'lf']:
                x = self.STAND_LENGTH + self.STEP_LENGTH  # NOT reversed 
            else:
                x = -self.STAND_LENGTH + self.STEP_LENGTH  # NOT reversed
        elif phase == 'lower':
            # Position leg forward before lowering - NOT reversed like in original
            if leg in ['rf', 'lf']:
                x = self.STAND_LENGTH + self.STEP_LENGTH  # NOT reversed
            else:
                x = -self.STAND_LENGTH + self.STEP_LENGTH  # NOT reversed
        elif phase == 'push':
            # Push leg back - NOT reversed like in original
            if leg in ['rf', 'lf']:
                x = self.STAND_LENGTH - self.STEP_LENGTH  # NOT reversed
            else:
                x = -self.STAND_LENGTH - self.STEP_LENGTH  # NOT reversed
        
        return x, y, z
    
    def set_leg_position(self, leg_name, phase):
        """Set a leg to a specific position with direct angle control"""
        x, y, z = self.calculate_leg_positions(phase, leg_name)
        
        # Simple case without IK - directly reversed from velocity_walker.py
        if phase == 'stand':
            hip_angle = 0.8  # Approximately 45 degrees
            knee_angle = 0.0
        elif phase == 'lift':
            hip_angle = 0.9  # Increase hip angle to lift
            knee_angle = -0.2  # Bend knee slightly
        elif phase == 'forward':
            # NOT REVERSED from the original that was marked "REVERSED for forward motion"
            hip_angle = 1.0  # Higher hip angle (NOT reversed)
            knee_angle = -0.2  # Keep knee bent
        elif phase == 'lower':
            hip_angle = 1.0  # Keep hip angle (NOT reversed)
            knee_angle = -0.1  # Start straightening knee
        elif phase == 'push':
            # NOT REVERSED from the original that was marked "REVERSED for forward motion"
            hip_angle = 0.7  # Lower hip angle to push (NOT reversed)
            knee_angle = 0.1  # Slight backward bend for push
        
        # Apply the angles
        self.joint_pubs[f'{leg_name}_joint1'].publish(hip_angle)
        self.joint_pubs[f'{leg_name}_joint2'].publish(knee_angle)
    
    def walk_cycle(self):
        """Execute one walking cycle - completely reversed from original"""
        step_scale = 1.0  # Full step size
        self.STEP_LENGTH = 0.05 * step_scale
        
        # Begin with a stable position
        for leg in ['rf', 'lf', 'rb', 'lb']:
            self.set_leg_position(leg, 'stand')
        rospy.sleep(0.05)
        
        # Phase 1: First diagonal pair (LF+RB) lift and prepare
        self.set_leg_position('lf', 'lift')
        self.set_leg_position('rb', 'lift')
        # Adjust other legs for better balance
        self.set_leg_position('rf', 'push')
        self.set_leg_position('lb', 'push')
        rospy.sleep(self.PHASE_1_TIME * 0.5)
        
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
        # Prepare second pair for lift
        self.set_leg_position('rf', 'stand')
        self.set_leg_position('lb', 'stand')
        rospy.sleep(self.PHASE_4_TIME * 0.5)
        
        # Phase 5: Second diagonal pair (RF+LB) lift
        self.set_leg_position('rf', 'lift')
        self.set_leg_position('lb', 'lift')
        # Maintain pressure on first pair
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
        
        # Phase 8: Second diagonal pair push and reset first pair
        self.set_leg_position('rf', 'push')
        self.set_leg_position('lb', 'push')
        self.set_leg_position('lf', 'stand')
        self.set_leg_position('rb', 'stand')
        rospy.sleep(self.PHASE_4_TIME * 0.5)
    
    def walk_continuously(self, duration=None):
        """Walk backward continuously for the specified duration"""
        self.walking = True
        rospy.loginfo(f"Starting to walk backward...")
        
        start_time = time.time()
        cycle_count = 0
        
        try:
            while (duration is None or time.time() - start_time < duration) and not rospy.is_shutdown():
                cycle_count += 1
                rospy.loginfo(f"Backward cycle {cycle_count}")
                self.walk_cycle()
                
                # Check if we've reached the duration
                if duration is not None and time.time() - start_time >= duration:
                    break
        
        except rospy.ROSInterruptException:
            pass
        finally:
            rospy.loginfo("Stopping backward walking and returning to standing position")
            self.walking = False
            self.stand()

def main():
    """Main function to run the reverse velocity walker"""
    try:
        walker = ReverseVelocityWalker()
        
        # Wait for everything to initialize
        rospy.loginfo("Waiting for initialization...")
        rospy.sleep(2.0)
        
        # Parse command line arguments
        import argparse
        parser = argparse.ArgumentParser(description='Walk the robot backward')
        parser.add_argument('--duration', type=float, default=10.0, help='Duration to walk in seconds')
        parser.add_argument('--speed', type=float, default=0.2, help='Walking speed factor')
        args = parser.parse_args()
        
        # Update walker speed if specified
        walker.speed = args.speed
        
        # Walk for the specified duration
        rospy.loginfo(f"Starting backward walking for {args.duration} seconds at speed {args.speed}")
        walker.walk_continuously(args.duration)
        
    except rospy.ROSInterruptException:
        pass

if __name__ == '__main__':
    main() 