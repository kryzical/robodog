#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
import sys
import time
import argparse

def walk_forward(linear_speed=0.2, duration=10.0):
    """
    Make the robot walk forward at the specified speed for the specified duration.
    
    Args:
        linear_speed (float): Forward speed in m/s
        duration (float): How long to walk in seconds
    """
    rospy.init_node('walk_forward', anonymous=True)
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    
    # Give time for the publisher to connect
    rospy.loginfo("Waiting for connection to establish...")
    time.sleep(1)
    
    # Create the velocity command
    cmd = Twist()
    cmd.linear.x = linear_speed
    cmd.angular.z = 0.0  # No rotation
    
    rospy.loginfo(f"Walking forward at {linear_speed:.2f} m/s for {duration:.1f} seconds")
    
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
    
    rospy.loginfo("Forward walking completed")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Walk the robot forward')
    parser.add_argument('--speed', type=float, default=0.2, help='Linear speed in m/s (default: 0.2)')
    parser.add_argument('--duration', type=float, default=10.0, help='Duration in seconds (default: 10.0)')
    args = parser.parse_args()
    
    try:
        walk_forward(args.speed, args.duration)
    except rospy.ROSInterruptException:
        pass 