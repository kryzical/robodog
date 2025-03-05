#!/usr/bin/env python3
# coding=utf8

import sys
import math
import rospy
import time
from std_msgs.msg import Float64
from sensor_msgs.msg import JointState

class PuppyController:
    def __init__(self, sim_mode=True):
        self.sim_mode = sim_mode
        self.node_name = 'puppy_stand'
        rospy.init_node(self.node_name, log_level=rospy.INFO)
        
        # Default pose parameters - adjusted for more stability
        self.pose_params = {
            'roll': math.radians(0),
            'pitch': math.radians(0),
            'yaw': 0.000,
            'height': -8,    # Reduced height for lower center of gravity
            'x_shift': 0.8,  # Increased forward shift for better balance
            'stance_x': 2,   # Wider stance for stability
            'stance_y': 1    # Slight widening of stance
        }
        
        # Initialize publishers
        self.setup_publishers()
        
        # Subscribe to joint states for feedback
        rospy.Subscriber('/puppy/joint_states', JointState, self.joint_states_callback)
        self.current_joint_states = None
        
        # Register shutdown hook
        rospy.on_shutdown(self.cleanup)
    
    def setup_publishers(self):
        """Setup publishers for joint control"""
        if self.sim_mode:
            self.joint_pubs = {
                'lf_joint1': rospy.Publisher('/puppy/joint2_position_controller/command', Float64, queue_size=1),
                'lf_joint2': rospy.Publisher('/puppy/joint6_position_controller/command', Float64, queue_size=1),
                'rf_joint1': rospy.Publisher('/puppy/joint1_position_controller/command', Float64, queue_size=1),
                'rf_joint2': rospy.Publisher('/puppy/joint5_position_controller/command', Float64, queue_size=1),
                'lb_joint1': rospy.Publisher('/puppy/joint4_position_controller/command', Float64, queue_size=1),
                'lb_joint2': rospy.Publisher('/puppy/joint8_position_controller/command', Float64, queue_size=1),
                'rb_joint1': rospy.Publisher('/puppy/joint3_position_controller/command', Float64, queue_size=1),
                'rb_joint2': rospy.Publisher('/puppy/joint7_position_controller/command', Float64, queue_size=1)
            }
    
    def calculate_standing_position(self):
        """Calculate the standing position for all joints"""
        positions = {}
        
        # Base positions from pose parameters - adjusted for stability
        base_lift = -0.25 - (self.pose_params['height'] / 100.0)  # Reduced lift angle
        base_forward = 0.5 + (self.pose_params['x_shift'] / 100.0)  # Adjusted forward position
        stance_x_adj = self.pose_params['stance_x'] / 100.0
        stance_y_adj = self.pose_params['stance_y'] / 100.0
        
        # Calculate positions for each leg with wider stance
        # Front legs
        positions['lf_joint1'] = base_lift + self.pose_params['pitch'] - stance_y_adj
        positions['lf_joint2'] = base_forward + stance_x_adj
        positions['rf_joint1'] = base_lift + self.pose_params['pitch'] + stance_y_adj
        positions['rf_joint2'] = base_forward + stance_x_adj
        
        # Back legs
        positions['lb_joint1'] = base_lift - self.pose_params['pitch'] - stance_y_adj
        positions['lb_joint2'] = base_forward - stance_x_adj
        positions['rb_joint1'] = base_lift - self.pose_params['pitch'] + stance_y_adj
        positions['rb_joint2'] = base_forward - stance_x_adj
        
        return positions
    
    def joint_states_callback(self, msg):
        """Store joint state feedback"""
        self.current_joint_states = msg
    
    def publish_joint_positions(self, positions):
        """Publish positions to all joints"""
        for joint, position in positions.items():
            if joint in self.joint_pubs:
                self.joint_pubs[joint].publish(float(position))
    
    def smooth_stand_up(self, steps=100, rate_hz=10):  # Increased steps, reduced rate
        """
        Smoothly transition from current position to standing position
        Args:
            steps: number of intermediate steps (increased for smoother motion)
            rate_hz: control rate in Hz (reduced for more stability)
        """
        print("Starting stand up sequence...")
        print("Press Ctrl+C to stop")
        
        # Calculate target standing position
        target_positions = self.calculate_standing_position()
        current_positions = {joint: 0.0 for joint in target_positions.keys()}
        
        # Create a ROS rate controller
        rate = rospy.Rate(rate_hz)
        
        # Smooth transition to standing position using cosine interpolation
        for step in range(steps):
            # Calculate smooth progress (cosine curve for even smoother acceleration/deceleration)
            progress = step / float(steps)
            smooth_progress = (1 - math.cos(progress * math.pi)) / 2
            
            # Calculate intermediate positions
            for joint in target_positions.keys():
                target = target_positions[joint]
                current_positions[joint] = target * smooth_progress
                
            # Publish positions
            self.publish_joint_positions(current_positions)
            rate.sleep()
        
        print("Standing position reached")
        
        # Hold the standing position with regular updates
        while not rospy.is_shutdown():
            self.publish_joint_positions(target_positions)
            rate.sleep()
    
    def cleanup(self):
        """Clean up on shutdown - gradually return to rest position"""
        print("Shutting down... Returning to rest position")
        # Get current positions
        if self.current_joint_states:
            current_pos = dict(zip(self.current_joint_states.name, 
                                 self.current_joint_states.position))
        else:
            current_pos = {joint: 0.0 for joint in self.joint_pubs.keys()}
        
        # Gradually move to zero
        steps = 50
        rate = rospy.Rate(10)
        for step in range(steps):
            progress = (steps - step) / float(steps)
            for joint in self.joint_pubs.keys():
                pos = current_pos.get(joint, 0.0) * progress
                self.joint_pubs[joint].publish(float(pos))
            rate.sleep()
        
        # Ensure final zero position
        for pub in self.joint_pubs.values():
            pub.publish(0.0)

def main():
    try:
        # Create controller in simulation mode
        controller = PuppyController(sim_mode=True)
        
        # Wait for publishers to connect
        rospy.sleep(2.0)  # Increased wait time for better initialization
        
        # Make the robot stand up
        controller.smooth_stand_up()
        
    except rospy.ROSInterruptException:
        pass
    except Exception as e:
        rospy.logerr(f"Error: {e}")

if __name__ == '__main__':
    main()