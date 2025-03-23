#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist

def cmd_vel_callback(data):
    """Callback for velocity commands"""
    rospy.loginfo("ROBOT MOVEMENT: linear.x=%.2f, angular.z=%.2f", data.linear.x, data.angular.z)
    
    # Print human-readable description of the movement
    if abs(data.linear.x) > 0.1 and abs(data.angular.z) < 0.1:
        if data.linear.x > 0:
            rospy.loginfo("=> Robot is moving FORWARD")
        else:
            rospy.loginfo("=> Robot is moving BACKWARD")
    elif abs(data.angular.z) > 0.1 and abs(data.linear.x) < 0.1:
        if data.angular.z > 0:
            rospy.loginfo("=> Robot is turning LEFT")
        else:
            rospy.loginfo("=> Robot is turning RIGHT")
    elif abs(data.linear.x) > 0.1 and abs(data.angular.z) > 0.1:
        rospy.loginfo("=> Robot is moving in a CURVE")
    elif abs(data.linear.x) < 0.01 and abs(data.angular.z) < 0.01:
        rospy.loginfo("=> Robot is STOPPED")

if __name__ == '__main__':
    rospy.init_node('velocity_monitor', anonymous=True)
    rospy.loginfo("Velocity monitor started - watching for cmd_vel messages")
    rospy.Subscriber('/cmd_vel', Twist, cmd_vel_callback)
    rospy.spin()
