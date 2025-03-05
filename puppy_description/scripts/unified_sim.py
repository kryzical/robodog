#!/usr/bin/env python3

import rospy
import math
import time
from std_msgs.msg import Float64
from sensor_msgs.msg import JointState

class SimulationController:
    def __init__(self):
        """Initialize the simulation-only robot controller"""
        # Initialize the ROS node with anonymous=True to avoid name conflicts
        rospy.init_node('simulation_controller', anonymous=True)
        rospy.loginfo("SimulationController initializing...")
        
        # Initialize joint publishers for simulation
        self.joint_pubs = {
            'rf_joint1': rospy.Publisher('/puppy/joint1_position_controller/command', Float64, queue_size=10),
            'lf_joint1': rospy.Publisher('/puppy/joint2_position_controller/command', Float64, queue_size=10),
            'rb_joint1': rospy.Publisher('/puppy/joint3_position_controller/command', Float64, queue_size=10),
            'lb_joint1': rospy.Publisher('/puppy/joint4_position_controller/command', Float64, queue_size=10),
            'rf_joint2': rospy.Publisher('/puppy/joint5_position_controller/command', Float64, queue_size=10),
            'lf_joint2': rospy.Publisher('/puppy/joint6_position_controller/command', Float64, queue_size=10),
            'rb_joint2': rospy.Publisher('/puppy/joint7_position_controller/command', Float64, queue_size=10),
            'lb_joint2': rospy.Publisher('/puppy/joint8_position_controller/command', Float64, queue_size=10)
        }
        
        # Mapping between physical servo names and simulation joint names
        self.joint_mapping = {
            'lf1': 'lf_joint1',
            'lf2': 'lf_joint2',
            'rf1': 'rf_joint1',
            'rf2': 'rf_joint2',
            'lr1': 'lb_joint1',
            'lr2': 'lb_joint2',
            'rr1': 'rb_joint1',
            'rr2': 'rb_joint2'
        }
        
        # These values convert from physical servo angles to simulation angles
        self.angle_conversion = {
            'lf1': {'offset': 90, 'factor': 0.0174533, 'invert': True},  # 0.0174533 is pi/180
            'lf2': {'offset': 90, 'factor': 0.0174533, 'invert': False},
            'rf1': {'offset': 90, 'factor': 0.0174533, 'invert': False},
            'rf2': {'offset': 90, 'factor': 0.0174533, 'invert': True},
            'lr1': {'offset': 90, 'factor': 0.0174533, 'invert': True},
            'lr2': {'offset': 90, 'factor': 0.0174533, 'invert': False},
            'rr1': {'offset': 90, 'factor': 0.0174533, 'invert': False},
            'rr2': {'offset': 90, 'factor': 0.0174533, 'invert': True}
        }
        
        # Subscribe to joint states for feedback
        rospy.Subscriber('/puppy/joint_states', JointState, self.joint_states_callback)
        self.current_joint_states = None
        
        # Wait for connections to establish
        rospy.loginfo("Waiting for publishers to connect...")
        self.wait_for_connections()
        rospy.loginfo("All publishers connected successfully")
    
    def wait_for_connections(self):
        """Wait for publishers to establish connections"""
        timeout = 10.0  # seconds
        start_time = time.time()
        connected = False
        
        while not connected and (time.time() - start_time < timeout) and not rospy.is_shutdown():
            connected = True
            for name, pub in self.joint_pubs.items():
                if pub.get_num_connections() == 0:
                    connected = False
                    break
            
            if not connected:
                rospy.loginfo(f"Waiting for connections... ({time.time() - start_time:.1f}s)")
                rospy.sleep(0.5)
        
        if not connected:
            rospy.logwarn("Timed out waiting for connections to controllers!")
        else:
            rospy.loginfo("All controllers connected!")
    
    def joint_states_callback(self, msg):
        """Store joint state feedback"""
        self.current_joint_states = msg
    
    def physical_to_sim_angle(self, servo_name, physical_angle):
        """Convert physical servo angle (degrees) to simulation angle (radians)"""
        if servo_name not in self.angle_conversion:
            rospy.logwarn(f"Unknown servo name: {servo_name}")
            return 0.0
            
        params = self.angle_conversion[servo_name]
        # Apply offset, convert to radians, and invert if needed
        sim_angle = (physical_angle - params['offset']) * params['factor']
        if params['invert']:
            sim_angle = -sim_angle
            
        return sim_angle
    
    def set_joint_angles(self, physical_angles):
        """Convert physical angles to simulation angles and publish"""
        for servo_name, angle in physical_angles.items():
            # Convert and publish to simulation
            if servo_name in self.joint_mapping:
                sim_joint = self.joint_mapping[servo_name]
                sim_angle = self.physical_to_sim_angle(servo_name, angle)
                
                if sim_joint in self.joint_pubs:
                    try:
                        self.joint_pubs[sim_joint].publish(Float64(sim_angle))
                        rospy.logdebug(f"Published {servo_name} -> {sim_joint}: {angle}° -> {sim_angle} rad")
                    except Exception as e:
                        rospy.logerr(f"Error publishing to {sim_joint}: {e}")
                else:
                    rospy.logwarn(f"No publisher for joint: {sim_joint}")
            else:
                rospy.logwarn(f"Unknown servo mapping: {servo_name}")
    
    def trot_forward(self):
        """Execute the trot forward gait"""
        rospy.loginfo("Starting trot forward gait")
        
        # Initial angles
        lf1_a = 152
        lf2_a = 66
        lr1_a = 152
        lr2_a = 66
        rf1_a = 13
        rf2_a = 96
        rr1_a = 13
        rr2_a = 96
        interval_time = 0.05  # Slower in simulation for visualization
        
        physical_angles = {
            'lf1': lf1_a, 'lf2': lf2_a,
            'lr1': lr1_a, 'lr2': lr2_a,
            'rf1': rf1_a, 'rf2': rf2_a,
            'rr1': rr1_a, 'rr2': rr2_a
        }
        
        # Set initial position
        self.set_joint_angles(physical_angles)
        rospy.sleep(1)  # Give time for the robot to reach initial position
        
        for _ in range(1):  # Just one cycle for now
            # Phase 1: swing rf lr
            # Lift
            i = 40  # lr and rf diff
            j = 30  # lf and rr diff
            
            while i >= 0 or j >= 0:
                if i >= 0:
                    lr2_a += 1  # Lift back left leg
                    rf2_a -= 1  # Lift front right leg
                    i -= 1
                    
                if j >= 0:
                    rr2_a += 1  # Adjust back right leg
                    lf2_a -= 1  # Adjust front left leg
                    j -= 1
                    
                self.set_joint_angles({
                    'lr2': lr2_a, 'rf2': rf2_a,
                    'rr2': rr2_a, 'lf2': lf2_a
                })
                rospy.sleep(interval_time)
            
            # Move rf and lr down (finish swing)
            i = 30  # rf1 and lr1 diff
            j = 40  # rf2 and lr2 diff
            
            while i >= 0 or j >= 0:
                if i >= 0:
                    rf1_a += 1  # Move front right leg forward
                    lr1_a -= 1  # Move back left leg backward
                    i -= 1
                    
                if j >= 0:
                    rf2_a += 1  # Lower front right leg
                    lr2_a -= 1  # Lower back left leg
                    j -= 1
                    
                self.set_joint_angles({
                    'rf1': rf1_a, 'lr1': lr1_a,
                    'rf2': rf2_a, 'lr2': lr2_a
                })
                rospy.sleep(interval_time)
            
            # Phase 2: swing lf rr
            i = 11  # lf1 and rr1 diff
            j = 30  # rf1 and lr1 diff
            k = 5   # rf2 and lr2 diff
            
            while i >= 0 or j >= 0 or k >= 0:
                if i >= 0:
                    lf1_a += 1  # Adjust front left upper
                    rr1_a -= 1  # Adjust back right upper
                    i -= 1
                    
                if j >= 0:
                    rf1_a -= 1  # Return front right leg
                    lr1_a += 1  # Return back left leg
                    j -= 1
                    
                if k >= 0:
                    # No op for rf2/lr2 in this phase
                    k -= 1
                    
                self.set_joint_angles({
                    'lf1': lf1_a, 'rr1': rr1_a,
                    'rf1': rf1_a, 'lr1': lr1_a
                })
                rospy.sleep(interval_time)
            
            # Retract lf2 and rr2
            i = 40  # lf2 and rr2 diff
            while i >= 0:
                lf2_a += 1  # Lift front left leg
                rr2_a -= 1  # Lift back right leg
                i -= 1
                
                self.set_joint_angles({
                    'lf2': lf2_a, 'rr2': rr2_a
                })
                rospy.sleep(interval_time)
            
            # Swing lf1 and rr1 (return to standing)
            i = 12  # lf1 and rr1 diff
            j = 10  # lf2 and rr2 diff
            
            while i > 0 or j > 0:
                if i > 0:
                    lf1_a -= 1  # Return front left leg
                    rr1_a += 1  # Return back right leg
                    i -= 1
                    
                if j > 0:
                    lf2_a -= 1  # Lower front left leg
                    rr2_a += 1  # Lower back right leg
                    j -= 1
                    
                self.set_joint_angles({
                    'lf1': lf1_a, 'rr1': rr1_a,
                    'lf2': lf2_a, 'rr2': rr2_a
                })
                rospy.sleep(interval_time)
        
        rospy.loginfo("Trot cycle completed")

    def turn_left(self):
        """Execute the turn left gait"""
        rospy.loginfo("Turn left not implemented yet")
        # TODO: Implement turn left gait
        pass
        
    def stand(self):
        """Put the robot in a standing position"""
        rospy.loginfo("Standing up")
        # Standard standing position
        physical_angles = {
            'lf1': 152, 'lf2': 66,
            'lr1': 152, 'lr2': 66,
            'rf1': 13,  'rf2': 96,
            'rr1': 13,  'rr2': 96
        }
        self.set_joint_angles(physical_angles)
        rospy.sleep(1)  # Give time to reach position
    
    def continuous_trot(self, cycles=5):
        """Execute multiple trot cycles"""
        rospy.loginfo(f"Starting continuous trot for {cycles} cycles")
        
        for i in range(cycles):
            rospy.loginfo(f"Cycle {i+1}/{cycles}")
            self.trot_forward()
            rospy.sleep(0.1)  # Short pause between cycles

if __name__ == '__main__':
    try:
        rospy.loginfo("Initializing simulation robot controller")
        controller = SimulationController()
        rospy.sleep(3)  # Increased wait time for full initialization
        
        # Print the current ROS topic list to debug
        rospy.loginfo("Available ROS topics:")
        topics = rospy.get_published_topics()
        for topic_name, topic_type in topics:
            rospy.loginfo(f" - {topic_name} [{topic_type}]")
        
        # Execute sequence of movements
        controller.stand()
        rospy.sleep(2)
        controller.continuous_trot(cycles=3)  # Do 3 trot cycles
        controller.stand()  # Return to standing position
        
        rospy.loginfo("Movement sequence completed")
        rospy.spin()  # Keep the node running
    except rospy.ROSInterruptException:
        rospy.loginfo("Program interrupted by user")
    except Exception as e:
        rospy.logerr(f"Error: {e}")