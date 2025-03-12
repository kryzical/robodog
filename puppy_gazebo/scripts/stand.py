#!/usr/bin/env python3
import rospy
import math
from time import sleep
try:
    # Try to import the physical robot library
    from adafruit_servokit import ServoKit
    physical_robot = True
except ImportError:
    # In simulation, this won't be available
    physical_robot = False

# Initial servo angles for standing
STAND_ANGLES = {
    'lf1': 152,  # front left upper
    'lf2': 66,   # front left lower
    'lr1': 152,  # back left upper
    'lr2': 66,   # back left lower
    'rf1': 13,   # front right upper
    'rf2': 96,   # front right lower
    'rr1': 13,   # back right upper
    'rr2': 96    # back right lower
}

# Servo port mapping
SERVO_MAP = {
    'lf1': 4,
    'lf2': 5,
    'rf1': 6,
    'rf2': 7,
    'lr1': 12,
    'lr2': 13,
    'rr1': 14,
    'rr2': 15
}

# ROS publishers for simulation mode
publishers = {}

# Initialize physical or simulated robot
kit = None
simulation_mode = False

def init():
    """Initialize the control system - either physical or simulation"""
    global kit, simulation_mode
    
    if physical_robot:
        try:
            kit = ServoKit(channels=16)
            simulation_mode = False
            print("Initialized physical robot control")
            return
        except Exception as e:
            print(f"Could not initialize physical robot: {e}")
    
    # Fall back to simulation mode
    try:
        simulation_mode = True
        rospy.init_node('holder_robot_controller', anonymous=True)
        
        # Create publishers for each joint
        publishers['lf1'] = rospy.Publisher('/puppy/joint2_position_controller/command', rospy.messages.std_msgs.Float64, queue_size=1)
        publishers['lf2'] = rospy.Publisher('/puppy/joint6_position_controller/command', rospy.messages.std_msgs.Float64, queue_size=1)
        publishers['rf1'] = rospy.Publisher('/puppy/joint1_position_controller/command', rospy.messages.std_msgs.Float64, queue_size=1)
        publishers['rf2'] = rospy.Publisher('/puppy/joint5_position_controller/command', rospy.messages.std_msgs.Float64, queue_size=1)
        publishers['lr1'] = rospy.Publisher('/puppy/joint4_position_controller/command', rospy.messages.std_msgs.Float64, queue_size=1)
        publishers['lr2'] = rospy.Publisher('/puppy/joint8_position_controller/command', rospy.messages.std_msgs.Float64, queue_size=1)
        publishers['rr1'] = rospy.Publisher('/puppy/joint3_position_controller/command', rospy.messages.std_msgs.Float64, queue_size=1)
        publishers['rr2'] = rospy.Publisher('/puppy/joint7_position_controller/command', rospy.messages.std_msgs.Float64, queue_size=1)
        
        print("Initialized simulation robot control")
        return
    except Exception as e:
        print(f"Could not initialize simulation: {e}")
        raise

def physical_to_sim_angle(servo_name, angle):
    """
    Convert physical servo angles (degrees) to simulation joint angles (radians)
    Different servos have different orientations and zero points
    """
    if servo_name in ['lf1', 'lr1']:
        # Left upper servos: 0(forward) 180(backward)
        return math.radians(-(angle - 90))
    elif servo_name in ['lf2', 'lr2']:
        # Left lower servos: 0(extended) 180(in)
        return math.radians(angle - 90)
    elif servo_name in ['rf1', 'rr1']:
        # Right upper servos: 0(backward) 180(forward)
        return math.radians(angle - 90)
    elif servo_name in ['rf2', 'rr2']:
        # Right lower servos: 0(in) 180 (extended)
        return math.radians(-(angle - 90))
    return 0

def set_servo_angle(servo_name, angle):
    """Set the angle for a specific servo in either physical or simulation mode"""
    if not simulation_mode and kit is not None:
        # Physical robot
        servo_id = SERVO_MAP[servo_name]
        kit.servo[servo_id].angle = angle
    elif servo_name in publishers:
        # Simulation
        sim_angle = physical_to_sim_angle(servo_name, angle)
        publishers[servo_name].publish(sim_angle)

def set_joint_angles(angles_dict):
    """Set angles for multiple servos at once"""
    for servo_name, angle in angles_dict.items():
        set_servo_angle(servo_name, angle)

def stand():
    """Put the robot in a standing position"""
    print("Standing up")
    
    # Initialize if not already done
    if not simulation_mode and kit is None:
        init()
    
    # Set all joints to standing position
    set_joint_angles(STAND_ANGLES)
    print("Robot commanded to stand")
    
    # Give time for the robot to reach position
    sleep(1.0)

# Initialize when the module is imported
init()

if __name__ == "__main__":
    stand()