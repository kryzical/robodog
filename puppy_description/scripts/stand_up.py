#!/usr/bin/env python3
import rospy
from std_msgs.msg import Float64
import time

def main():
    rospy.init_node('stand_up_controller')
    
    # Create publishers for each joint
    joint_pubs = {}
    for i in range(1, 9):
        topic = f'/puppy/joint{i}_position_controller/command'
        joint_pubs[i] = rospy.Publisher(topic, Float64, queue_size=1)
    
    rospy.sleep(1)  # Wait for publishers to initialize
    
    # Standing position values that we know work
    hip_angle = 0.8  # Approximately 45 degrees
    knee_angle = 0.0  # Straight legs
    
    # Set all joints to standing position
    for i in range(1, 9, 2):  # Hip joints (1,3,5,7)
        joint_pubs[i].publish(hip_angle)
    for i in range(2, 9, 2):  # Knee joints (2,4,6,8)
        joint_pubs[i].publish(knee_angle)
    
    # Keep publishing the standing position
    rate = rospy.Rate(10)  # 10 Hz
    while not rospy.is_shutdown():
        for i in range(1, 9, 2):  # Hip joints
            joint_pubs[i].publish(hip_angle)
        for i in range(2, 9, 2):  # Knee joints
            joint_pubs[i].publish(knee_angle)
        rate.sleep()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass 