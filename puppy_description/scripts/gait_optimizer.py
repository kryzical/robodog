#!/usr/bin/env python3

import rospy
import math
import time
import subprocess
import signal
import os
import json
from std_msgs.msg import Float64
from geometry_msgs.msg import PoseStamped
from sensor_msgs.msg import JointState
from std_srvs.srv import Empty

class GaitOptimizer:
    def __init__(self):
        rospy.init_node('gait_optimizer', anonymous=True)
        rospy.loginfo("Starting Gait Optimizer...")
        
        # Control rate
        self.rate = rospy.Rate(10)  # 10Hz
        
        # Create joint publishers
        self.joint_pubs = {}
        self.joint_mapping = {
            'rf_joint1': 1,  # Right front hip
            'lf_joint1': 2,  # Left front hip
            'rb_joint1': 3,  # Right back hip
            'lb_joint1': 4,  # Left back hip
            'rf_joint2': 5,  # Right front knee
            'lf_joint2': 6,  # Left front knee
            'rb_joint2': 7,  # Right back knee
            'lb_joint2': 8   # Left back knee
        }
        
        for joint_name, controller_num in self.joint_mapping.items():
            pub = rospy.Publisher(f'/puppy/joint{controller_num}_position_controller/command', Float64, queue_size=1)
            self.joint_pubs[joint_name] = pub
        
        # Subscribers
        rospy.Subscriber('/joint_states', JointState, self.joint_states_callback)
        rospy.Subscriber('/puppy/pose', PoseStamped, self.pose_callback)
        
        # Wait for Gazebo services
        rospy.loginfo("Waiting for Gazebo services...")
        try:
            rospy.wait_for_service('/gazebo/reset_simulation', timeout=5)
            rospy.wait_for_service('/gazebo/reset_world', timeout=5)
            self.reset_simulation = rospy.ServiceProxy('/gazebo/reset_simulation', Empty)
            self.reset_world = rospy.ServiceProxy('/gazebo/reset_world', Empty)
        except rospy.ROSException:
            rospy.logerr("Failed to connect to Gazebo services. Is Gazebo running?")
            return
            
        # State variables
        self.joint_positions = {}
        self.current_pose = None
        self.initial_pose = None
        self.distance_traveled = 0.0
        self.start_time = None
        self.results = []
        self.current_config = None
        
        # Default gait parameters - will be modified during optimization
        self.base_params = {
            'STAND_HIP': 0.8,
            'STAND_KNEE': 0.0,
            'HIP_DELTA': 0.6,
            'KNEE_DELTA': 0.4,
            'PHASE_1_TIME': 0.3,
            'PHASE_2_TIME': 0.2,
            'PHASE_3_TIME': 0.3,
            'PHASE_4_TIME': 0.2,
            'TARGET_DISTANCE': 1.0
        }
        
        # Parameter variations for optimization
        self.parameter_variations = [
            {'HIP_DELTA': 0.4, 'KNEE_DELTA': 0.3},
            {'HIP_DELTA': 0.5, 'KNEE_DELTA': 0.3},
            {'HIP_DELTA': 0.6, 'KNEE_DELTA': 0.3},
            {'HIP_DELTA': 0.6, 'KNEE_DELTA': 0.4},
            {'HIP_DELTA': 0.7, 'KNEE_DELTA': 0.4},
            {'PHASE_1_TIME': 0.25, 'PHASE_3_TIME': 0.25},
            {'PHASE_1_TIME': 0.35, 'PHASE_3_TIME': 0.35},
            {'PHASE_2_TIME': 0.15, 'PHASE_4_TIME': 0.15},
            {'PHASE_2_TIME': 0.25, 'PHASE_4_TIME': 0.25}
        ]
        
        # Wait for subscribers to initialize
        rospy.sleep(1.0)
        
    def joint_states_callback(self, msg):
        # Create a mapping from joint name to position
        joint_name_to_pos = {}
        for i, name in enumerate(msg.name):
            joint_name_to_pos[name] = msg.position[i]
        
        # Map the joint positions to our internal representation
        reverse_joint_mapping = {
            'rf_joint1': 'puppy::rf_joint1',
            'lf_joint1': 'puppy::lf_joint1',
            'rb_joint1': 'puppy::rb_joint1',
            'lb_joint1': 'puppy::lb_joint1',
            'rf_joint2': 'puppy::rf_joint2',
            'lf_joint2': 'puppy::lf_joint2',
            'rb_joint2': 'puppy::rb_joint2',
            'lb_joint2': 'puppy::lb_joint2'
        }
        
        # Update our joint positions
        for our_name, gazebo_name in reverse_joint_mapping.items():
            if gazebo_name in joint_name_to_pos:
                self.joint_positions[our_name] = joint_name_to_pos[gazebo_name]
    
    def pose_callback(self, msg):
        self.current_pose = msg.pose
        
        # Calculate distance traveled if we have an initial pose
        if self.initial_pose is not None:
            dx = msg.pose.position.x - self.initial_pose.position.x
            dy = msg.pose.position.y - self.initial_pose.position.y
            self.distance_traveled = math.sqrt(dx*dx + dy*dy)
    
    def set_leg_position(self, leg_name, hip_pos, knee_pos):
        """Set a single leg's position"""
        self.joint_pubs[f'{leg_name}_joint1'].publish(hip_pos)
        self.joint_pubs[f'{leg_name}_joint2'].publish(knee_pos)
    
    def stand(self):
        """Put the robot in a standing position"""
        rospy.loginfo("Setting standing position...")
        
        # Get parameters from current config
        stand_hip = self.current_config['STAND_HIP']
        stand_knee = self.current_config['STAND_KNEE']
        
        for leg in ['rf', 'lf', 'rb', 'lb']:
            self.set_leg_position(leg, stand_hip, stand_knee)
        
        # Wait for robot to stabilize
        rospy.sleep(1.0)
    
    def verify_standing(self):
        """Verify that the robot is in the standing position"""
        # Get parameters from current config
        stand_hip = self.current_config['STAND_HIP']
        stand_knee = self.current_config['STAND_KNEE']
        
        # Check if all joints are close to the standing position
        for leg in ['rf', 'lf', 'rb', 'lb']:
            hip_joint = f'{leg}_joint1'
            knee_joint = f'{leg}_joint2'
            
            if hip_joint not in self.joint_positions or knee_joint not in self.joint_positions:
                rospy.logwarn(f"Joint {hip_joint} or {knee_joint} not found in joint positions")
                return False
            
            hip_error = abs(self.joint_positions[hip_joint] - stand_hip)
            knee_error = abs(self.joint_positions[knee_joint] - stand_knee)
            
            if hip_error > 0.1 or knee_error > 0.1:
                rospy.logwarn(f"Joint {hip_joint} or {knee_joint} not in standing position")
                return False
        
        return True
    
    def reset_simulation_state(self):
        """Reset the simulation to a clean state"""
        rospy.loginfo("Resetting simulation...")
        
        try:
            # Call reset services
            self.reset_simulation()
            rospy.sleep(0.5)
            self.reset_world()
            rospy.sleep(0.5)
            
            # Reset state variables
            self.joint_positions = {}
            self.current_pose = None
            self.initial_pose = None
            self.distance_traveled = 0.0
            self.start_time = None
            
            # Wait for simulation to stabilize
            rospy.sleep(1.0)
            
            return True
        except rospy.ServiceException as e:
            rospy.logerr(f"Failed to reset simulation: {e}")
            return False
    
    def walk_cycle(self):
        """Execute one complete walk cycle with the current parameters"""
        # Extract parameters from current config
        stand_hip = self.current_config['STAND_HIP']
        stand_knee = self.current_config['STAND_KNEE']
        hip_delta = self.current_config['HIP_DELTA']
        knee_delta = self.current_config['KNEE_DELTA']
        phase_1_time = self.current_config['PHASE_1_TIME']
        phase_2_time = self.current_config['PHASE_2_TIME']
        phase_3_time = self.current_config['PHASE_3_TIME']
        phase_4_time = self.current_config['PHASE_4_TIME']
        target_distance = self.current_config['TARGET_DISTANCE']
        
        # Reset tracking variables
        self.initial_pose = self.current_pose
        self.distance_traveled = 0.0
        self.start_time = rospy.Time.now()
        
        # Start walking cycle
        rospy.loginfo("Starting walk cycle with parameters:")
        for key, value in self.current_config.items():
            rospy.loginfo(f"  {key}: {value}")
        
        cycle_count = 0
        max_cycles = 20  # Prevent infinite loops
        
        try:
            while not rospy.is_shutdown() and cycle_count < max_cycles:
                # Phase 1: Left front and right back legs up and forward
                rospy.loginfo("Phase 1: LF + RB forward")
                self.set_leg_position('lf', stand_hip - hip_delta, stand_knee - knee_delta)
                self.set_leg_position('rb', stand_hip - hip_delta, stand_knee - knee_delta)
                self.set_leg_position('rf', stand_hip + hip_delta, stand_knee)
                self.set_leg_position('lb', stand_hip + hip_delta, stand_knee)
                rospy.sleep(phase_1_time)
                
                # Phase 2: Left front and right back legs down
                rospy.loginfo("Phase 2: LF + RB down")
                self.set_leg_position('lf', stand_hip - hip_delta, stand_knee + knee_delta)
                self.set_leg_position('rb', stand_hip - hip_delta, stand_knee + knee_delta)
                rospy.sleep(phase_2_time)
                
                # Phase 3: Right front and left back legs up and forward
                rospy.loginfo("Phase 3: RF + LB forward")
                self.set_leg_position('rf', stand_hip - hip_delta, stand_knee - knee_delta)
                self.set_leg_position('lb', stand_hip - hip_delta, stand_knee - knee_delta)
                self.set_leg_position('lf', stand_hip + hip_delta, stand_knee)
                self.set_leg_position('rb', stand_hip + hip_delta, stand_knee)
                rospy.sleep(phase_3_time)
                
                # Phase 4: Right front and left back legs down
                rospy.loginfo("Phase 4: RF + LB down")
                self.set_leg_position('rf', stand_hip - hip_delta, stand_knee + knee_delta)
                self.set_leg_position('lb', stand_hip - hip_delta, stand_knee + knee_delta)
                rospy.sleep(phase_4_time)
                
                # Log progress
                elapsed_time = (rospy.Time.now() - self.start_time).to_sec()
                rospy.loginfo(f"Distance: {self.distance_traveled:.2f}m, Time: {elapsed_time:.2f}s")
                
                # Check if we've reached target distance
                if self.distance_traveled >= target_distance:
                    rospy.loginfo(f"Reached target distance of {target_distance} meters")
                    break
                
                cycle_count += 1
                self.rate.sleep()
            
            # Return to standing position
            self.stand()
            
            # Calculate metrics
            elapsed_time = (rospy.Time.now() - self.start_time).to_sec()
            speed = self.distance_traveled / elapsed_time if elapsed_time > 0 else 0
            
            # Store results
            result = {
                'parameters': self.current_config.copy(),
                'distance': self.distance_traveled,
                'time': elapsed_time,
                'speed': speed,
                'cycles': cycle_count,
                'standing_verified': self.verify_standing()
            }
            
            self.results.append(result)
            
            rospy.loginfo(f"Test completed: Distance={self.distance_traveled:.2f}m, Time={elapsed_time:.2f}s, Speed={speed:.2f}m/s")
            
            return True
            
        except rospy.ROSInterruptException:
            rospy.loginfo("Walk cycle interrupted")
            return False
    
    def run_optimization(self):
        """Run the optimization process with different parameter sets"""
        rospy.loginfo("Starting gait optimization...")
        
        # Test each parameter variation
        for i, variation in enumerate(self.parameter_variations):
            rospy.loginfo(f"\n=== Testing parameter set {i+1}/{len(self.parameter_variations)} ===")
            
            # Create config by updating base params with current variation
            self.current_config = self.base_params.copy()
            self.current_config.update(variation)
            
            # Reset simulation
            if not self.reset_simulation_state():
                rospy.logerr("Failed to reset simulation, skipping parameter set")
                continue
            
            # Set initial standing position
            self.stand()
            
            # Run walk cycle
            self.walk_cycle()
            
            # Short pause between tests
            rospy.sleep(2.0)
        
        # Analyze and report results
        self.analyze_results()
    
    def analyze_results(self):
        """Analyze the optimization results and report the best parameters"""
        if not self.results:
            rospy.logwarn("No results to analyze")
            return
        
        # Sort results by speed (primary) and distance (secondary)
        sorted_results = sorted(self.results, key=lambda x: (x['speed'], x['distance']), reverse=True)
        
        # Print results
        rospy.loginfo("\n=== Gait Optimization Results ===")
        rospy.loginfo("Parameters ranked by speed:")
        
        for i, result in enumerate(sorted_results):
            params = result['parameters']
            rospy.loginfo(f"\n{i+1}. Speed: {result['speed']:.2f}m/s, Distance: {result['distance']:.2f}m, Time: {result['time']:.2f}s, Standing verified: {result['standing_verified']}")
            rospy.loginfo(f"   HIP_DELTA: {params['HIP_DELTA']}, KNEE_DELTA: {params['KNEE_DELTA']}")
            rospy.loginfo(f"   Phase times: {params['PHASE_1_TIME']}/{params['PHASE_2_TIME']}/{params['PHASE_3_TIME']}/{params['PHASE_4_TIME']}")
        
        # Save results to file
        self.save_results()
        
        # Return the best parameters
        best = sorted_results[0]
        rospy.loginfo("\n=== Best Parameters ===")
        rospy.loginfo(f"Speed: {best['speed']:.2f}m/s, Distance: {best['distance']:.2f}m")
        for key, value in best['parameters'].items():
            rospy.loginfo(f"{key}: {value}")
    
    def save_results(self):
        """Save the optimization results to a file"""
        try:
            # Create a results directory if it doesn't exist
            results_dir = os.path.join(os.path.dirname(__file__), '..', 'results')
            os.makedirs(results_dir, exist_ok=True)
            
            # Save results
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            filename = os.path.join(results_dir, f"gait_optimization_{timestamp}.json")
            
            with open(filename, 'w') as f:
                json.dump(self.results, f, indent=2)
            
            rospy.loginfo(f"Results saved to {filename}")
        except Exception as e:
            rospy.logerr(f"Failed to save results: {e}")

if __name__ == '__main__':
    try:
        optimizer = GaitOptimizer()
        optimizer.run_optimization()
        
    except rospy.ROSInterruptException:
        rospy.loginfo("Gait optimizer interrupted")
    except Exception as e:
        rospy.logerr(f"Error during gait optimization: {e}") 