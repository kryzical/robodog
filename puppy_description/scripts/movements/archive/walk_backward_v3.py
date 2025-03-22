#!/usr/bin/env python3
import rospy
from std_msgs.msg import Float64
import time
import argparse
import sys

def walk_backward(speed=0.3, duration=10.0):
    """
    Make the robot walk backward using aggressive joint positions
    with much stronger forces to ensure backward motion.
    
    Args:
        speed (float): Speed scale, higher is faster (default: 0.3)
        duration (float): How long to walk in seconds (default: 10.0)
    """
    rospy.init_node('aggressive_backward_walker', anonymous=True)
    
    # Joint publishers
    joint_pubs = {}
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
        joint_pubs[joint_name] = pub
    
    # Give time for publishers to connect
    rospy.loginfo("Initializing aggressive backward walker...")
    time.sleep(1)
    
    # Timing adjusted for more aggressive movement
    cycle_time = 0.07 / speed  # Faster cycle time for more aggressive movement
    
    # AGGRESSIVE angle settings for backward motion
    # These are deliberately more extreme to create stronger backward force
    angles = {
        'stand': {
            'hip': 0.8,
            'knee': 0.0
        },
        'extreme_back': {  # Position far back for strong push
            'hip': 0.4,    # Much lower angle moves leg back
            'knee': 0.2    # Slight bend for force
        },
        'lift': {
            'hip': 1.1,    # Higher hip angle for more lift
            'knee': -0.3   # More bend
        },
        'forward_high': {  # High forward position to prepare for push
            'hip': 1.2,    # Even higher angle
            'knee': -0.3   # Keep the bend
        },
        'push_down': {     # Powerful pushing action
            'hip': 0.5,    # Strong push angle
            'knee': 0.3    # Extended for force
        }
    }
    
    # Function to set leg joint positions for aggressive backward walking
    def set_leg_position(leg_name, position):
        """Set a leg to a specific position with strong angles for backward motion"""
        hip_angle = angles[position]['hip']
        knee_angle = angles[position]['knee']
        
        # Apply the angles
        joint_pubs[f'{leg_name}_joint1'].publish(hip_angle)
        joint_pubs[f'{leg_name}_joint2'].publish(knee_angle)
    
    # Reset to standing position at start
    rospy.loginfo("Setting initial standing position...")
    for leg in ['rf', 'lf', 'rb', 'lb']:
        set_leg_position(leg, 'stand')
    time.sleep(1.0)
    
    # Start backward walking
    rospy.loginfo(f"Starting AGGRESSIVE backward walking at speed {speed:.2f} for {duration:.1f} seconds")
    start_time = time.time()
    cycle_count = 0
    
    try:
        while time.time() - start_time < duration and not rospy.is_shutdown():
            cycle_count += 1
            rospy.loginfo(f"Backward walk cycle {cycle_count}")
            
            # Aggressive backward gait pattern - all legs coordinated for maximum force
            
            # PHASE 1: Front legs push back strongly, rear legs prepare
            set_leg_position('rf', 'push_down')
            set_leg_position('lf', 'push_down')
            set_leg_position('rb', 'lift')
            set_leg_position('lb', 'lift')
            time.sleep(cycle_time)
            
            # PHASE 2: Front legs reach extreme back position
            set_leg_position('rf', 'extreme_back')
            set_leg_position('lf', 'extreme_back')
            set_leg_position('rb', 'forward_high')
            set_leg_position('lb', 'forward_high')
            time.sleep(cycle_time)
            
            # PHASE 3: Rear legs push while front legs reset
            set_leg_position('rf', 'lift')
            set_leg_position('lf', 'lift')
            set_leg_position('rb', 'push_down')
            set_leg_position('lb', 'push_down')
            time.sleep(cycle_time)
            
            # PHASE 4: Rear legs reach extreme position while front legs prepare next push
            set_leg_position('rf', 'forward_high')
            set_leg_position('lf', 'forward_high')
            set_leg_position('rb', 'extreme_back')
            set_leg_position('lb', 'extreme_back')
            time.sleep(cycle_time)
            
            # Add a small pause between cycles for stability if needed
            if cycle_count % 5 == 0:
                for leg in ['rf', 'lf', 'rb', 'lb']:
                    set_leg_position(leg, 'stand')
                time.sleep(0.1)
            
            # Check if we've reached the duration
            if time.time() - start_time >= duration:
                break
                
    except rospy.ROSInterruptException:
        pass
    finally:
        # Return to standing position
        rospy.loginfo("Aggressive backward walking completed, returning to standing position")
        for leg in ['rf', 'lf', 'rb', 'lb']:
            set_leg_position(leg, 'stand')
        time.sleep(1.0)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Aggressively control the robot to walk backward')
    parser.add_argument('--speed', type=float, default=0.3, help='Speed scale, higher is faster (default: 0.3)')
    parser.add_argument('--duration', type=float, default=10.0, help='Duration in seconds (default: 10.0)')
    args = parser.parse_args()
    
    try:
        walk_backward(args.speed, args.duration)
    except rospy.ROSInterruptException:
        pass 