#!/usr/bin/env python3
# coding=utf8

import sys
import math
import rospy
import time
from std_msgs.msg import Float64
from sensor_msgs.msg import JointState

ROS_NODE_NAME = 'puppy_demo'

PuppyMove = {'x': 6, 'y': 0, 'yaw_rate': 0}
# x: forward control, forward direction is positive, unit cm/s
# y: lateral control, left direction is positive, unit cm/s (not implemented)
# yaw_rate: turn control, counterclockwise is positive, unit rad/s

PuppyPose = {'roll': math.radians(0), 'pitch': math.radians(0), 'yaw': 0.000, 
             'height': -10, 'x_shift': 0.5, 'stance_x': 0, 'stance_y': 0,
             'circle_radius': 0.2, 'circle_speed': 2.0}  # Added circle parameters
# stance_x: extra distance apart for legs on X-axis (cm)
# stance_y: extra distance apart for legs on Y-axis (cm)
# x_shift: shared x-axis movement, affects balance (cm)
# height: vertical distance from toe to thigh rotation axis (cm)
# pitch: body pitch angle (radians)
# circle_radius: radius of circular motion (radians)
# circle_speed: speed of circular motion (radians/second)

# Gait selection
gait = 'Trot'  # Options: 'Trot', 'Amble', 'Walk'

# Gait configurations
GaitConfig = {}
if gait == 'Trot':
    GaitConfig = {'overlap_time': 0.2, 'swing_time': 0.3, 'clearance_time': 0.0, 'z_clearance': 5}
    PuppyPose['x_shift'] = -0.6
    # Trot gait clearance_time = 0
elif gait == 'Amble':
    GaitConfig = {'overlap_time': 0.1, 'swing_time': 0.2, 'clearance_time': 0.1, 'z_clearance': 5}
    PuppyPose['x_shift'] = -0.9
    # Amble gait 0 < clearance_time < swing_time
elif gait == 'Walk':
    GaitConfig = {'overlap_time': 0.1, 'swing_time': 0.2, 'clearance_time': 0.3, 'z_clearance': 5}
    PuppyPose['x_shift'] = -0.65
    # Walk gait swing_time ≤ clearance_time

# Joint state feedback
current_joint_states = None

def calculate_leg_positions(t, gait_config, move_params, pose_params):
    """Calculate positions for all legs based on gait pattern and timing"""
    positions = {}
    
    # Period of a complete step cycle
    period = gait_config['swing_time'] + gait_config['overlap_time']
    phase = (t % period) / period
    
    # Base positions from pose parameters
    base_lift = -0.3 - (pose_params['height'] / 100.0)
    base_forward = 0.6 + (pose_params['x_shift'] / 100.0)
    stance_x_adj = pose_params['stance_x'] / 100.0
    
    # Calculate circular motion
    circle_angle = t * pose_params['circle_speed']
    circle_x = math.cos(circle_angle) * pose_params['circle_radius']
    circle_y = math.sin(circle_angle) * pose_params['circle_radius']
    
    # Calculate leg phases based on gait type
    if gait == 'Trot':
        # Diagonal pairs move together
        lf_phase = phase
        rf_phase = (phase + 0.5) % 1.0
        lb_phase = rf_phase
        rb_phase = lf_phase
    elif gait == 'Amble':
        # Legs move in sequence with overlap
        lf_phase = phase
        rf_phase = (phase + 0.25) % 1.0
        lb_phase = (phase + 0.5) % 1.0
        rb_phase = (phase + 0.75) % 1.0
    elif gait == 'Walk':
        # Each leg moves independently
        lf_phase = phase
        rf_phase = (phase + 0.25) % 1.0
        rb_phase = (phase + 0.5) % 1.0
        lb_phase = (phase + 0.75) % 1.0
    
    # Calculate positions for each leg
    def leg_motion(phase, is_front):
        swing_portion = gait_config['swing_time'] / period
        if phase < swing_portion:
            # Swing phase
            swing_progress = phase / swing_portion
            height_factor = math.sin(swing_progress * math.pi) * (gait_config['z_clearance'] / 100.0)
            forward_factor = math.cos(swing_progress * math.pi * 2) * 0.3
            
            j1 = base_lift - height_factor + (pose_params['pitch'] if is_front else -pose_params['pitch']) + circle_y
            j2 = base_forward + forward_factor + (stance_x_adj if is_front else -stance_x_adj) + circle_x
        else:
            # Stance phase
            j1 = base_lift + (pose_params['pitch'] if is_front else -pose_params['pitch']) + circle_y
            j2 = base_forward + (stance_x_adj if is_front else -stance_x_adj) + circle_x
        
        return j1, j2
    
    # Apply leg motions
    positions['lf_joint1'], positions['lf_joint2'] = leg_motion(lf_phase, True)
    positions['rf_joint1'], positions['rf_joint2'] = leg_motion(rf_phase, True)
    positions['lb_joint1'], positions['lb_joint2'] = leg_motion(lb_phase, False)
    positions['rb_joint1'], positions['rb_joint2'] = leg_motion(rb_phase, False)
    
    # Apply movement adjustments
    speed_factor = move_params['x'] / 15.0
    for joint in positions:
        if joint.endswith('joint2'):
            if 'f_' in joint:  # Front legs
                positions[joint] -= speed_factor * 0.2
            else:  # Back legs
                positions[joint] += speed_factor * 0.2
    
    # Apply turn adjustments
    turn_factor = move_params['yaw_rate'] * 0.3
    positions['lf_joint1'] += turn_factor
    positions['rf_joint1'] -= turn_factor
    positions['lb_joint1'] += turn_factor
    positions['rb_joint1'] -= turn_factor
    
    return positions

