#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
import time
import sys
import signal

def signal_handler(sig, frame):
    """Handle SIGINT for clean shutdown"""
    print("Shutting down...")
    # Send stop command before exiting
    stop_cmd = Twist()
    pub.publish(stop_cmd)
    sys.exit(0)

if __name__ == '__main__':
    # Initialize ROS node
    rospy.init_node('simple_velocity_test', anonymous=True)
    
    # Set up signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    
    # Create publisher for velocity commands
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    
    # Set control rate
    rate = rospy.Rate(10)  # 10 Hz
    
    print("Simple velocity test starting...")
    print("Publishing zero velocity for 2 seconds to ensure robot is in standing position")
    
    # First publish zero velocity for 2 seconds to ensure robot is in standing position
    start_time = time.time()
    while time.time() - start_time < 2.0 and not rospy.is_shutdown():
        stop_cmd = Twist()
        pub.publish(stop_cmd)
        rate.sleep()
    
    # Now publish forward velocity for 5 seconds
    print("Publishing forward velocity (0.2 m/s) for 5 seconds")
    forward_cmd = Twist()
    forward_cmd.linear.x = 0.2
    
    start_time = time.time()
    while time.time() - start_time < 5.0 and not rospy.is_shutdown():
        pub.publish(forward_cmd)
        rate.sleep()
    
    # Stop the robot
    print("Stopping robot")
    stop_cmd = Twist()
    
    start_time = time.time()
    while time.time() - start_time < 2.0 and not rospy.is_shutdown():
        pub.publish(stop_cmd)
        rate.sleep()
        
    print("Test complete!") 