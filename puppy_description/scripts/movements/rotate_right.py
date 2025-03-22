#!/usr/bin/env python3
import rospy
from std_msgs.msg import Float64
from sensor_msgs.msg import JointState
from gazebo_msgs.msg import ModelStates
import signal
import sys
import time
import argparse
import math

class RightRotationController:
    """
    Joint controller for RIGHT rotation of the PuppyPi robot.
    Implements powerful movements for effective right rotation.
    """
    def __init__(self):
        rospy.init_node('right_rotation_controller', anonymous=True)
        
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
        
        # Walking parameters - optimized for faster rotation while maintaining stability
        self.STAND_HEIGHT = 0.12  # Height from ground to body
        self.STAND_WIDTH = 0.05   # Width between legs
        self.STAND_LENGTH = 0.07  # Length offset for standing position
        self.STEP_HEIGHT = 0.03   # Moderate step height for quicker yet controlled movement
        self.ROTATION_STEP = 0.09  # Larger rotation step for faster turning
        
        # Timing parameters - optimized for faster rotation
        self.BASE_PHASE_TIME = 0.18  # Faster for quicker rotation cycles
        self.TRANSITION_STEPS = 4     # Balance between speed and smoothness
        
        # State tracking
        self.joint_positions = {}
        self.initial_position = None
        self.current_position = None
        self.rotation_speed = 0.3  # Default rotation speed modifier
        self.rotating = False
        
        # Currently active position for each leg (for smooth transitions)
        self.current_leg_positions = {
            'rf': {'hip': 0.8, 'knee': 0.0},
            'lf': {'hip': 0.8, 'knee': 0.0},
            'rb': {'hip': 0.8, 'knee': 0.0},
            'lb': {'hip': 0.8, 'knee': 0.0}
        }
        
        # Setup signal handler for clean shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        
        rospy.loginfo("Starting Right Rotation Controller...")
        
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
        """Put the robot in standing position with smooth transition"""
        rospy.loginfo("Setting standing position...")
        
        # Target standing position
        stand_position = {
            'hip': 0.8,  # Approximately 45 degrees
            'knee': 0.0  # Straight knee
        }
        
        # Smoothly transition all legs to standing position
        for leg in ['rf', 'lf', 'rb', 'lb']:
            self.smooth_transition_to_position(leg, stand_position)
            
        rospy.sleep(0.7)  # Allow time to reach position
        rospy.loginfo("Standing position achieved")
    
    def smooth_transition_to_position(self, leg_name, target_position):
        """Make a quick but controlled transition to the target position for a leg"""
        # Get current position
        current_position = self.current_leg_positions[leg_name]
        
        # Calculate steps for smooth but quick transition
        steps = self.TRANSITION_STEPS
        hip_step = (target_position['hip'] - current_position['hip']) / steps
        knee_step = (target_position['knee'] - current_position['knee']) / steps
        
        # Execute quick but controlled transition
        for i in range(steps):
            # Calculate intermediate position
            current_position['hip'] += hip_step
            current_position['knee'] += knee_step
            
            # Apply position
            self.joint_pubs[f'{leg_name}_joint1'].publish(current_position['hip'])
            self.joint_pubs[f'{leg_name}_joint2'].publish(current_position['knee'])
            
            # Quick but not extreme sleep for faster movement
            rospy.sleep(0.015)  # 15ms for quicker transitions
        
        # Ensure final position is exactly the target
        self.joint_pubs[f'{leg_name}_joint1'].publish(target_position['hip'])
        self.joint_pubs[f'{leg_name}_joint2'].publish(target_position['knee'])
        
        # Update current position
        self.current_leg_positions[leg_name] = target_position.copy()
    
    def get_rotation_positions(self):
        """Define the optimized positions for effective right rotation"""
        # Positions optimized specifically for right rotation
        positions = {
            'stand': {
                'hip': 0.8,
                'knee': 0.0
            },
            # Clear right rotation positions - opposite of left rotation
            'right_forward': {  # Right legs push forward
                'hip': 1.4,     # Forward for right legs 
                'knee': 0.2     # Slight bend for traction
            },
            'left_backward': {  # Left legs push backward
                'hip': 0.2,     # Backward for left legs
                'knee': 0.2     # Slight bend for traction
            },
            # Clearance positions
            'left_lift': {     
                'hip': 0.8,
                'knee': -0.6    # Higher lift for faster clearance
            },
            'right_lift': {     
                'hip': 0.8,
                'knee': -0.6    # Higher lift for faster clearance
            }
        }
        return positions
    
    def rotation_cycle(self):
        """Execute a right rotation cycle with clear, effective movements"""
        # Get positions
        positions = self.get_rotation_positions()
        
        # Calculate phase timing
        phase_time = self.BASE_PHASE_TIME / self.rotation_speed
        
        # ---------- RIGHT ROTATION CYCLE ----------
        
        # Phase 1: Lift left legs to prepare for backward push
        self.smooth_transition_to_position('lf', positions['left_lift'])
        self.smooth_transition_to_position('lb', positions['left_lift'])
        rospy.sleep(phase_time * 0.2)
        
        # Phase 2: Right legs push forward, left legs push backward
        # This creates a rightward torque
        self.smooth_transition_to_position('rf', positions['right_forward'])
        self.smooth_transition_to_position('rb', positions['right_forward'])
        self.smooth_transition_to_position('lf', positions['left_backward'])
        self.smooth_transition_to_position('lb', positions['left_backward'])
        rospy.sleep(phase_time * 0.3)
        
        # Phase 3: Apply downward pressure for better grip
        for leg in ['rf', 'rb', 'lf', 'lb']:
            current = self.current_leg_positions[leg].copy()
            current['knee'] = 0.3  # Downward pressure for traction
            self.smooth_transition_to_position(leg, current)
        rospy.sleep(phase_time * 0.3)
        
        # Phase 4: Lift right legs to reposition
        self.smooth_transition_to_position('rf', positions['right_lift'])
        self.smooth_transition_to_position('rb', positions['right_lift'])
        rospy.sleep(phase_time * 0.2)
        
        # Phase 5: Return to start positions
        self.smooth_transition_to_position('rf', positions['right_forward'])
        self.smooth_transition_to_position('rb', positions['right_forward'])
        self.smooth_transition_to_position('lf', positions['left_backward'])
        self.smooth_transition_to_position('lb', positions['left_backward'])
        rospy.sleep(phase_time * 0.2)
    
    def rotate_continuously(self, duration=None):
        """Rotate right continuously for the specified duration with smooth transitions"""
        self.rotating = True
        rospy.loginfo(f"Starting right rotation at speed factor {self.rotation_speed:.2f}...")
        
        start_time = time.time()
        cycle_count = 0
        
        try:
            while (duration is None or time.time() - start_time < duration) and not rospy.is_shutdown():
                cycle_count += 1
                rospy.loginfo(f"Right rotation cycle {cycle_count}")
                self.rotation_cycle()
                
                # Check if we've reached the duration
                if duration is not None and time.time() - start_time >= duration:
                    break
        
        except rospy.ROSInterruptException:
            pass
        finally:
            rospy.loginfo("Stopping rotation and returning to standing position")
            self.rotating = False
            self.stand()

def main():
    """Main function to run the right rotation controller"""
    try:
        controller = RightRotationController()
        
        # Wait for everything to initialize
        rospy.loginfo("Waiting for initialization...")
        rospy.sleep(2.0)
        
        # Parse command line arguments
        parser = argparse.ArgumentParser(description='Rotate the robot to the right with powerful movement')
        parser.add_argument('--duration', type=float, default=5.0, help='Duration to rotate in seconds')
        parser.add_argument('--speed', type=float, default=0.3, help='Rotation speed factor')
        args = parser.parse_args()
        
        # Update controller speed if specified
        controller.rotation_speed = args.speed
        
        # Rotate for the specified duration
        rospy.loginfo(f"Starting right rotation for {args.duration} seconds at speed factor {args.speed}")
        controller.rotate_continuously(args.duration)
        
    except rospy.ROSInterruptException:
        pass

if __name__ == '__main__':
    main() 