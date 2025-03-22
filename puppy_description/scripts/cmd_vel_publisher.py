#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
import time
import argparse

def send_velocity_command(linear_x, angular_z, duration):
    """Send a velocity command for the specified duration"""
    rospy.init_node('cmd_vel_publisher', anonymous=True)
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    
    # Wait for connection to establish
    rospy.loginfo("Waiting for connection to velocity_walker...")
    time.sleep(1)
    
    cmd = Twist()
    cmd.linear.x = linear_x
    cmd.angular.z = angular_z
    
    rospy.loginfo(f"Sending command: linear.x={linear_x:.2f}, angular.z={angular_z:.2f} for {duration:.1f} seconds")
    
    start_time = time.time()
    rate = rospy.Rate(10)  # 10 Hz
    
    while time.time() - start_time < duration and not rospy.is_shutdown():
        pub.publish(cmd)
        rate.sleep()
    
    # Send stop command if we were moving
    if abs(linear_x) > 0.01 or abs(angular_z) > 0.01:
        stop_cmd = Twist()
        rospy.loginfo("Sending stop command")
        for i in range(10):  # Send multiple stop commands to ensure it's received
            pub.publish(stop_cmd)
            rate.sleep()
    
    rospy.loginfo("Command completed")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simple cmd_vel publisher for testing')
    parser.add_argument('--linear', type=float, default=0.2, help='Linear velocity (default: 0.2)')
    parser.add_argument('--angular', type=float, default=0.0, help='Angular velocity (default: 0.0)')
    parser.add_argument('--duration', type=float, default=5.0, help='Command duration in seconds (default: 5.0)')
    args = parser.parse_args()
    
    try:
        send_velocity_command(args.linear, args.angular, args.duration)
    except rospy.ROSInterruptException:
        pass 