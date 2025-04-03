#!/usr/bin/env python3
import rospy
from std_msgs.msg import Float64
import time

def main():
    rospy.init_node('fixed_legs_controller')
    
    # Create publishers for each joint we want to control (all except right front leg)
    joint_pubs = {}
    
    # Skip joints 1 and 5 (right front leg hip and knee)
    for i in [2, 3, 4, 6, 7, 8]:
        topic = f'/puppy/joint{i}_position_controller/command'
        joint_pubs[i] = rospy.Publisher(topic, Float64, queue_size=1)
    
    rospy.sleep(1)  # Wait for publishers to initialize
    
    # Standing position values
    hip_angle = 0.8  # Approximately 45 degrees
    knee_angle = 0.0  # Straight legs
    
    # Set all joints except right front leg to standing position
    # Hip joints (2=lf, 3=rb, 4=lb)
    for i in [2, 3, 4]:
        joint_pubs[i].publish(hip_angle)
    
    # Knee joints (6=lf, 7=rb, 8=lb)
    for i in [6, 7, 8]:
        joint_pubs[i].publish(knee_angle)
    
    # Keep publishing the standing position to maintain pose
    rate = rospy.Rate(10)  # 10 Hz
    while not rospy.is_shutdown():
        # Hip joints (except right front)
        for i in [2, 3, 4]:
            joint_pubs[i].publish(hip_angle)
        
        # Knee joints (except right front)
        for i in [6, 7, 8]:
            joint_pubs[i].publish(knee_angle)
        
        rate.sleep()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass