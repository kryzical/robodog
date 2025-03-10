#!/usr/bin/env python3
# coding=utf8
"""
Walking controller for the puppy quadruped robot.
Uses the common robot controller library for joint control.
"""

import rospy
import math
import time
from geometry_msgs.msg import Twist
from robot_controller_lib import PuppyJointController

class PuppyWalkingController(PuppyJointController):
    def __init__(self):
        """Initialize the walking controller"""
        super().__init__(node_name='walking_controller')
        
        # Gait parameters
        self.gait_config = {
            'trot': {
                'swing_time': 0.3,
                'stance_time': 0.3,
                'overlap_time': 0.1,
                'z_clearance': 0.05,
                'step_length': 0.1
            }
        }
        
        # Movement parameters
        self.current_speed = {'x': 0, 'y': 0, 'yaw': 0}
        self.cmd_vel_sub = rospy.Subscriber('cmd_vel', Twist, self.cmd_vel_callback)
        
        # Joint name mapping for walking algorithm
        self.joint_name_map = {
            'rf_joint1': 'rf_hip',
            'rf_joint2': 'rf_knee',
            'lf_joint1': 'lf_hip',
            'lf_joint2': 'lf_knee',
            'rb_joint1': 'rb_hip',
            'rb_joint2': 'rb_knee',
            'lb_joint1': 'lb_hip',
            'lb_joint2': 'lb_knee'
        }

    def cmd_vel_callback(self, msg):
        """Handle incoming velocity commands"""
        self.current_speed['x'] = msg.linear.x
        self.current_speed['y'] = msg.linear.y
        self.current_speed['yaw'] = msg.angular.z

    def calculate_leg_positions(self, t, gait='trot'):
        """Calculate leg positions based on gait pattern and timing"""
        config = self.gait_config[gait]
        cycle_time = config['swing_time'] + config['stance_time']
        phase = (t % cycle_time) / cycle_time
        positions = {}
        
        # Define leg pairs for trot gait
        diagonal_pairs = [
            (['rf_joint1', 'rf_joint2', 'lb_joint1', 'lb_joint2'], 0),
            (['lf_joint1', 'lf_joint2', 'rb_joint1', 'rb_joint2'], 0.5)
        ]
        
        for pair, phase_offset in diagonal_pairs:
            pair_phase = (phase + phase_offset) % 1.0
            
            # Swing phase
            if pair_phase < config['swing_time'] / cycle_time:
                swing_progress = pair_phase / (config['swing_time'] / cycle_time)
                height = config['z_clearance'] * math.sin(swing_progress * math.pi)
                x_offset = config['step_length'] * (1 - 2 * swing_progress)
            # Stance phase
            else:
                height = 0
                stance_progress = (pair_phase - config['swing_time'] / cycle_time) / (config['stance_time'] / cycle_time)
                x_offset = config['step_length'] * (2 * stance_progress - 1)
            
            for joint in pair:
                if joint.endswith('joint1'):  # Hip joint
                    positions[self.joint_name_map[joint]] = x_offset
                else:  # Knee joint
                    positions[self.joint_name_map[joint]] = -0.8 - height  # Base stance + height adjustment
        
        return positions

    def walk(self):
        """Execute walking sequence"""
        print("Starting walking controller...")
        
        # First stand up
        self.stand_before_walking()
        
        rate = rospy.Rate(50)  # 50Hz control rate
        start_time = time.time()
        
        try:
            while not rospy.is_shutdown():
                t = time.time() - start_time
                
                # Calculate leg positions
                positions = self.calculate_leg_positions(t)
                
                # Apply speed scaling
                if abs(self.current_speed['x']) > 0.01:
                    speed_factor = abs(self.current_speed['x']) / 0.5  # 0.5 m/s max speed
                    for joint, position in positions.items():
                        if joint.endswith('hip'):  # Scale only hip joints for speed
                            positions[joint] *= speed_factor
                    
                    # Send the commands
                    self.send_joint_commands(positions)
                else:
                    # If not moving, maintain a stable standing posture
                    self.stand_in_place()
                
                rate.sleep()
        except rospy.ROSInterruptException:
            pass
    
    def stand_before_walking(self):
        """Get into a ready position before walking"""
        # Initial standing position (same as in stand_up.py)
        x = -0.08
        y = 0
        z = -0.12
        
        front_hip, front_knee = self.calculate_leg_ik(x, y, z, is_front=True)
        back_hip, back_knee = self.calculate_leg_ik(x, y, z, is_front=False)
        
        standing_positions = {
            'rf_hip': front_hip, 'rf_knee': front_knee,
            'lf_hip': front_hip, 'lf_knee': front_knee,
            'rb_hip': back_hip, 'rb_knee': back_knee,
            'lb_hip': back_hip, 'lb_knee': back_knee
        }
        
        # First reset joints
        self.reset_pose()
        rospy.sleep(0.5)
        
        # Then move to standing position
        self.send_joint_commands(standing_positions)
        rospy.sleep(1.0)
    
    def stand_in_place(self):
        """Maintain a stable standing position when not walking"""
        x = -0.08
        y = 0
        z = -0.12
        
        front_hip, front_knee = self.calculate_leg_ik(x, y, z, is_front=True)
        back_hip, back_knee = self.calculate_leg_ik(x, y, z, is_front=False)
        
        standing_positions = {
            'rf_hip': front_hip, 'rf_knee': front_knee,
            'lf_hip': front_hip, 'lf_knee': front_knee,
            'rb_hip': back_hip, 'rb_knee': back_knee,
            'lb_hip': back_hip, 'lb_knee': back_knee
        }
        
        self.send_joint_commands(standing_positions)

def main():
    try:
        controller = PuppyWalkingController()
        controller.walk()
    except Exception as e:
        rospy.logerr(f"Error: {e}")

if __name__ == '__main__':
    main()