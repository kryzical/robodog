#!/usr/bin/env python3
import rospy
from std_msgs.msg import Float64
from sensor_msgs.msg import JointState
from adafruit_servokit import ServoKit
import time

class UnifiedRobotController:
    def __init__(self):
        rospy.init_node('unified_robot_controller')
        
        # Initialize physical robot control
        self.kit = ServoKit(channels=16)
        
        # Physical servo mappings
        self.servo_map = {
            'lf1': 4,  # front left upper
            'lf2': 5,  # front left lower
            'rf1': 6,  # front right upper
            'rf2': 7,  # front right lower
            'lr1': 12, # back left upper
            'lr2': 13, # back left lower
            'rr1': 14, # back right upper
            'rr2': 15  # back right lower
        }
        
        # Initialize ROS publishers for simulation
        self.joint_pubs = {
            'rf_joint1': rospy.Publisher('/puppy/joint1_position_controller/command', Float64, queue_size=1),
            'lf_joint1': rospy.Publisher('/puppy/joint2_position_controller/command', Float64, queue_size=1),
            'rb_joint1': rospy.Publisher('/puppy/joint3_position_controller/command', Float64, queue_size=1),
            'lb_joint1': rospy.Publisher('/puppy/joint4_position_controller/command', Float64, queue_size=1),
            'rf_joint2': rospy.Publisher('/puppy/joint5_position_controller/command', Float64, queue_size=1),
            'lf_joint2': rospy.Publisher('/puppy/joint6_position_controller/command', Float64, queue_size=1),
            'rb_joint2': rospy.Publisher('/puppy/joint7_position_controller/command', Float64, queue_size=1),
            'lb_joint2': rospy.Publisher('/puppy/joint8_position_controller/command', Float64, queue_size=1)
        }
        
        # Angle conversion parameters (physical degrees to simulation radians)
        # These values need to be calibrated for your specific robot
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

    def physical_to_sim_angle(self, servo_name, physical_angle):
        """Convert physical servo angle (degrees) to simulation angle (radians)"""
        if servo_name not in self.angle_conversion:
            return 0.0
            
        params = self.angle_conversion[servo_name]
        # Apply offset, convert to radians, and invert if needed
        sim_angle = (physical_angle - params['offset']) * params['factor']
        if params['invert']:
            sim_angle = -sim_angle
            
        return sim_angle

    def set_joint_angles(self, physical_angles):
        # Update physical robot
        for servo_name, angle in physical_angles.items():
            if servo_name in self.servo_map:
                self.kit.servo[self.servo_map[servo_name]].angle = angle
                
                # Convert and publish to simulation
                if servo_name in self.joint_mapping:
                    sim_joint = self.joint_mapping[servo_name]
                    sim_angle = self.physical_to_sim_angle(servo_name, angle)
                    if sim_joint in self.joint_pubs:
                        self.joint_pubs[sim_joint].publish(Float64(sim_angle))

    def trot_forward(self):
        print("Starting trot forward gait")
        # Initial angles
        lf1_a = 152
        lf2_a = 66
        lr1_a = 152
        lr2_a = 66
        rf1_a = 13
        rf2_a = 96
        rr1_a = 13
        rr2_a = 96
        interval_time = 0.00005  # Very small delay for smoother motion
        
        physical_angles = {
            'lf1': lf1_a, 'lf2': lf2_a,
            'lr1': lr1_a, 'lr2': lr2_a,
            'rf1': rf1_a, 'rf2': rf2_a,
            'rr1': rr1_a, 'rr2': rr2_a
        }
        
        # Set initial position
        self.set_joint_angles(physical_angles)
        time.sleep(1)  # Give time for the robot to reach initial position
        
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
                time.sleep(interval_time)
            
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
                time.sleep(interval_time)
            
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
                    # Commented out in original:
                    # rf2_a += 1
                    # lr2_a -= 1
                    k -= 1
                    
                self.set_joint_angles({
                    'lf1': lf1_a, 'rr1': rr1_a,
                    'rf1': rf1_a, 'lr1': lr1_a
                })
                time.sleep(interval_time)
            
            # Retract lf2 and rr2
            i = 40  # lf2 and rr2 diff
            while i >= 0:
                lf2_a += 1  # Lift front left leg
                rr2_a -= 1  # Lift back right leg
                i -= 1
                
                self.set_joint_angles({
                    'lf2': lf2_a, 'rr2': rr2_a
                })
                time.sleep(interval_time)
            
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
                time.sleep(interval_time)
        
        print("Trot cycle completed")
        
    def turn_left(self):
        print("Turn left not implemented yet")
        # TODO: Implement turn left gait
        pass
        
    def stand(self):
        """Put the robot in a standing position"""
        print("Standing up")
        # Standard standing position
        physical_angles = {
            'lf1': 152, 'lf2': 66,
            'lr1': 152, 'lr2': 66,
            'rf1': 13,  'rf2': 96,
            'rr1': 13,  'rr2': 96
        }
        self.set_joint_angles(physical_angles)
        time.sleep(1)  # Give time to reach position

if __name__ == '__main__':
    try:
        controller = UnifiedRobotController()
        rospy.sleep(1)  # Wait for everything to initialize
        controller.stand()
        controller.trot_forward()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
    except Exception as e:
        rospy.logerr(f"Error: {e}")