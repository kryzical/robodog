#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
import sys
import time
import argparse

def rotate_left(angular_speed=0.5, duration=5.0):
    """
    Make the robot rotate left (counterclockwise) at the specified 
    angular speed for the specified duration.
    
    Args:
        angular_speed (float): Angular speed in rad/s
        duration (float): How long to rotate in seconds
    """
    rospy.init_node('rotate_left', anonymous=True)
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    
    # Give time for the publisher to connect
    rospy.loginfo("Waiting for connection to establish...")
    time.sleep(1)
    
    # Create the velocity command
    cmd = Twist()
    cmd.linear.x = 0.0  # No forward/backward motion
    cmd.angular.z = angular_speed  # Positive for counterclockwise rotation
    
    rospy.loginfo(f"Rotating left at {angular_speed:.2f} rad/s for {duration:.1f} seconds")
    
    # Send commands at a fixed rate
    start_time = time.time()
    rate = rospy.Rate(10)  # 10 Hz
    
    while time.time() - start_time < duration and not rospy.is_shutdown():
        pub.publish(cmd)
        rate.sleep()
    
    # Send stop command
    stop_cmd = Twist()
    rospy.loginfo("Sending stop command")
    for i in range(5):  # Send multiple times to ensure it's received
        pub.publish(stop_cmd)
        rate.sleep()
    
    rospy.loginfo("Left rotation completed")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Rotate the robot left (counterclockwise)')
    parser.add_argument('--speed', type=float, default=0.5, help='Angular speed in rad/s (default: 0.5)')
    parser.add_argument('--duration', type=float, default=5.0, help='Duration in seconds (default: 5.0)')
    args = parser.parse_args()
    
    try:
        rotate_left(args.speed, args.duration)
    except rospy.ROSInterruptException:
        pass 