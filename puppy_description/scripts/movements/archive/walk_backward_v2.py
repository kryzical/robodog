#!/usr/bin/env python3
import rospy
from std_msgs.msg import Float64
import time
import argparse
import sys

def walk_backward(speed=0.2, duration=10.0):
    """
    Make the robot walk backward by directly controlling joint positions
    rather than using the velocity walker's cmd_vel interpretation.
    
    Args:
        speed (float): Speed scale, higher is faster (default: 0.2)
        duration (float): How long to walk in seconds (default: 10.0)
    """
    rospy.init_node('direct_backward_walker', anonymous=True)
    
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
    rospy.loginfo("Waiting for connections to establish...")
    time.sleep(1)
    
    # Walking parameters - adjusted for backward motion
    stand_height = 0.12  # Height from ground to body
    stand_width = 0.05   # Width between legs
    stand_length = 0.07  # Length offset for standing position
    step_height = 0.03   # Height for leg lifting
    step_length = 0.05 * speed  # Length of step, scaled by speed
    
    # Timing parameters - adjusted based on speed
    base_time = 0.1 / speed
    phase_1_time = base_time  # Time for lifting leg
    phase_2_time = base_time  # Time for moving leg backward
    phase_3_time = base_time  # Time for lowering leg
    phase_4_time = base_time  # Time for pushing forward
    
    # Function to set leg joint positions for backward walking
    def set_leg_position(leg_name, phase):
        """Set a leg to a specific position for backward movement"""
        # Simple approach without IK - using direct angle control optimized for backward motion
        # REVERSED angles compared to the forward walking pattern
        
        if phase == 'stand':
            hip_angle = 0.8  # Approximately 45 degrees
            knee_angle = 0.0
        elif phase == 'lift':
            hip_angle = 0.9  # Increase hip angle to lift
            knee_angle = -0.2  # Bend knee slightly
        elif phase == 'backward':  # This phase moves leg backward (opposite of forward)
            hip_angle = 1.0  # Higher hip angle for backward motion
            knee_angle = -0.2  # Keep knee bent
        elif phase == 'lower':
            hip_angle = 1.0  # Keep hip angle for backward
            knee_angle = -0.1  # Start straightening knee
        elif phase == 'push':  # This phase pushes leg forward (opposite of push back)
            hip_angle = 0.7  # Lower hip angle for forward push (gives backward motion)
            knee_angle = 0.1  # Slight backward bend for push
        
        # Apply the angles
        joint_pubs[f'{leg_name}_joint1'].publish(hip_angle)
        joint_pubs[f'{leg_name}_joint2'].publish(knee_angle)
    
    # First, ensure the robot is in standing position
    rospy.loginfo("Setting initial standing position...")
    for leg in ['rf', 'lf', 'rb', 'lb']:
        set_leg_position(leg, 'stand')
    time.sleep(1.0)
    
    # Start backward walking
    rospy.loginfo(f"Starting to walk backward at speed scale {speed:.2f} for {duration:.1f} seconds")
    start_time = time.time()
    cycle_count = 0
    
    try:
        while time.time() - start_time < duration and not rospy.is_shutdown():
            cycle_count += 1
            rospy.loginfo(f"Backward walk cycle {cycle_count}")
            
            # Phase 1: First diagonal pair (RF+LB) lift
            set_leg_position('rf', 'lift')
            set_leg_position('lb', 'lift')
            set_leg_position('lf', 'push')  # Help with balance and movement
            set_leg_position('rb', 'push')  # Help with balance and movement
            time.sleep(phase_1_time)
            
            # Phase 2: First diagonal pair move backward
            set_leg_position('rf', 'backward')
            set_leg_position('lb', 'backward')
            time.sleep(phase_2_time)
            
            # Phase 3: First diagonal pair lower to ground
            set_leg_position('rf', 'lower')
            set_leg_position('lb', 'lower')
            time.sleep(phase_3_time)
            
            # Phase 4: First diagonal pair push forward (for backward motion)
            set_leg_position('rf', 'push')
            set_leg_position('lb', 'push')
            set_leg_position('lf', 'stand')  # Prepare second pair
            set_leg_position('rb', 'stand')  # Prepare second pair
            time.sleep(phase_4_time)
            
            # Phase 5: Second diagonal pair (LF+RB) lift
            set_leg_position('lf', 'lift')
            set_leg_position('rb', 'lift')
            set_leg_position('rf', 'push')  # Maintain pressure
            set_leg_position('lb', 'push')  # Maintain pressure
            time.sleep(phase_1_time)
            
            # Phase 6: Second diagonal pair move backward
            set_leg_position('lf', 'backward')
            set_leg_position('rb', 'backward')
            time.sleep(phase_2_time)
            
            # Phase 7: Second diagonal pair lower to ground
            set_leg_position('lf', 'lower')
            set_leg_position('rb', 'lower')
            time.sleep(phase_3_time)
            
            # Phase 8: Second diagonal pair push forward (for backward motion)
            set_leg_position('lf', 'push')
            set_leg_position('rb', 'push')
            time.sleep(phase_4_time)
            
            # Check elapsed time to decide whether to continue
            if time.time() - start_time >= duration:
                break
                
    except rospy.ROSInterruptException:
        pass
    finally:
        # Return to standing position
        rospy.loginfo("Backward walking completed, returning to standing position")
        for leg in ['rf', 'lf', 'rb', 'lb']:
            set_leg_position(leg, 'stand')
        time.sleep(1.0)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Directly control the robot to walk backward')
    parser.add_argument('--speed', type=float, default=0.2, help='Speed scale, higher is faster (default: 0.2)')
    parser.add_argument('--duration', type=float, default=10.0, help='Duration in seconds (default: 10.0)')
    args = parser.parse_args()
    
    try:
        walk_backward(args.speed, args.duration)
    except rospy.ROSInterruptException:
        pass 