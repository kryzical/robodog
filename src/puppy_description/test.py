#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64, Float32MultiArray

def servo_callback(msg):
    print(msg)

if __name__ == "__main__":
    rospy.init_node("sub")

    rospy.Subscriber('/puppy/joint1_position_controller/command', Float64, servo_callback)
    print('start')
    
    try:
        rospy.spin()
    except BaseException as e:
        print(e)
