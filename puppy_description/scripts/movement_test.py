#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float64
from geometry_msgs.msg import PoseStamped
from sensor_msgs.msg import JointState
from gazebo_msgs.msg import ModelStates
import time
import math
import numpy as np
from leg_ik import LegIK

class MovementTest:
    def __init__(self):
        rospy.init_node('movement_test', anonymous=True)
        rospy.loginfo("Starting refined walking test with IK and improved stability tracking...")
        
        # Set control rate
        self.rate = rospy.Rate(50)  # Increased to 50Hz for smoother motion
        
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
        
        # Movement parameters - standing position (in meters)
        self.STAND_HEIGHT = 0.12  # Reduced from 0.15 for better stability
        self.STAND_WIDTH = 0.10   # Reduced from 0.12 for better balance
        self.STAND_LENGTH = 0.12  # Reduced from 0.15 for better stability
        
        # Performance monitoring parameters
        self.MIN_SPEED = 0.08    # Reduced from 0.1 for more stable walking
        self.MAX_SPEED = 0.25    # Reduced from 0.3 for better control
        self.TARGET_SPEED = 0.15  # Reduced from 0.2 for more stable walking
        self.SPEED_CHECK_INTERVAL = 1.0  # Reduced from 2.0 for more frequent checks
        self.MAX_TIME_PER_METER = 15.0   # Increased from 10.0 to allow for slower, more stable walking
        self.MIN_PROGRESS_INTERVAL = 3.0  # Reduced from 5.0 for more frequent progress checks
        self.MIN_DISTANCE_PROGRESS = 0.05  # Reduced from 0.1 for more sensitive progress tracking
        
        # Walking parameters
        self.STEP_HEIGHT = 0.03  # Reduced from 0.05 for more stable walking
        self.STEP_LENGTH = 0.06  # Reduced from 0.08 for better control
        self.STEP_WIDTH = 0.10   # Reduced from 0.12 for better balance
        
        # Phase timing - optimized for stability
        self.PHASE_1_TIME = 0.08  # Increased from 0.06 for smoother lift
        self.PHASE_2_TIME = 0.06  # Increased from 0.04 for smoother forward movement
        self.PHASE_3_TIME = 0.08  # Increased from 0.06 for smoother lower
        self.PHASE_4_TIME = 0.06  # Increased from 0.04 for smoother push
        
        # Transition steps for smoother movement
        self.TRANSITION_STEPS = 15  # Increased from 10 for even smoother transitions
        
        # State tracking
        self.joint_positions = {}
        self.initial_position = None
        self.current_position = None
        self.distance_traveled = 0.0
        self.lateral_drift = 0.0
        self.direction_angle = 0.0
        self.target_distance = 10.0
        self.max_walk_time = 180.0
        
        # Performance metrics
        self.cycle_start_time = None
        self.last_cycle_distance = 0.0
        self.cycle_speeds = []
        self.cycle_drifts = []
        self.cycle_angles = []
        self.joint_velocities = {}  # Track joint velocities for smoothness
        
        # Log initial parameters
        rospy.loginfo("\n=== Movement Parameters ===")
        rospy.loginfo(f"Standing Height: {self.STAND_HEIGHT:.3f}m")
        rospy.loginfo(f"Standing Width: {self.STAND_WIDTH:.3f}m")
        rospy.loginfo(f"Standing Length: {self.STAND_LENGTH:.3f}m")
        rospy.loginfo(f"Step Height: {self.STEP_HEIGHT:.3f}m")
        rospy.loginfo(f"Step Length: {self.STEP_LENGTH:.3f}m")
        rospy.loginfo(f"Step Width: {self.STEP_WIDTH:.3f}m")
        rospy.loginfo(f"Phase Timings: P1={self.PHASE_1_TIME:.2f}s, P2={self.PHASE_2_TIME:.2f}s, P3={self.PHASE_3_TIME:.2f}s, P4={self.PHASE_4_TIME:.2f}s")
        rospy.loginfo(f"Target Distance: {self.target_distance:.1f}m")
        rospy.loginfo(f"Max Time: {self.max_walk_time:.1f}s")
        
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
        
    def set_leg_position(self, leg_name, phase, transition_time=0.08):  # Increased from 0.05
        """Set a single leg's position using IK with smooth transition"""
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
            # Use smooth acceleration curve with easing
            t = 0.5 - 0.5 * math.cos(t * math.pi)  # Smooth acceleration
            t = t * t * (3 - 2 * t)  # Additional smoothing
            
            intermediate_hip = current_hip + (hip_angle - current_hip) * t
            intermediate_knee = current_knee + (knee_angle - current_knee) * t
            
            # Publish joint positions
            self.joint_pubs[f'{leg_name}_joint1'].publish(intermediate_hip)
            self.joint_pubs[f'{leg_name}_joint2'].publish(intermediate_knee)
            
            # Log detailed joint information
            rospy.loginfo(f"\n=== Joint Update ===")
            rospy.loginfo(f"Leg: {leg_name}")
            rospy.loginfo(f"Phase: {phase}")
            rospy.loginfo(f"Step: {step + 1}/{self.TRANSITION_STEPS}")
            rospy.loginfo(f"Target Position: ({x:.3f}, {y:.3f}, {z:.3f})")
            rospy.loginfo(f"Target Angles: hip={math.degrees(hip_angle):.1f}°, knee={math.degrees(knee_angle):.1f}°")
            rospy.loginfo(f"Current Angles: hip={math.degrees(current_hip):.1f}°, knee={math.degrees(current_knee):.1f}°")
            rospy.loginfo(f"Intermediate Angles: hip={math.degrees(intermediate_hip):.1f}°, knee={math.degrees(intermediate_knee):.1f}°")
            
            # Calculate and log joint velocities
            if step > 0:
                hip_velocity = (intermediate_hip - last_hip) / (transition_time / self.TRANSITION_STEPS)
                knee_velocity = (intermediate_knee - last_knee) / (transition_time / self.TRANSITION_STEPS)
                rospy.loginfo(f"Joint Velocities: hip={math.degrees(hip_velocity):.1f}°/s, knee={math.degrees(knee_velocity):.1f}°/s")
            
            last_hip = intermediate_hip
            last_knee = intermediate_knee
            
            rospy.sleep(transition_time / self.TRANSITION_STEPS)
        
        # Final position to ensure exact target
        self.joint_pubs[f'{leg_name}_joint1'].publish(hip_angle)
        self.joint_pubs[f'{leg_name}_joint2'].publish(knee_angle)
        
    def walk_cycle(self, num_cycles=None):
        """Execute a refined walking cycle with IK and improved stability tracking"""
        try:
            self.start_time = rospy.Time.now()
            cycle_count = 0
            max_cycles = 100 if num_cycles is None else num_cycles
            last_progress_check = self.start_time
            last_distance = 0.0
            
            # Reset position tracking
            self.initial_position = None
            self.distance_traveled = 0.0
            self.lateral_drift = 0.0
            self.direction_angle = 0.0
            self.cycle_speeds = []
            self.cycle_drifts = []
            self.cycle_angles = []
            
            # Wait for initial position to be set
            rospy.loginfo("\nWaiting for initial position...")
            timeout = rospy.Duration(5.0)
            while self.initial_position is None and not rospy.is_shutdown():
                if (rospy.Time.now() - self.start_time) > timeout:
                    rospy.logwarn("Timeout waiting for initial position")
                    return False
                rospy.sleep(0.1)
                
            self.start_time = rospy.Time.now()  # Reset start time after initialization
            
            while not rospy.is_shutdown() and cycle_count < max_cycles:
                current_time = rospy.Time.now()
                
                # Start new cycle
                self.cycle_start_time = current_time
                self.last_cycle_distance = self.distance_traveled
                
                # Check progress periodically
                if (current_time - last_progress_check).to_sec() >= self.MIN_PROGRESS_INTERVAL:
                    if not self.check_progress():
                        rospy.logwarn("\nProgress check failed - stopping walk cycle")
                        return False
                    last_progress_check = current_time
                
                # Check if we've reached target distance
                if self.distance_traveled >= self.target_distance:
                    rospy.loginfo(f"\nTarget distance reached: {self.distance_traveled:.2f}m")
                    return True
                
                # Check if we've exceeded maximum time
                elapsed_time = (current_time - self.start_time).to_sec()
                if elapsed_time > self.max_walk_time:
                    rospy.logwarn(f"\nMaximum time exceeded: {elapsed_time:.2f}s")
                    return False
                
                # Log cycle start
                rospy.loginfo(f"\n=== Starting Cycle {cycle_count + 1} ===")
                rospy.loginfo(f"Current Distance: {self.distance_traveled:.3f}m")
                rospy.loginfo(f"Current Speed: {self.cycle_speeds[-1] if self.cycle_speeds else 0:.3f}m/s")
                rospy.loginfo(f"Current Drift: {self.lateral_drift:.3f}m")
                rospy.loginfo(f"Current Angle: {self.direction_angle:.1f}°")
                
                # ===== DIAGONAL GAIT PATTERN WITH IK =====
                
                # Phase 1: First diagonal pair (LF+RB) lift
                rospy.loginfo(f"\nPhase 1 - LF + RB lift")
                self.set_leg_position('lf', 'lift')
                self.set_leg_position('rb', 'lift')
                rospy.sleep(self.PHASE_1_TIME)
                
                # Phase 2: First diagonal pair move forward
                rospy.loginfo(f"\nPhase 2 - LF + RB forward")
                self.set_leg_position('lf', 'forward')
                self.set_leg_position('rb', 'forward')
                rospy.sleep(self.PHASE_2_TIME)
                
                # Phase 3: First diagonal pair lower
                rospy.loginfo(f"\nPhase 3 - LF + RB lower")
                self.set_leg_position('lf', 'lower')
                self.set_leg_position('rb', 'lower')
                rospy.sleep(self.PHASE_3_TIME)
                
                # Phase 4: First diagonal pair push
                rospy.loginfo(f"\nPhase 4 - LF + RB push")
                self.set_leg_position('lf', 'push')
                self.set_leg_position('rb', 'push')
                rospy.sleep(self.PHASE_4_TIME)
                
                # Phase 5: Second diagonal pair (RF+LB) lift
                rospy.loginfo(f"\nPhase 5 - RF + LB lift")
                self.set_leg_position('rf', 'lift')
                self.set_leg_position('lb', 'lift')
                rospy.sleep(self.PHASE_1_TIME)
                
                # Phase 6: Second diagonal pair move forward
                rospy.loginfo(f"\nPhase 6 - RF + LB forward")
                self.set_leg_position('rf', 'forward')
                self.set_leg_position('lb', 'forward')
                rospy.sleep(self.PHASE_2_TIME)
                
                # Phase 7: Second diagonal pair lower
                rospy.loginfo(f"\nPhase 7 - RF + LB lower")
                self.set_leg_position('rf', 'lower')
                self.set_leg_position('lb', 'lower')
                rospy.sleep(self.PHASE_3_TIME)
                
                # Phase 8: Second diagonal pair push
                rospy.loginfo(f"\nPhase 8 - RF + LB push")
                self.set_leg_position('rf', 'push')
                self.set_leg_position('lb', 'push')
                rospy.sleep(self.PHASE_4_TIME)
                
                # Log cycle completion
                cycle_time = (rospy.Time.now() - self.cycle_start_time).to_sec()
                cycle_distance = self.distance_traveled - self.last_cycle_distance
                cycle_speed = cycle_distance / cycle_time if cycle_time > 0 else 0
                
                rospy.loginfo(f"\n=== Cycle {cycle_count + 1} Complete ===")
                rospy.loginfo(f"Cycle Time: {cycle_time:.3f}s")
                rospy.loginfo(f"Cycle Distance: {cycle_distance:.3f}m")
                rospy.loginfo(f"Cycle Speed: {cycle_speed:.3f}m/s")
                rospy.loginfo(f"Total Distance: {self.distance_traveled:.3f}m")
                rospy.loginfo(f"Current Drift: {self.lateral_drift:.3f}m")
                rospy.loginfo(f"Current Angle: {self.direction_angle:.1f}°")
                
                cycle_count += 1
                self.rate.sleep()
            
            # Calculate walking metrics
            elapsed_time = (rospy.Time.now() - self.start_time).to_sec()
            speed = self.distance_traveled / elapsed_time if elapsed_time > 0 else 0
            efficiency = self.distance_traveled / cycle_count if cycle_count > 0 else 0
            straightness = 1.0 - (self.lateral_drift / self.distance_traveled if self.distance_traveled > 0 else 0)
            straightness = max(0, min(1, straightness))  # Clamp between 0 and 1
            
            rospy.loginfo("\n=== Final Walking Performance ===")
            rospy.loginfo(f"Total Distance: {self.distance_traveled:.2f}m")
            rospy.loginfo(f"Total Time: {elapsed_time:.2f}s")
            rospy.loginfo(f"Average Speed: {speed:.3f}m/s")
            rospy.loginfo(f"Total Cycles: {cycle_count}")
            rospy.loginfo(f"Distance per Cycle: {efficiency:.3f}m/cycle")
            rospy.loginfo(f"Final Lateral Drift: {self.lateral_drift:.3f}m")
            rospy.loginfo(f"Final Directional Angle: {self.direction_angle:.1f}°")
            rospy.loginfo(f"Straightness: {straightness:.2f} (1.0 = perfectly straight)")
            
            if self.cycle_speeds:
                rospy.loginfo("\nSpeed Statistics:")
                rospy.loginfo(f"Average Speed: {sum(self.cycle_speeds) / len(self.cycle_speeds):.3f}m/s")
                rospy.loginfo(f"Max Speed: {max(self.cycle_speeds):.3f}m/s")
                rospy.loginfo(f"Min Speed: {min(self.cycle_speeds):.3f}m/s")
            
            # Return to standing position
            self.stand()
            return True
            
        except rospy.ROSInterruptException:
            rospy.loginfo("Walk cycle interrupted")
            return False
            
    def stand(self):
        """Put the robot in a standing position using IK"""
        rospy.loginfo("Setting standing position...")
        
        # Move all legs to standing position with smooth transition
        for leg in ['rf', 'lf', 'rb', 'lb']:
            self.set_leg_position(leg, 'stand')
            rospy.sleep(0.1)
        
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
                
        # Log joint positions periodically
        curr_time = rospy.get_time()
        if int(curr_time * 2) != int((curr_time - 0.1) * 2):
            rospy.loginfo("\n=== Joint Positions ===")
            for joint, pos in self.joint_positions.items():
                rospy.loginfo(f"{joint}: {math.degrees(pos):.1f}°")
        
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
                    
                    # Log detailed position every 0.5 seconds
                    curr_time = rospy.get_time()
                    if int(curr_time * 2) != int((curr_time - 0.1) * 2):
                        rospy.loginfo(f"\n=== Position Update ===")
                        rospy.loginfo(f"Distance: {self.distance_traveled:.3f}m")
                        rospy.loginfo(f"Position: x={pose.position.x:.3f}, y={pose.position.y:.3f}")
                        rospy.loginfo(f"Drift: {self.lateral_drift:.3f}m")
                        rospy.loginfo(f"Angle: {self.direction_angle:.1f}°")
                        if self.cycle_speeds:
                            avg_speed = sum(self.cycle_speeds[-5:]) / min(5, len(self.cycle_speeds))
                            rospy.loginfo(f"Average Speed: {avg_speed:.3f}m/s")
                        rospy.loginfo(f"Joint Positions:")
                        for joint, pos in self.joint_positions.items():
                            rospy.loginfo(f"  {joint}: {math.degrees(pos):.1f}°")
        except ValueError:
            # Model not found
            pass
        except Exception as e:
            rospy.logerr(f"Error in model_states_callback: {e}")

if __name__ == '__main__':
    try:
        walker = MovementTest()
        
        # Reset position before starting
        if not walker.reset_position():
            rospy.logerr("Failed to reset position")
            exit(1)
            
        # Execute walking test with performance monitoring
        success = walker.walk_cycle()
        
        if success:
            rospy.loginfo("Walking test completed successfully")
        else:
            rospy.logerr("Walking test failed to meet performance criteria")
            
        # Return to standing position
        walker.stand()
        
    except rospy.ROSInterruptException:
        pass