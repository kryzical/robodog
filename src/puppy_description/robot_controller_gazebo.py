#!/usr/bin/env python
import math
import rospy
import numpy as np
from std_msgs.msg import Float64, Float32MultiArray

def servo_callback(msg):
    joint_angles = msg.data
    #print(np.array(np.array(joint_angles)*2000/math.pi, np.uint32) + 500)
    
    for i in range(len(joint_angles)):
        if i in [0, 2, 5, 7]:
            publishers[i].publish(joint_angles[i])
        else:
            publishers[i].publish(joint_angles[i])

if __name__ == "__main__":
    rospy.init_node("test")

    command_topics = ["/puppy/joint1_position_controller/command",
                      "/puppy/joint2_position_controller/command",
                      "/puppy/joint3_position_controller/command",
                      "/puppy/joint4_position_controller/command",
                      "/puppy/joint5_position_controller/command",
                      "/puppy/joint6_position_controller/command",
                      "/puppy/joint7_position_controller/command",
                      "/puppy/joint8_position_controller/command"]

    publishers = []
    for i in range(len(command_topics)):
        publishers.append(rospy.Publisher(command_topics[i], Float64, queue_size = 10))
    
    rospy.Subscriber('/puppy_control/legs_servo_value', Float32MultiArray, servo_callback)
    print('start')
    
    try:
        rospy.spin()
    except BaseException as e:
        print(e)