def cleanup():
    """Clean up function called on shutdown"""
    print('Shutting down...')
    # Set all joint positions to safe values
    for pub in joint_pubs.values():
        pub.publish(0.0)

def joint_states_callback(msg):
    """Callback function for joint state subscriber"""
    global current_joint_states
    current_joint_states = msg

if __name__ == '__main__':
    try:
        # Initialize ROS node
        rospy.init_node(ROS_NODE_NAME, log_level=rospy.INFO)
        rospy.on_shutdown(cleanup)
        
        # Create publishers for each joint
        joint_pubs = {
            'lf_joint1': rospy.Publisher('/puppy/joint2_position_controller/command', Float64, queue_size=1),
            'lf_joint2': rospy.Publisher('/puppy/joint6_position_controller/command', Float64, queue_size=1),
            'rf_joint1': rospy.Publisher('/puppy/joint1_position_controller/command', Float64, queue_size=1),
            'rf_joint2': rospy.Publisher('/puppy/joint5_position_controller/command', Float64, queue_size=1),
            'lb_joint1': rospy.Publisher('/puppy/joint4_position_controller/command', Float64, queue_size=1),
            'lb_joint2': rospy.Publisher('/puppy/joint8_position_controller/command', Float64, queue_size=1),
            'rb_joint1': rospy.Publisher('/puppy/joint3_position_controller/command', Float64, queue_size=1),
            'rb_joint2': rospy.Publisher('/puppy/joint7_position_controller/command', Float64, queue_size=1)
        }
        
        # Subscribe to joint states for feedback
        rospy.Subscriber('/puppy/joint_states', JointState, joint_states_callback)
        
        # Wait for publishers to connect
        rospy.sleep(1.0)
        
        print(f"Starting motion with gait: {gait}")
        print(f"Height: {PuppyPose['height']}cm, X-shift: {PuppyPose['x_shift']}cm")
        print(f"Circle radius: {PuppyPose['circle_radius']} rad, Speed: {PuppyPose['circle_speed']} rad/s")
        print("Press Ctrl+C to stop")
        
        # Start from zero position
        initial_positions = calculate_leg_positions(0, GaitConfig, {'x': 0, 'y': 0, 'yaw_rate': 0}, PuppyPose)
        
        # Gradually move to initial position
        steps = 50
        rate = rospy.Rate(20)
        current_positions = {joint: 0.0 for joint in initial_positions.keys()}
        
        # Smooth transition to initial pose
        for step in range(steps):
            progress = step / float(steps)
            smooth_progress = math.sin(progress * math.pi / 2)
            
            for joint in initial_positions.keys():
                target = initial_positions[joint]
                new_position = target * smooth_progress
                joint_pubs[joint].publish(new_position)
            
            rate.sleep()
        
        print("Initial position reached, starting gait...")
        
        # Main control loop
        start_time = time.time()
        rate = rospy.Rate(50)  # 50Hz control rate
        
        while not rospy.is_shutdown():
            t = time.time() - start_time
            
            # Calculate and publish joint positions
            positions = calculate_leg_positions(t, GaitConfig, PuppyMove, PuppyPose)
            for joint, position in positions.items():
                joint_pubs[joint].publish(position)
            
            rate.sleep()
            
    except rospy.ROSInterruptException:
        pass
    
    except Exception as e:
        rospy.logerr(f"Error: {e}")
        for pub in joint_pubs.values():
            pub.publish(0.0)
