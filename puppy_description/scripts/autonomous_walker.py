#!/usr/bin/env python3
import rospy
from std_msgs.msg import Float64
from geometry_msgs.msg import PoseStamped
from sensor_msgs.msg import JointState
from gazebo_msgs.msg import ModelStates
import time
import math
import numpy as np
import datetime
import signal
import sys
from leg_ik import LegIK
import argparse

class AutonomousWalker:
    def __init__(self):
        # Generate a unique ID based on timestamp for logging
        self.unique_id = str(int(time.time()) % 10000)
        
        rospy.init_node(f'autonomous_walker_{self.unique_id}', anonymous=True)
        
        rospy.loginfo(f"Starting autonomous walker [{self.unique_id}] with optimized gait parameters...")
        
        # Set control rate
        self.rate = rospy.Rate(40)  # Increased rate for smoother motion (from 20 to 40Hz)
        
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
        
        # Create inverse kinematics helper
        try:
            from puppy_ik import PuppyIK
            self.ik = PuppyIK()
        except ImportError:
            rospy.logerr("Could not import PuppyIK. Using simple joint angle control instead.")
            self.ik = None
        
        # Performance monitoring parameters
        self.TARGET_SPEED = 0.15  # Increased target speed from 0.12 to 0.15 m/s
        self.MIN_PROGRESS_INTERVAL = 3.0  # Check progress every 3 seconds
        self.MIN_DISTANCE_PROGRESS = 0.08  # Expect at least 8cm progress every check interval
        self.stability_threshold = 0.75  # Stability score threshold
        self.stability_window_size = 10  # Size of stability history window
        self.auto_recovery = True  # Enable auto-recovery when stability is low

        # Walking parameters - fine-tuned for stability and effective forward movement
        self.STAND_HEIGHT = 0.12  # Height from ground to body
        self.STAND_WIDTH = 0.05   # Width between legs
        self.STAND_LENGTH = 0.07  # Length offset for standing position
        self.STEP_HEIGHT = 0.05   # Increased height for leg lifting (from 0.04 to 0.05)
        self.STEP_LENGTH = 0.05   # Length of forward step (increased from 0.04 to 0.05)
        
        # Timing parameters - adjusted for smoother coordination
        self.PHASE_1_TIME = 0.10  # Time for lifting leg
        self.PHASE_2_TIME = 0.08  # Time for moving leg forward
        self.PHASE_3_TIME = 0.10  # Time for lowering leg
        self.PHASE_4_TIME = 0.08  # Time for pushing back
        
        # Transition steps for smoother motion
        self.TRANSITION_STEPS = 10  # Increased from 8 to 10 for smoother transitions
        
        # State tracking
        self.joint_positions = {}
        self.initial_position = None
        self.current_position = None
        self.initial_orientation = None
        self.current_orientation = None
        self.distance_traveled = 0.0
        self.lateral_drift = 0.0
        self.direction_angle = 0.0
        self.target_distance = float('inf')  # Walk continuously
        self.max_walk_time = float('inf')    # Walk indefinitely
        
        # Performance metrics
        self.cycle_start_time = None
        self.start_time = None
        self.last_cycle_distance = 0.0
        self.cycle_speeds = []
        self.cycle_drifts = []
        self.cycle_angles = []
        self.stability_window = []
        
        # Register shutdown handler
        import signal
        signal.signal(signal.SIGINT, self.signal_handler)
        
        # Log initial parameters
        rospy.loginfo(f"\n=== Walker [{self.unique_id}] Parameters ===")
        rospy.loginfo(f"Standing Height: {self.STAND_HEIGHT:.3f}m")
        rospy.loginfo(f"Standing Width: {self.STAND_WIDTH:.3f}m")
        rospy.loginfo(f"Standing Length: {self.STAND_LENGTH:.3f}m")
        rospy.loginfo(f"Step Height: {self.STEP_HEIGHT:.3f}m")
        rospy.loginfo(f"Step Length: {self.STEP_LENGTH:.3f}m")
        rospy.loginfo(f"Phase Timings: P1={self.PHASE_1_TIME:.2f}s, P2={self.PHASE_2_TIME:.2f}s, P3={self.PHASE_3_TIME:.2f}s, P4={self.PHASE_4_TIME:.2f}s")
        rospy.loginfo(f"Transition Steps: {self.TRANSITION_STEPS}")
        
        # Wait for subscribers to initialize
        rospy.loginfo(f"\nWaiting for model state updates...")
        start_time = rospy.Time.now()
        while self.current_position is None and not rospy.is_shutdown():
            if (rospy.Time.now() - start_time).to_sec() > 5.0:
                rospy.logwarn("Timeout waiting for model state. Check if Gazebo is running.")
                break
            rospy.sleep(0.1)
        
        if self.current_position:
            rospy.loginfo(f"Robot position initialized at: x={self.current_position.x:.3f}, y={self.current_position.y:.3f}")
    
    def signal_handler(self, sig, frame):
        """Handle ctrl+c to ensure clean shutdown"""
        rospy.loginfo("\nShutdown requested. Stopping walker and returning to stand position...")
        self.stand()
        sys.exit(0)
    
    def stability_score(self):
        """Calculate a stability score based on recent motion metrics"""
        if len(self.stability_window) < 5:
            return 1.0  # Assume stable at start
            
        # Calculate stability based on angular drift and lateral drift
        angle_stability = 1.0 - min(1.0, abs(self.direction_angle) / 25.0)
        lateral_stability = 1.0 - min(1.0, self.lateral_drift / 0.3)
        
        # Weight the stability factors
        stability = 0.6 * angle_stability + 0.4 * lateral_stability
        
        return stability
        
    def update_stability_window(self):
        """Update the stability tracking window"""
        stability = self.stability_score()
        
        self.stability_window.append(stability)
        if len(self.stability_window) > self.stability_window_size:
            self.stability_window.pop(0)
            
        avg_stability = sum(self.stability_window) / len(self.stability_window)
        
        # Log stability periodically
        curr_time = rospy.get_time()
        if int(curr_time * 0.5) != int((curr_time - 0.1) * 0.5):
            rospy.loginfo(f"Current stability: {stability:.2f}, Average: {avg_stability:.2f}")
            
        return avg_stability >= self.stability_threshold
    
    def calculate_leg_positions(self, phase, leg):
        """Calculate target foot positions for each leg based on walking phase"""
        if phase == "stand":
            # Standing position
            if leg in ['rf', 'rb']:  # Right side
                x = self.STAND_LENGTH if leg == 'rf' else -self.STAND_LENGTH
                y = -self.STAND_WIDTH
            else:  # Left side
                x = self.STAND_LENGTH if leg == 'lf' else -self.STAND_LENGTH
                y = self.STAND_WIDTH
            z = -self.STAND_HEIGHT
            
        elif phase == "lift":
            # Lift phase - move foot up and slightly forward
            if leg in ['rf', 'rb']:  # Right side
                x = self.STAND_LENGTH * 1.2 if leg == 'rf' else -self.STAND_LENGTH * 0.9
                y = -self.STAND_WIDTH
            else:  # Left side
                x = self.STAND_LENGTH * 1.2 if leg == 'lf' else -self.STAND_LENGTH * 0.9
                y = self.STAND_WIDTH
            z = -self.STAND_HEIGHT + self.STEP_HEIGHT
            
        elif phase == "forward":
            # Forward phase - move foot forward
            if leg in ['rf', 'rb']:  # Right side
                x = (self.STAND_LENGTH + self.STEP_LENGTH * 1.2) if leg == 'rf' else -(self.STAND_LENGTH * 0.8)
                y = -self.STAND_WIDTH
            else:  # Left side
                x = (self.STAND_LENGTH + self.STEP_LENGTH * 1.2) if leg == 'lf' else -(self.STAND_LENGTH * 0.8)
                y = self.STAND_WIDTH
            z = -self.STAND_HEIGHT + self.STEP_HEIGHT * 0.8  # Slightly lower to prepare for touchdown
            
        elif phase == "lower":
            # Lower phase - move foot down
            if leg in ['rf', 'rb']:  # Right side
                x = (self.STAND_LENGTH + self.STEP_LENGTH) if leg == 'rf' else -self.STAND_LENGTH
                y = -self.STAND_WIDTH
            else:  # Left side
                x = (self.STAND_LENGTH + self.STEP_LENGTH) if leg == 'lf' else -self.STAND_LENGTH
                y = self.STAND_WIDTH
            z = -self.STAND_HEIGHT
            
        else:  # push phase
            # Push phase - move foot back while maintaining downward pressure
            if leg in ['rf', 'rb']:  # Right side
                x = self.STAND_LENGTH * 0.9 if leg == 'rf' else -self.STAND_LENGTH * 1.1
                y = -self.STAND_WIDTH
            else:  # Left side
                x = self.STAND_LENGTH * 0.9 if leg == 'lf' else -self.STAND_LENGTH * 1.1
                y = self.STAND_WIDTH
            z = -self.STAND_HEIGHT - 0.005  # Slight downward pressure during push phase
            
        return x, y, z
        
    def set_leg_position(self, leg_name, phase, transition_time=None):
        """Set a single leg's position using IK with smooth transition"""
        # Auto-adjust transition time based on phase
        if transition_time is None:
            if phase == 'lift':
                transition_time = self.PHASE_1_TIME
            elif phase == 'forward':
                transition_time = self.PHASE_2_TIME
            elif phase == 'lower':
                transition_time = self.PHASE_3_TIME
            elif phase == 'push':
                transition_time = self.PHASE_4_TIME
            else:
                transition_time = 0.08  # Default

        # Calculate target foot position
        x, y, z = self.calculate_leg_positions(phase, leg_name)
        
        # Calculate target joint angles using IK
        hip_angle, knee_angle = self.ik.calculate_angles(x, y, z)
        if hip_angle is None or knee_angle is None:
            rospy.logwarn(f"Warning: Could not calculate angles for {leg_name} in phase {phase}")
            return
            
        # Get current positions
        current_hip = self.joint_positions.get(f'{leg_name}_joint1', 0.0)
        current_knee = self.joint_positions.get(f'{leg_name}_joint2', 0.0)
        
        # Calculate intermediate positions with smooth acceleration
        for step in range(self.TRANSITION_STEPS):
            t = (step + 1) / self.TRANSITION_STEPS
            
            # Use improved easing function for smoother motion
            # Combination of sine easing and cubic easing for natural movement
            t = 0.5 - 0.5 * math.cos(t * math.pi)  # Sine easing
            t = t * t * (3 - 2 * t)  # Additional cubic smoothing
            
            intermediate_hip = current_hip + (hip_angle - current_hip) * t
            intermediate_knee = current_knee + (knee_angle - current_knee) * t
            
            # Publish joint positions
            self.joint_pubs[f'{leg_name}_joint1'].publish(intermediate_hip)
            self.joint_pubs[f'{leg_name}_joint2'].publish(intermediate_knee)
            
            # Sleep for the appropriate amount of time
            rospy.sleep(transition_time / self.TRANSITION_STEPS)
        
        # Final position to ensure exact target
        self.joint_pubs[f'{leg_name}_joint1'].publish(hip_angle)
        self.joint_pubs[f'{leg_name}_joint2'].publish(knee_angle)
        
    def walk_cycle(self, num_cycles=None):
        """Execute an optimized walking cycle with improved stability control"""
        try:
            self.start_time = rospy.Time.now()
            cycle_count = 0
            max_cycles = float('inf') if num_cycles is None else num_cycles
            last_progress_check = self.start_time
            last_distance = 0.0
            
            # Reset position tracking
            if self.initial_position is None:
                rospy.logwarn("Initial position not set, waiting...")
                timeout = rospy.Duration(5.0)
                start_wait = rospy.Time.now()
                while self.initial_position is None and not rospy.is_shutdown():
                    if (rospy.Time.now() - start_wait) > timeout:
                        rospy.logwarn("Timeout waiting for initial position")
                        return False
                    rospy.sleep(0.1)
            
            self.distance_traveled = 0.0
            self.lateral_drift = 0.0
            self.direction_angle = 0.0
            self.cycle_speeds = []
            self.cycle_drifts = []
            self.cycle_angles = []
            self.stability_window = []
            
            # First stand in stable position
            self.stand()
            rospy.loginfo(f"Starting autonomous walking... [{self.unique_id}]")
                
            while not rospy.is_shutdown() and cycle_count < max_cycles:
                current_time = rospy.Time.now()
                
                # Check if we've exceeded the maximum walk time
                elapsed_time = (current_time - self.start_time).to_sec()
                if self.max_walk_time != float('inf') and elapsed_time >= self.max_walk_time:
                    rospy.loginfo(f"Maximum walk time of {self.max_walk_time:.1f}s reached. Stopping.")
                    break
                
                # Check if we've reached the target distance
                if self.target_distance != float('inf') and self.distance_traveled >= self.target_distance:
                    rospy.loginfo(f"Target distance of {self.target_distance:.2f}m reached. Stopping.")
                    break
                
                # Start new cycle
                self.cycle_start_time = current_time
                self.last_cycle_distance = self.distance_traveled
                
                # Check stability periodically
                is_stable = self.update_stability_window()
                if not is_stable and self.auto_recovery and cycle_count > 10:
                    rospy.logwarn(f"Instability detected - performing recovery sequence")
                    self.recovery_sequence()
                
                # Check progress periodically
                if (current_time - last_progress_check).to_sec() >= self.MIN_PROGRESS_INTERVAL:
                    # Check if we're making forward progress
                    progress = self.distance_traveled - last_distance
                    
                    # Log detailed performance metrics
                    rospy.loginfo(f"\n=== Performance Update [{self.unique_id}] ===")
                    rospy.loginfo(f"Progress: {progress:.3f}m over {self.MIN_PROGRESS_INTERVAL:.1f}s")
                    rospy.loginfo(f"Total distance: {self.distance_traveled:.3f}m")
                    rospy.loginfo(f"Speed: {progress/self.MIN_PROGRESS_INTERVAL:.3f}m/s")
                    rospy.loginfo(f"Drift: {self.lateral_drift:.3f}m")
                    rospy.loginfo(f"Angle: {self.direction_angle:.1f}°")
                    rospy.loginfo(f"Time elapsed: {elapsed_time:.1f}s / {self.max_walk_time if self.max_walk_time != float('inf') else 'inf'}s")
                    rospy.loginfo(f"Distance remaining: {self.target_distance - self.distance_traveled:.2f}m" if self.target_distance != float('inf') else "Distance: unlimited")
                    
                    if progress < self.MIN_DISTANCE_PROGRESS and cycle_count > 5:
                        rospy.logwarn(f"Low progress detected: {progress:.3f}m - adjusting gait parameters")
                        self.adjust_gait_parameters()
                    
                    last_distance = self.distance_traveled
                    last_progress_check = current_time
                
                # Log cycle start (less frequently to reduce noise)
                if cycle_count % 5 == 0:
                    rospy.loginfo(f"\n=== Cycle {cycle_count + 1} [{self.unique_id}] ===")
                    rospy.loginfo(f"Distance: {self.distance_traveled:.3f}m, Speed: {self.cycle_speeds[-1] if self.cycle_speeds else 0:.3f}m/s")
                    rospy.loginfo(f"Drift: {self.lateral_drift:.3f}m, Angle: {self.direction_angle:.1f}°")
                
                # ===== IMPROVED DIAGONAL GAIT PATTERN =====
                
                # First prepare all legs for better balance before movement
                # Set a pre-walk position for better weight distribution
                self.set_leg_position('rf', 'stand', 0.15)
                self.set_leg_position('lf', 'stand', 0.15)
                self.set_leg_position('rb', 'stand', 0.15)
                self.set_leg_position('lb', 'stand', 0.15)
                rospy.sleep(0.05)
                
                # Phase 1: First diagonal pair (LF+RB) lift and prepare
                self.set_leg_position('lf', 'lift', self.PHASE_1_TIME)
                self.set_leg_position('rb', 'lift', self.PHASE_1_TIME)
                # Slightly adjust other legs for better balance
                self.set_leg_position('rf', 'push', self.PHASE_1_TIME)
                self.set_leg_position('lb', 'push', self.PHASE_1_TIME)
                rospy.sleep(self.PHASE_1_TIME * 0.2)
                
                # Phase 2: First diagonal pair move forward
                self.set_leg_position('lf', 'forward', self.PHASE_2_TIME)
                self.set_leg_position('rb', 'forward', self.PHASE_2_TIME)
                rospy.sleep(self.PHASE_2_TIME * 0.2)
                
                # Phase 3: First diagonal pair lower to ground
                self.set_leg_position('lf', 'lower', self.PHASE_3_TIME)
                self.set_leg_position('rb', 'lower', self.PHASE_3_TIME)
                rospy.sleep(self.PHASE_3_TIME * 0.2)
                
                # Phase 4: First diagonal pair push while preparing second pair
                self.set_leg_position('lf', 'push', self.PHASE_4_TIME)
                self.set_leg_position('rb', 'push', self.PHASE_4_TIME)
                # Pre-adjust second pair to prepare for lift
                self.set_leg_position('rf', 'stand', self.PHASE_4_TIME)
                self.set_leg_position('lb', 'stand', self.PHASE_4_TIME)
                rospy.sleep(self.PHASE_4_TIME * 0.2)
                
                # Phase 5: Second diagonal pair (RF+LB) lift
                self.set_leg_position('rf', 'lift', self.PHASE_1_TIME)
                self.set_leg_position('lb', 'lift', self.PHASE_1_TIME)
                # Maintain pressure on first pair for stability
                self.set_leg_position('lf', 'push', self.PHASE_1_TIME)
                self.set_leg_position('rb', 'push', self.PHASE_1_TIME)
                rospy.sleep(self.PHASE_1_TIME * 0.2)
                
                # Phase 6: Second diagonal pair move forward
                self.set_leg_position('rf', 'forward', self.PHASE_2_TIME)
                self.set_leg_position('lb', 'forward', self.PHASE_2_TIME)
                rospy.sleep(self.PHASE_2_TIME * 0.2)
                
                # Phase 7: Second diagonal pair lower
                self.set_leg_position('rf', 'lower', self.PHASE_3_TIME)
                self.set_leg_position('lb', 'lower', self.PHASE_3_TIME)
                rospy.sleep(self.PHASE_3_TIME * 0.2)
                
                # Phase 8: Second diagonal pair push
                self.set_leg_position('rf', 'push', self.PHASE_4_TIME)
                self.set_leg_position('lb', 'push', self.PHASE_4_TIME)
                # Return first pair to neutral for next cycle
                self.set_leg_position('lf', 'stand', self.PHASE_4_TIME)
                self.set_leg_position('rb', 'stand', self.PHASE_4_TIME)
                rospy.sleep(self.PHASE_4_TIME * 0.2)
                
                # Calculate cycle metrics
                cycle_time = (rospy.Time.now() - self.cycle_start_time).to_sec()
                cycle_distance = self.distance_traveled - self.last_cycle_distance
                cycle_speed = cycle_distance / cycle_time if cycle_time > 0 else 0
                
                # Track cycle metrics
                self.cycle_speeds.append(cycle_speed)
                self.cycle_drifts.append(self.lateral_drift)
                self.cycle_angles.append(abs(self.direction_angle))
                
                # Report full stats periodically
                if cycle_count % 20 == 0 and cycle_count > 0:
                    avg_speed = sum(self.cycle_speeds[-20:]) / min(20, len(self.cycle_speeds))
                    avg_drift = sum(self.cycle_drifts[-20:]) / min(20, len(self.cycle_drifts))
                    avg_angle = sum(self.cycle_angles[-20:]) / min(20, len(self.cycle_angles))
                    
                    elapsed_time = (rospy.Time.now() - self.start_time).to_sec()
                    rospy.loginfo(f"\n=== Performance Summary [{self.unique_id}] ===")
                    rospy.loginfo(f"Total Distance: {self.distance_traveled:.3f}m in {elapsed_time:.1f}s")
                    rospy.loginfo(f"Average Speed: {avg_speed:.3f}m/s")
                    rospy.loginfo(f"Average Drift: {avg_drift:.3f}m")
                    rospy.loginfo(f"Average Angle: {avg_angle:.1f}°")
                    
                cycle_count += 1
                self.rate.sleep()
            
            # Return to standing position
            self.stand()
            return True
            
        except rospy.ROSInterruptException:
            rospy.loginfo("Walk cycle interrupted")
            self.stand()
            return False
    
    def recovery_sequence(self):
        """Perform a recovery sequence when stability issues are detected"""
        rospy.logwarn("\nExecuting recovery sequence...")
        
        # First go to a stable standing position
        self.stand()
        rospy.sleep(0.5)
        
        # Shift weight slightly to reset stability
        for leg in ['rf', 'lf', 'rb', 'lb']:
            x, y, z = self.calculate_leg_positions('stand', leg)
            # Adjust height slightly for weight shift
            z += 0.01  
            
            hip_angle, knee_angle = self.ik.calculate_angles(x, y, z)
            if hip_angle and knee_angle:
                self.joint_pubs[f'{leg}_joint1'].publish(hip_angle)
                self.joint_pubs[f'{leg}_joint2'].publish(knee_angle)
                
        rospy.sleep(0.5)
        
        # Return to standing position
        self.stand()
        rospy.sleep(0.5)
        
        # Reset stability window
        self.stability_window = []
        
        rospy.loginfo("Recovery sequence completed")
    
    def adjust_gait_parameters(self):
        """Adjust gait parameters based on performance metrics"""
        
        # Calculate average metrics
        recent_speeds = self.cycle_speeds[-5:] if len(self.cycle_speeds) >= 5 else self.cycle_speeds
        recent_drifts = self.cycle_drifts[-5:] if len(self.cycle_drifts) >= 5 else self.cycle_drifts
        recent_angles = self.cycle_angles[-5:] if len(self.cycle_angles) >= 5 else self.cycle_angles
        
        avg_speed = sum(recent_speeds) / len(recent_speeds) if recent_speeds else 0
        avg_drift = sum(recent_drifts) / len(recent_drifts) if recent_drifts else 0
        avg_angle = sum(recent_angles) / len(recent_angles) if recent_angles else 0
        
        rospy.loginfo(f"Adjusting gait parameters - Current metrics:")
        rospy.loginfo(f"Speed: {avg_speed:.3f}m/s, Drift: {avg_drift:.3f}m, Angle: {avg_angle:.1f}°")
        
        # Check which parameter needs adjustment most
        if avg_speed < self.TARGET_SPEED * 0.7:
            # Robot is moving too slowly - increase step length and reduce phase times
            self.STEP_LENGTH = min(self.STEP_LENGTH * 1.15, 0.06)  # Max 6cm step
            self.PHASE_1_TIME *= 0.9  # Reduce phase times by 10%
            self.PHASE_2_TIME *= 0.9
            self.PHASE_3_TIME *= 0.9
            self.PHASE_4_TIME *= 0.9
            rospy.loginfo(f"Speed too low - Increasing step length to {self.STEP_LENGTH:.3f}m and reducing phase times")
            
        elif avg_angle > 10.0 or avg_drift > 0.1:
            # Robot is drifting or turning - adjust step parameters to compensate
            # Check drift direction from angle
            if self.direction_angle > 5.0:  # Drifting right
                self.STAND_WIDTH *= 0.95  # Reduce stance width
                rospy.loginfo(f"Drifting right - Reducing stance width to {self.STAND_WIDTH:.3f}m")
            elif self.direction_angle < -5.0:  # Drifting left
                self.STAND_WIDTH *= 1.05  # Increase stance width
                rospy.loginfo(f"Drifting left - Increasing stance width to {self.STAND_WIDTH:.3f}m")
            else:  # Just reduce drift by increasing downward pressure
                self.STAND_HEIGHT *= 0.95  # Lower stance height for more stability
                rospy.loginfo(f"Excessive drift - Lowering stance height to {self.STAND_HEIGHT:.3f}m")
                
        elif len(self.stability_window) > 5 and sum(self.stability_window[-5:]) / 5 < 0.8:
            # Stability is low - focus on a more conservative gait
            self.STEP_HEIGHT *= 0.9  # Lower step height
            self.PHASE_1_TIME *= 1.1  # Increase phase times by 10% for more careful stepping
            self.PHASE_3_TIME *= 1.1
            rospy.loginfo(f"Low stability - Reducing step height to {self.STEP_HEIGHT:.3f}m and increasing phase times")
        
        else:
            # Fine-tune for optimal speed if everything else looks good
            if avg_speed < self.TARGET_SPEED * 0.9:
                # Slightly increase step length
                self.STEP_LENGTH = min(self.STEP_LENGTH * 1.05, 0.06)
                rospy.loginfo(f"Fine-tuning - Increasing step length to {self.STEP_LENGTH:.3f}m")
            elif avg_speed > self.TARGET_SPEED * 1.1:
                # Slightly decrease step length for more control
                self.STEP_LENGTH *= 0.95
                rospy.loginfo(f"Fine-tuning - Decreasing step length to {self.STEP_LENGTH:.3f}m")
                
        # Apply safety bounds to all parameters
        self.STEP_LENGTH = max(0.03, min(self.STEP_LENGTH, 0.06))
        self.STEP_HEIGHT = max(0.03, min(self.STEP_HEIGHT, 0.06))
        self.STAND_HEIGHT = max(0.10, min(self.STAND_HEIGHT, 0.15))
        self.STAND_WIDTH = max(0.04, min(self.STAND_WIDTH, 0.06))
        self.PHASE_1_TIME = max(0.05, min(self.PHASE_1_TIME, 0.15))
        self.PHASE_2_TIME = max(0.05, min(self.PHASE_2_TIME, 0.15))
        self.PHASE_3_TIME = max(0.05, min(self.PHASE_3_TIME, 0.15))
        self.PHASE_4_TIME = max(0.05, min(self.PHASE_4_TIME, 0.15))
        
        rospy.loginfo("Gait parameters adjusted and applied")
    
    def stand(self):
        """Put the robot in a standing position using IK"""
        rospy.loginfo("Setting standing position...")
        
        # Move all legs to standing position with smooth transition
        for leg in ['rf', 'lf', 'rb', 'lb']:
            self.set_leg_position(leg, 'stand', transition_time=0.5)
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
                    rospy.loginfo(f"\nInitial position set: x={pose.position.x:.3f}, y={pose.position.y:.3f}, z={pose.position.z:.3f}")
                else:
                    # Calculate distance traveled along x-axis (forward)
                    dx = pose.position.x - self.initial_position.x
                    dy = pose.position.y - self.initial_position.y
                    self.distance_traveled = math.sqrt(dx*dx + dy*dy)
                    
                    # Calculate lateral drift (absolute y displacement)
                    self.lateral_drift = abs(dy)
                    
                    # Calculate direction angle in degrees from x-axis
                    self.direction_angle = math.degrees(math.atan2(dy, dx)) if dx != 0 else 0
                    
                    # Calculate current speed if we have a cycle start time
                    if self.cycle_start_time is not None:
                        elapsed_time = (rospy.Time.now() - self.cycle_start_time).to_sec()
                        if elapsed_time > 0:
                            current_speed = (self.distance_traveled - self.last_cycle_distance) / elapsed_time
                            self.cycle_speeds.append(current_speed)
                    
        except ValueError:
            # Model not found
            pass
        except Exception as e:
            rospy.logerr(f"Error in model_states_callback: {e}")

if __name__ == '__main__':
    try:
        # Parse command line arguments
        parser = argparse.ArgumentParser(description='Run the autonomous walker for PuppyPi robot')
        parser.add_argument('--distance', type=float, help='Target distance to walk in meters (default: infinite)')
        parser.add_argument('--time', type=float, help='Maximum time to walk in seconds (default: infinite)')
        parser.add_argument('--cycles', type=int, help='Number of walking cycles to perform (default: infinite)')
        args = parser.parse_args()
        
        rospy.loginfo("=== Starting Autonomous Walker ===")
        walker = AutonomousWalker()
        
        # Set parameters based on command line arguments
        if args.distance is not None:
            walker.target_distance = args.distance
            rospy.loginfo(f"Target distance set to: {args.distance} meters")
        
        if args.time is not None:
            walker.max_walk_time = args.time
            rospy.loginfo(f"Maximum walk time set to: {args.time} seconds")
        
        cycles = None
        if args.cycles is not None:
            cycles = args.cycles
            rospy.loginfo(f"Number of cycles set to: {args.cycles}")
        
        # Start continuous walking
        walker.walk_cycle(cycles)
        
        # Ensure we stand at the end
        walker.stand()
        
    except rospy.ROSInterruptException:
        pass