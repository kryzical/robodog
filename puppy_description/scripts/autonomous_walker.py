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

class AutonomousWalker:
    def __init__(self):
        # Generate a unique ID based on timestamp for logging
        self.unique_id = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        rospy.init_node(f'autonomous_walker_{self.unique_id}', anonymous=True)
        
        rospy.loginfo(f"Starting autonomous walker [{self.unique_id}] with optimized gait parameters...")
        
        # Set control rate
        self.rate = rospy.Rate(60)  # Increased to 60Hz for even smoother motion
        
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
            
        # Subscribe to joint states for position verification
        rospy.Subscriber('/joint_states', JointState, self.joint_states_callback)
        
        # Subscribe to model states for position tracking
        rospy.Subscriber('/gazebo/model_states', ModelStates, self.model_states_callback)
        
        # Initialize IK solver
        self.ik = LegIK()
        
        # Setup signal handler for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        
        # Movement parameters - standing position (in meters) - fine-tuned for stability
        self.STAND_HEIGHT = 0.11  # Optimized height for stability
        self.STAND_WIDTH = 0.095  # Slightly narrower stance for better balance
        self.STAND_LENGTH = 0.115  # Optimized length for stability
        
        # Performance monitoring parameters
        self.MIN_SPEED = 0.06     # Lower minimum acceptable speed
        self.MAX_SPEED = 0.22     # Reasonable maximum speed
        self.TARGET_SPEED = 0.12  # Target speed for stable walking
        self.SPEED_CHECK_INTERVAL = 1.5  # Check speed every 1.5 seconds
        self.MAX_TIME_PER_METER = 20.0  # More lenient time per meter
        self.MIN_PROGRESS_INTERVAL = 2.5  # Check progress every 2.5 seconds
        self.MIN_DISTANCE_PROGRESS = 0.04  # Minimum progress per interval
        
        # Walking parameters - fine-tuned for reliability
        self.STEP_HEIGHT = 0.025  # Lower step height for stability
        self.STEP_LENGTH = 0.05   # Shorter steps for reliability
        self.STEP_WIDTH = 0.095   # Match stand width for consistency
        
        # Phase timing - optimized for smooth transitions
        self.PHASE_1_TIME = 0.09  # Lift phase
        self.PHASE_2_TIME = 0.08  # Forward phase
        self.PHASE_3_TIME = 0.09  # Lower phase
        self.PHASE_4_TIME = 0.07  # Push phase
        
        # Transition steps for smoother movement
        self.TRANSITION_STEPS = 18  # More steps for smoother transitions
        
        # State tracking
        self.joint_positions = {}
        self.initial_position = None
        self.current_position = None
        self.distance_traveled = 0.0
        self.lateral_drift = 0.0
        self.direction_angle = 0.0
        self.target_distance = float('inf')  # Walk continuously
        self.max_walk_time = float('inf')    # Walk indefinitely
        self.auto_recovery = True            # Enable automatic recovery from issues
        
        # Stability tracking
        self.stability_window = []
        self.max_stability_window = 20
        self.stability_threshold = 0.7
        
        # Performance metrics
        self.cycle_start_time = None
        self.last_cycle_distance = 0.0
        self.cycle_speeds = []
        self.cycle_drifts = []
        self.cycle_angles = []
        self.joint_velocities = {}
        self.start_time = None
        
        # Log initial parameters
        rospy.loginfo(f"\n=== Walker [{self.unique_id}] Parameters ===")
        rospy.loginfo(f"Standing Height: {self.STAND_HEIGHT:.3f}m")
        rospy.loginfo(f"Standing Width: {self.STAND_WIDTH:.3f}m")
        rospy.loginfo(f"Standing Length: {self.STAND_LENGTH:.3f}m")
        rospy.loginfo(f"Step Height: {self.STEP_HEIGHT:.3f}m")
        rospy.loginfo(f"Step Length: {self.STEP_LENGTH:.3f}m")
        rospy.loginfo(f"Step Width: {self.STEP_WIDTH:.3f}m")
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
        if len(self.stability_window) > self.max_stability_window:
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
                x = self.STAND_LENGTH if leg == 'rf' else -self.STAND_LENGTH
                y = -self.STAND_WIDTH
            else:  # Left side
                x = self.STAND_LENGTH if leg == 'lf' else -self.STAND_LENGTH
                y = self.STAND_WIDTH
            z = -self.STAND_HEIGHT + self.STEP_HEIGHT
            
        elif phase == "forward":
            # Forward phase - move foot forward
            if leg in ['rf', 'rb']:  # Right side
                x = (self.STAND_LENGTH + self.STEP_LENGTH) if leg == 'rf' else -self.STAND_LENGTH
                y = -self.STAND_WIDTH
            else:  # Left side
                x = (self.STAND_LENGTH + self.STEP_LENGTH) if leg == 'lf' else -self.STAND_LENGTH
                y = self.STAND_WIDTH
            z = -self.STAND_HEIGHT + self.STEP_HEIGHT
            
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
            # Push phase - move foot back
            if leg in ['rf', 'rb']:  # Right side
                x = self.STAND_LENGTH if leg == 'rf' else -self.STAND_LENGTH
                y = -self.STAND_WIDTH
            else:  # Left side
                x = self.STAND_LENGTH if leg == 'lf' else -self.STAND_LENGTH
                y = self.STAND_WIDTH
            z = -self.STAND_HEIGHT
            
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
                
                # ===== OPTIMIZED DIAGONAL GAIT PATTERN =====
                
                # Phase 1: First diagonal pair (LF+RB) lift
                self.set_leg_position('lf', 'lift')
                self.set_leg_position('rb', 'lift')
                rospy.sleep(self.PHASE_1_TIME * 0.2)  # Reduced sleep for more responsive movement
                
                # Phase 2: First diagonal pair move forward
                self.set_leg_position('lf', 'forward')
                self.set_leg_position('rb', 'forward')
                rospy.sleep(self.PHASE_2_TIME * 0.2)
                
                # Phase 3: First diagonal pair lower
                self.set_leg_position('lf', 'lower')
                self.set_leg_position('rb', 'lower')
                rospy.sleep(self.PHASE_3_TIME * 0.2)
                
                # Phase 4: First diagonal pair push
                self.set_leg_position('lf', 'push')
                self.set_leg_position('rb', 'push')
                rospy.sleep(self.PHASE_4_TIME * 0.2)
                
                # Phase 5: Second diagonal pair (RF+LB) lift
                self.set_leg_position('rf', 'lift')
                self.set_leg_position('lb', 'lift')
                rospy.sleep(self.PHASE_1_TIME * 0.2)
                
                # Phase 6: Second diagonal pair move forward
                self.set_leg_position('rf', 'forward')
                self.set_leg_position('lb', 'forward')
                rospy.sleep(self.PHASE_2_TIME * 0.2)
                
                # Phase 7: Second diagonal pair lower
                self.set_leg_position('rf', 'lower')
                self.set_leg_position('lb', 'lower')
                rospy.sleep(self.PHASE_3_TIME * 0.2)
                
                # Phase 8: Second diagonal pair push
                self.set_leg_position('rf', 'push')
                self.set_leg_position('lb', 'push')
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
        """Dynamically adjust gait parameters based on performance"""
        rospy.loginfo("\nAdjusting gait parameters for better performance...")
        
        # Get recent performance metrics
        if len(self.cycle_speeds) >= 5:
            avg_speed = sum(self.cycle_speeds[-5:]) / 5
            avg_drift = sum(self.cycle_drifts[-5:]) / 5
            avg_angle = sum(self.cycle_angles[-5:]) / 5
            
            # Adjust step length based on speed
            if avg_speed < self.MIN_SPEED:
                self.STEP_LENGTH = min(0.07, self.STEP_LENGTH * 1.05)
                rospy.loginfo(f"Increasing step length to {self.STEP_LENGTH:.3f}m for better speed")
            
            # Adjust step height based on drift
            if avg_drift > 0.15:
                self.STEP_HEIGHT = max(0.02, self.STEP_HEIGHT * 0.95)
                rospy.loginfo(f"Decreasing step height to {self.STEP_HEIGHT:.3f}m for better stability")
            
            # Adjust phase timing based on direction angle
            if avg_angle > 10:
                # Slowdown phases for more stability
                self.PHASE_1_TIME *= 1.05
                self.PHASE_2_TIME *= 1.05
                self.PHASE_3_TIME *= 1.05
                self.PHASE_4_TIME *= 1.05
                rospy.loginfo(f"Slowing phase timing for better directional control")
            
        # Cap at reasonable values
        self.STEP_LENGTH = max(0.03, min(0.07, self.STEP_LENGTH))
        self.STEP_HEIGHT = max(0.02, min(0.04, self.STEP_HEIGHT))
        self.PHASE_1_TIME = max(0.06, min(0.12, self.PHASE_1_TIME))
        self.PHASE_2_TIME = max(0.05, min(0.10, self.PHASE_2_TIME))
        self.PHASE_3_TIME = max(0.06, min(0.12, self.PHASE_3_TIME))
        self.PHASE_4_TIME = max(0.05, min(0.10, self.PHASE_4_TIME))
            
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
        rospy.loginfo("=== Starting Autonomous Walker ===")
        walker = AutonomousWalker()
        
        # Start continuous walking
        walker.walk_cycle()
            
        # Return to standing position on shutdown
        walker.stand()
        
    except rospy.ROSInterruptException:
        pass
```