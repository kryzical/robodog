#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float64
from geometry_msgs.msg import PoseStamped
from sensor_msgs.msg import JointState
from gazebo_msgs.msg import ModelStates
import time
import math

class MovementTest:
    def __init__(self):
        rospy.init_node('movement_test', anonymous=True)
        rospy.loginfo("Starting refined walking test with improved stability monitoring and calibration...")
        
        # Set control rate
        self.rate = rospy.Rate(20)  # 20Hz rate for smooth motion
        
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
        
        # Subscribe to model states for position and orientation tracking
        rospy.Subscriber('/gazebo/model_states', ModelStates, self.model_states_callback)
        
        # Movement parameters - standing position
        self.STAND_HIP = 0.8   # Hip neutral position
        self.STAND_KNEE = 0.0  # Knee neutral position
        
        # Performance monitoring parameters
        self.MIN_SPEED = 0.1   # Minimum acceptable speed in m/s
        self.MAX_SPEED = 0.3   # Maximum target speed in m/s
        self.TARGET_SPEED = 0.2 # Target speed in m/s
        self.SPEED_CHECK_INTERVAL = 2.0  # How often to check speed (seconds)
        self.MAX_TIME_PER_METER = 10.0   # Maximum time allowed per meter of distance
        self.MIN_PROGRESS_INTERVAL = 5.0  # Minimum time between progress checks
        self.MIN_DISTANCE_PROGRESS = 0.1  # Minimum distance progress between checks (meters)
        self.LEG_MOVEMENT_TIMEOUT = 1.0   # Maximum time allowed for a leg to complete its movement
        self.LEG_POSITION_TOLERANCE = 0.05  # Tolerance for leg position verification
        self.MAX_TEST_DURATION = 30.0  # Maximum test duration in seconds
        self.TARGET_DISTANCE = 2.0  # Target distance in meters
        self.NATURAL_MOVEMENT_CHECK_INTERVAL = 1.0  # How often to check for natural movement
        self.MIN_LEG_MOVEMENT_RATIO = 0.7  # Minimum ratio of legs that should be moving at any time
        self.MIN_LEG_ANGLE_CHANGE = 0.1  # Minimum angle change required to consider a leg as moving
        
        # Stability monitoring parameters
        self.MAX_TILT_ANGLE = 15.0  # Maximum allowed tilt angle in degrees
        self.MAX_ROLL_ANGLE = 10.0  # Maximum allowed roll angle in degrees
        self.STABILITY_CHECK_INTERVAL = 0.5  # How often to check stability (seconds)
        self.ORIENTATION_HISTORY_SIZE = 10  # Number of orientation measurements to keep for trend analysis
        
        # Movement parameters - adjusted for much faster movement
        self.HIP_FORWARD = 0.65  # More aggressive forward position
        self.HIP_MID = 0.75      # Mid hip position
        self.HIP_BACK = 0.85     # Back hip position
        
        # Knee movement - adjusted for faster stride
        self.KNEE_UP = -0.55     # Higher lift for faster movement
        self.KNEE_MID = 0.0      # Neutral position
        self.KNEE_DOWN = 0.55    # More ground push
        
        # Phase timing - much faster movement
        self.PHASE_1_TIME = 0.03  # Faster lift
        self.PHASE_2_TIME = 0.02  # Faster forward swing
        self.PHASE_3_TIME = 0.03  # Faster ground contact
        self.PHASE_4_TIME = 0.02  # Faster push
        
        # Transition steps for quick movement
        self.TRANSITION_STEPS = 8  # Fewer steps for faster transitions
        
        # Fine-tuned values for opposite side legs
        self.LEFT_ADJUST = 0.01  # Minimal adjustment for speed
        
        # State tracking
        self.joint_positions = {}
        self.initial_position = None
        self.current_position = None
        self.initial_orientation = None
        self.current_orientation = None
        self.orientation_history = []
        self.distance_traveled = 0.0
        self.lateral_drift = 0.0
        self.direction_angle = 0.0
        self.max_walk_time = 180.0
        
        # Performance metrics
        self.cycle_start_time = None
        self.last_cycle_distance = 0.0
        self.cycle_speeds = []
        self.cycle_drifts = []
        self.cycle_angles = []
        self.stability_scores = []
        self.last_stability_check = None
        
        # Speed check parameters
        self.target_distance = 2.0  # Target distance in meters
        self.TARGET_DISTANCE = 2.0  # Target distance in meters (for compatibility)
        
        # Log initial parameters
        rospy.loginfo("\n=== Movement Parameters ===")
        rospy.loginfo(f"Hip Positions: Forward={self.HIP_FORWARD:.2f}, Mid={self.HIP_MID:.2f}, Back={self.HIP_BACK:.2f}")
        rospy.loginfo(f"Knee Positions: Up={self.KNEE_UP:.2f}, Mid={self.KNEE_MID:.2f}, Down={self.KNEE_DOWN:.2f}")
        rospy.loginfo(f"Phase Timings: P1={self.PHASE_1_TIME:.2f}s, P2={self.PHASE_2_TIME:.2f}s, P3={self.PHASE_3_TIME:.2f}s, P4={self.PHASE_4_TIME:.2f}s")
        rospy.loginfo(f"Left Side Adjustment: {self.LEFT_ADJUST:.2f}")
        rospy.loginfo(f"Target Distance: {self.target_distance:.1f}m")
        rospy.loginfo(f"Max Time: {self.max_walk_time:.1f}s")
        rospy.loginfo(f"Max Tilt Angle: {self.MAX_TILT_ANGLE:.1f}°")
        rospy.loginfo(f"Max Roll Angle: {self.MAX_ROLL_ANGLE:.1f}°")
        
        # Wait for subscribers to initialize
        rospy.loginfo("\nWaiting for model state updates...")
        start_time = rospy.Time.now()
        while self.current_position is None and not rospy.is_shutdown():
            if (rospy.Time.now() - start_time).to_sec() > 5.0:
                rospy.logwarn("Timeout waiting for model state. Check Gazebo is running.")
                break
            rospy.sleep(0.1)
        
        if self.current_position:
            rospy.loginfo(f"Robot position initialized at: x={self.current_position.x:.3f}, y={self.current_position.y:.3f}")
            
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
        """Track robot position and orientation using model states"""
        try:
            # Find the puppy model in the model_states message
            if 'puppy' in msg.name:
                idx = msg.name.index('puppy')
                pose = msg.pose[idx]
                
                # Update current position and orientation
                self.current_position = pose.position
                self.current_orientation = pose.orientation
                
                # Initialize start position and orientation if not set
                if self.initial_position is None:
                    self.initial_position = pose.position
                    self.initial_orientation = pose.orientation
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
                    
                    # Update orientation history
                    self.orientation_history.append(self.current_orientation)
                    if len(self.orientation_history) > self.ORIENTATION_HISTORY_SIZE:
                        self.orientation_history.pop(0)
                    
                    # Check stability periodically
                    current_time = rospy.Time.now()
                    if (self.last_stability_check is None or 
                        (current_time - self.last_stability_check).to_sec() >= self.STABILITY_CHECK_INTERVAL):
                        self.check_stability()
                        self.last_stability_check = current_time
                    
                    # Log detailed position and orientation every 0.5 seconds
                    curr_time = rospy.get_time()
                    if int(curr_time * 2) != int((curr_time - 0.1) * 2):
                        self.log_status()
                        
        except ValueError:
            # Model not found
            pass
        except Exception as e:
            rospy.logerr(f"Error in model_states_callback: {e}")
            
    def check_stability(self):
        """Check robot stability based on orientation"""
        if not self.current_orientation:
            return
            
        # Convert quaternion to Euler angles
        q = self.current_orientation
        # Roll (x-axis rotation)
        sinr_cosp = 2 * (q.w * q.x + q.y * q.z)
        cosr_cosp = 1 - 2 * (q.x * q.x + q.y * q.y)
        roll = math.degrees(math.atan2(sinr_cosp, cosr_cosp))
        
        # Pitch (y-axis rotation)
        sinp = 2 * (q.w * q.y - q.z * q.x)
        pitch = math.degrees(math.asin(sinp))
        
        # Calculate stability score (0-1, higher is better)
        roll_score = 1.0 - min(abs(roll) / self.MAX_ROLL_ANGLE, 1.0)
        pitch_score = 1.0 - min(abs(pitch) / self.MAX_TILT_ANGLE, 1.0)
        stability_score = (roll_score + pitch_score) / 2.0
        
        self.stability_scores.append(stability_score)
        if len(self.stability_scores) > 10:
            self.stability_scores.pop(0)
            
        # Log stability metrics
        rospy.loginfo(f"\n=== Stability Check ===")
        rospy.loginfo(f"Roll: {roll:.1f}° (max: {self.MAX_ROLL_ANGLE}°)")
        rospy.loginfo(f"Pitch: {pitch:.1f}° (max: {self.MAX_TILT_ANGLE}°)")
        rospy.loginfo(f"Stability Score: {stability_score:.2f}")
        
        # Check if stability is deteriorating
        if len(self.stability_scores) >= 3:
            recent_trend = sum(self.stability_scores[-3:]) / 3.0
            if recent_trend < 0.7:  # Warning threshold
                rospy.logwarn("Warning: Robot stability is deteriorating")
                return False
                
        return True
        
    def log_status(self):
        """Log detailed robot status"""
        rospy.loginfo(f"\n=== Robot Status ===")
        rospy.loginfo(f"Distance: {self.distance_traveled:.3f}m")
        rospy.loginfo(f"Position: x={self.current_position.x:.3f}, y={self.current_position.y:.3f}")
        rospy.loginfo(f"Drift: {self.lateral_drift:.3f}m")
        rospy.loginfo(f"Angle: {self.direction_angle:.1f}°")
        
        if self.cycle_speeds:
            avg_speed = sum(self.cycle_speeds[-5:]) / min(5, len(self.cycle_speeds))
            rospy.loginfo(f"Average Speed: {avg_speed:.3f}m/s")
            
        if self.stability_scores:
            avg_stability = sum(self.stability_scores) / len(self.stability_scores)
            rospy.loginfo(f"Average Stability: {avg_stability:.2f}")
            
        rospy.loginfo(f"Joint Positions:")
        for joint, pos in self.joint_positions.items():
            rospy.loginfo(f"  {joint}: {pos:.3f}")
            
    def check_leg_movement(self, leg_name, target_hip, target_knee):
        """Verify that a leg has moved to its target position within timeout"""
        start_time = rospy.Time.now()
        while not rospy.is_shutdown():
            current_time = rospy.Time.now()
            if (current_time - start_time).to_sec() > self.LEG_MOVEMENT_TIMEOUT:
                rospy.logwarn(f"Leg {leg_name} movement timeout - did not reach target position")
                return False
                
            current_hip = self.joint_positions.get(f'{leg_name}_joint1')
            current_knee = self.joint_positions.get(f'{leg_name}_joint2')
            
            if current_hip is not None and current_knee is not None:
                hip_diff = abs(current_hip - target_hip)
                knee_diff = abs(current_knee - target_knee)
                
                if hip_diff < self.LEG_POSITION_TOLERANCE and knee_diff < self.LEG_POSITION_TOLERANCE:
                    rospy.loginfo(f"Leg {leg_name} reached target position: hip={current_hip:.3f}, knee={current_knee:.3f}")
                    return True
                    
            rospy.sleep(0.1)
        return False

    def set_leg_position(self, leg_name, hip_pos, knee_pos, transition_time=0.08):
        """Set a single leg's position with smooth transition and movement verification"""
        # Apply left side adjustment to help robot walk straighter
        if leg_name.startswith('l'):  # Left legs
            hip_pos += self.LEFT_ADJUST
            
        # Get current positions
        current_hip = self.joint_positions.get(f'{leg_name}_joint1', self.STAND_HIP)
        current_knee = self.joint_positions.get(f'{leg_name}_joint2', self.STAND_KNEE)
        
        # Log movement start
        rospy.loginfo(f"\n=== Starting Leg Movement ===")
        rospy.loginfo(f"Leg: {leg_name}")
        rospy.loginfo(f"Current Position: hip={current_hip:.3f}, knee={current_knee:.3f}")
        rospy.loginfo(f"Target Position: hip={hip_pos:.3f}, knee={knee_pos:.3f}")
        
        # Calculate intermediate positions with smooth acceleration
        for step in range(self.TRANSITION_STEPS):
            t = (step + 1) / self.TRANSITION_STEPS
            # Use smooth acceleration curve with easing
            t = 0.5 - 0.5 * math.cos(t * math.pi)  # Smooth acceleration
            t = t * t * (3 - 2 * t)  # Additional smoothing
            
            intermediate_hip = current_hip + (hip_pos - current_hip) * t
            intermediate_knee = current_knee + (knee_pos - current_knee) * t
            
            # Publish joint positions
            self.joint_pubs[f'{leg_name}_joint1'].publish(intermediate_hip)
            self.joint_pubs[f'{leg_name}_joint2'].publish(intermediate_knee)
            
            # Log intermediate position
            rospy.loginfo(f"Step {step + 1}/{self.TRANSITION_STEPS}: hip={intermediate_hip:.3f}, knee={intermediate_knee:.3f}")
            
            rospy.sleep(transition_time / self.TRANSITION_STEPS)
        
        # Final position to ensure exact target
        self.joint_pubs[f'{leg_name}_joint1'].publish(hip_pos)
        self.joint_pubs[f'{leg_name}_joint2'].publish(knee_pos)
        
        # Verify leg reached target position
        if not self.check_leg_movement(leg_name, hip_pos, knee_pos):
            rospy.logwarn(f"Leg {leg_name} failed to reach target position")
            return False
            
        return True

    def check_natural_movement(self):
        """Check if the robot is moving naturally by monitoring leg movements"""
        moving_legs = 0
        total_legs = 0
        
        for leg in ['rf', 'lf', 'rb', 'lb']:
            total_legs += 1
            # Get current joint positions
            hip_joint = f'{leg}_joint1'
            knee_joint = f'{leg}_joint2'
            
            if hip_joint in self.joint_positions and knee_joint in self.joint_positions:
                # Check if either joint has moved significantly
                hip_change = abs(self.joint_positions[hip_joint] - self.last_joint_positions.get(hip_joint, self.joint_positions[hip_joint]))
                knee_change = abs(self.joint_positions[knee_joint] - self.last_joint_positions.get(knee_joint, self.joint_positions[knee_joint]))
                
                if hip_change > self.MIN_LEG_ANGLE_CHANGE or knee_change > self.MIN_LEG_ANGLE_CHANGE:
                    moving_legs += 1
                    rospy.loginfo(f"Leg {leg} is moving: hip_change={hip_change:.3f}, knee_change={knee_change:.3f}")
                else:
                    rospy.logwarn(f"Leg {leg} is not moving enough: hip_change={hip_change:.3f}, knee_change={knee_change:.3f}")
        
        # Update last positions
        self.last_joint_positions = self.joint_positions.copy()
        
        # Calculate movement ratio
        movement_ratio = moving_legs / total_legs if total_legs > 0 else 0
        
        if movement_ratio < self.MIN_LEG_MOVEMENT_RATIO:
            rospy.logwarn(f"Not enough legs moving: {moving_legs}/{total_legs} ({movement_ratio:.2f})")
            return False
            
        rospy.loginfo(f"Natural movement check passed: {moving_legs}/{total_legs} legs moving")
        return True

    def check_progress(self):
        """Check if the robot is making acceptable progress"""
        if self.initial_position is None or self.current_position is None:
            return True
            
        # Calculate current distance and speed
        distance = math.sqrt(
            (self.current_position.x - self.initial_position.x) ** 2 +
            (self.current_position.y - self.initial_position.y) ** 2
        )
        
        elapsed_time = (rospy.Time.now() - self.start_time).to_sec()
        if elapsed_time < 0.1:  # Avoid division by zero
            return True
            
        current_speed = distance / elapsed_time
        
        # Strict 10-second distance threshold check
        if elapsed_time >= 10.0:
            if distance < 2.0:  # Must cover 2 meters in 10 seconds
                rospy.logerr(f"Robot movement too slow: Only covered {distance:.2f}m in {elapsed_time:.1f}s")
                rospy.logerr(f"Current speed: {current_speed:.2f} m/s")
                rospy.logerr("Robot failed to meet minimum speed requirement - design needs iteration")
                return False
            else:
                rospy.loginfo(f"Robot passed speed test: {distance:.2f}m in {elapsed_time:.1f}s")
                rospy.loginfo(f"Average speed: {current_speed:.2f} m/s")
        
        # Check stability
        if not self.check_stability():
            rospy.logwarn("Robot stability check failed")
            return False
            
        rospy.loginfo(f"Progress: {distance:.2f}m at {current_speed:.2f} m/s")
        return True

    def run(self):
        """Run the movement test"""
        rospy.loginfo("Starting movement test...")
        self.start_time = rospy.Time.now()
        self.last_progress_check = rospy.Time.now()
        self.last_natural_movement_check = rospy.Time.now()
        
        # Initialize last joint positions
        self.last_joint_positions = self.joint_positions.copy()
        
        # Wait for initial position
        while not self.has_initial_position():
            rospy.sleep(0.1)
            
        rospy.loginfo(f"Initial position: x={self.initial_position.x:.3f}, y={self.initial_position.y:.3f}")
        
        # Main test loop
        while not rospy.is_shutdown():
            current_time = rospy.Time.now()
            
            # Check progress periodically
            if (current_time - self.last_progress_check).to_sec() >= self.MIN_PROGRESS_INTERVAL:
                if not self.check_progress():
                    rospy.logwarn("Test failed: Progress check failed")
                    break
                self.last_progress_check = current_time
                
            # Check natural movement periodically
            if (current_time - self.last_natural_movement_check).to_sec() >= self.NATURAL_MOVEMENT_CHECK_INTERVAL:
                if not self.check_natural_movement():
                    rospy.logwarn("Test failed: Natural movement check failed")
                    break
                self.last_natural_movement_check = current_time
                
            # Execute walking sequence
            self.walk_sequence()
            
            # Check if we've reached target distance
            if self.current_position is not None:
                distance = math.sqrt(
                    (self.current_position.x - self.initial_position.x) ** 2 +
                    (self.current_position.y - self.initial_position.y) ** 2
                )
                if distance >= self.TARGET_DISTANCE:
                    rospy.loginfo(f"Successfully reached target distance: {distance:.2f}m")
                    break
                    
            rospy.sleep(0.1)
            
        # Ensure robot returns to standing position
        rospy.loginfo("Test complete. Returning to standing position...")
        self.stand()
        
        # Log final position and performance metrics
        if self.current_position is not None:
            final_distance = math.sqrt(
                (self.current_position.x - self.initial_position.x) ** 2 +
                (self.current_position.y - self.initial_position.y) ** 2
            )
            elapsed_time = (rospy.Time.now() - self.start_time).to_sec()
            final_speed = final_distance / elapsed_time if elapsed_time > 0 else 0
            
            rospy.loginfo("\n=== Final Test Results ===")
            rospy.loginfo(f"Final Distance: {final_distance:.2f}m")
            rospy.loginfo(f"Final Speed: {final_speed:.2f}m/s")
            rospy.loginfo(f"Total Time: {elapsed_time:.2f}s")
            rospy.loginfo(f"Final Position: x={self.current_position.x:.3f}, y={self.current_position.y:.3f}")
            rospy.loginfo(f"Final Drift: {self.lateral_drift:.3f}m")
            rospy.loginfo(f"Final Angle: {self.direction_angle:.1f}°")
            
        rospy.loginfo("Test complete. Robot in standing position.")

    def stand(self):
        """Put the robot in a standing position"""
        rospy.loginfo("Setting standing position...")
        
        # Gradually return to standing position to avoid sudden movements
        # Start by guessing current positions based on where we ended the gait
        current_positions = {
            'rf': {'hip': self.HIP_BACK, 'knee': self.KNEE_DOWN},
            'lf': {'hip': self.HIP_BACK, 'knee': self.KNEE_DOWN},
            'rb': {'hip': self.HIP_BACK, 'knee': self.KNEE_DOWN},
            'lb': {'hip': self.HIP_BACK, 'knee': self.KNEE_DOWN}
        }
        
        # Gradually move to standing over 15 steps for smoother transition
        steps = 15
        for step in range(1, steps + 1):
            for leg in ['rf', 'lf', 'rb', 'lb']:
                hip_pos = current_positions[leg]['hip'] + (self.STAND_HIP - current_positions[leg]['hip']) * step / steps
                knee_pos = current_positions[leg]['knee'] + (self.STAND_KNEE - current_positions[leg]['knee']) * step / steps
                self.set_leg_position(leg, hip_pos, knee_pos)
            rospy.sleep(0.05)
        
        # Final set to ensure exact standing position
        for leg in ['rf', 'lf', 'rb', 'lb']:
            self.set_leg_position(leg, self.STAND_HIP, self.STAND_KNEE)
        
        rospy.loginfo("Standing position achieved")
        rospy.sleep(1.0)  # Allow time to stabilize in standing position

    def reset_position(self):
        """Reset the robot's position to the center of the map"""
        rospy.loginfo("Resetting robot position to center...")
        
        # First return to standing position
        self.stand()
        
        # Wait for model states to update
        rospy.sleep(1.0)
        
        # Reset position tracking
        self.initial_position = None
        self.current_position = None
        self.distance_traveled = 0.0
        self.lateral_drift = 0.0
        self.direction_angle = 0.0
        
        # Wait for position to be reset
        start_time = rospy.Time.now()
        while self.current_position is None and not rospy.is_shutdown():
            if (rospy.Time.now() - start_time).to_sec() > 5.0:
                rospy.logwarn("Timeout waiting for position reset")
                break
            rospy.sleep(0.1)
            
        if self.current_position:
            rospy.loginfo(f"Robot position reset to: x={self.current_position.x:.3f}, y={self.current_position.y:.3f}")
        else:
            rospy.logwarn("Could not verify position reset")
            
        rospy.sleep(1.0)  # Give time to stabilize
        return self.current_position is not None

    def has_initial_position(self):
        """Check if initial position has been set"""
        return self.initial_position is not None
    
    def walk_sequence(self):
        """Execute one complete walking sequence for the robot"""
        try:
            # Start a new walking cycle - prepare
            # Offset values for improved movement
            hip_forward = self.HIP_FORWARD 
            hip_mid = self.HIP_MID
            hip_back = self.HIP_BACK
            knee_up = self.KNEE_UP
            knee_mid = self.KNEE_MID
            knee_down = self.KNEE_DOWN
            
            # Prepare all legs for better balance before starting walking movement
            self.set_leg_position('rf', hip_mid, knee_mid, self.PHASE_1_TIME * 0.5)
            self.set_leg_position('lf', hip_mid, knee_mid, self.PHASE_1_TIME * 0.5)
            self.set_leg_position('rb', hip_mid, knee_mid, self.PHASE_1_TIME * 0.5)
            self.set_leg_position('lb', hip_mid, knee_mid, self.PHASE_1_TIME * 0.5)
            rospy.sleep(self.PHASE_1_TIME * 0.05)
            
            # DIAGONAL GAIT PATTERN
            # Diagonal pairs: (Right Front + Left Back) and (Left Front + Right Back)
            
            # === First Diagonal Pair (Left Front + Right Back) ===
            
            # Phase 1: Lift LF+RB legs while adjusting other legs for balance
            self.set_leg_position('lf', hip_forward - 0.02, knee_up, self.PHASE_1_TIME)
            self.set_leg_position('rb', hip_forward - 0.02, knee_up, self.PHASE_1_TIME)
            # Stabilize with other diagonal pair
            self.set_leg_position('rf', hip_back + 0.02, knee_down + 0.05, self.PHASE_1_TIME)
            self.set_leg_position('lb', hip_back + 0.02, knee_down + 0.05, self.PHASE_1_TIME)
            rospy.sleep(self.PHASE_1_TIME)
            
            # Phase 2: Move LF+RB legs forward
            self.set_leg_position('lf', hip_forward, knee_up, self.PHASE_2_TIME)
            self.set_leg_position('rb', hip_forward, knee_up, self.PHASE_2_TIME)
            rospy.sleep(self.PHASE_2_TIME)
            
            # Phase 3: Lower LF+RB legs
            self.set_leg_position('lf', hip_forward, knee_down, self.PHASE_3_TIME)
            self.set_leg_position('rb', hip_forward, knee_down, self.PHASE_3_TIME)
            rospy.sleep(self.PHASE_3_TIME)
            
            # Phase 4: Push with LF+RB legs while beginning to shift weight for next step
            self.set_leg_position('lf', hip_mid, knee_down, self.PHASE_4_TIME)
            self.set_leg_position('rb', hip_mid, knee_down, self.PHASE_4_TIME)
            # Pre-adjust the second diagonal pair to prepare for their movement
            self.set_leg_position('rf', hip_mid, knee_mid, self.PHASE_4_TIME)
            self.set_leg_position('lb', hip_mid, knee_mid, self.PHASE_4_TIME)
            rospy.sleep(self.PHASE_4_TIME)
            
            # === Second Diagonal Pair (Right Front + Left Back) ===
            
            # Phase 5: Lift RF+LB legs while maintaining pressure on first pair
            self.set_leg_position('rf', hip_forward - 0.02, knee_up, self.PHASE_1_TIME)
            self.set_leg_position('lb', hip_forward - 0.02, knee_up, self.PHASE_1_TIME)
            # Maintain stability with first diagonal pair
            self.set_leg_position('lf', hip_back + 0.02, knee_down + 0.05, self.PHASE_1_TIME)
            self.set_leg_position('rb', hip_back + 0.02, knee_down + 0.05, self.PHASE_1_TIME)
            rospy.sleep(self.PHASE_1_TIME)
            
            # Phase 6: Move RF+LB legs forward
            self.set_leg_position('rf', hip_forward, knee_up, self.PHASE_2_TIME)
            self.set_leg_position('lb', hip_forward, knee_up, self.PHASE_2_TIME)
            rospy.sleep(self.PHASE_2_TIME)
            
            # Phase 7: Lower RF+LB legs
            self.set_leg_position('rf', hip_forward, knee_down, self.PHASE_3_TIME)
            self.set_leg_position('lb', hip_forward, knee_down, self.PHASE_3_TIME)
            rospy.sleep(self.PHASE_3_TIME)
            
            # Phase 8: Push with RF+LB legs while returning other legs to neutral
            self.set_leg_position('rf', hip_mid, knee_down, self.PHASE_4_TIME)
            self.set_leg_position('lb', hip_mid, knee_down, self.PHASE_4_TIME)
            # Return first diagonal pair to ready position for next cycle
            self.set_leg_position('lf', hip_mid, knee_mid, self.PHASE_4_TIME)
            self.set_leg_position('rb', hip_mid, knee_mid, self.PHASE_4_TIME)
            rospy.sleep(self.PHASE_4_TIME)
            
            # End walking cycle in balanced position to maintain stability
            return True
            
        except Exception as e:
            rospy.logerr(f"Error in walk_sequence: {e}")
            return False

if __name__ == '__main__':
    try:
        walker = MovementTest()
        
        # Reset position before starting
        if not walker.reset_position():
            rospy.logerr("Failed to reset position")
            exit(1)
            
        # Execute walking test with performance monitoring
        walker.run()
        
        # Return to standing position
        walker.stand()
        
    except rospy.ROSInterruptException:
        pass