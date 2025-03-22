#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
import time
import sys
import argparse

def send_velocity_command(pub, linear_x, angular_z, duration):
    """Send a velocity command for the specified duration"""
    cmd = Twist()
    cmd.linear.x = linear_x
    cmd.angular.z = angular_z
    
    start_time = time.time()
    rate = rospy.Rate(10)  # 10 Hz
    
    rospy.loginfo(f"Sending command: linear.x={linear_x:.2f}, angular.z={angular_z:.2f} for {duration:.1f} seconds")
    
    while time.time() - start_time < duration and not rospy.is_shutdown():
        pub.publish(cmd)
        rate.sleep()

def run_automatic_test():
    """Run a predefined test sequence"""
    rospy.loginfo("Running automatic test sequence")
    
    # Test 1: Walk forward
    send_velocity_command(pub, 0.2, 0.0, 10.0)
    
    # Test 2: Stop and stand
    send_velocity_command(pub, 0.0, 0.0, 3.0)
    
    # Test 3: Walk at slower speed
    send_velocity_command(pub, 0.1, 0.0, 5.0)
    
    # Test 4: Final stop
    send_velocity_command(pub, 0.0, 0.0, 2.0)
    
    rospy.loginfo("Test sequence completed")

def run_interactive_mode():
    """Run in interactive mode where user can enter commands"""
    rospy.loginfo("Interactive mode - enter commands manually")
    rospy.loginfo("Format: linear_x angular_z duration")
    rospy.loginfo("Example: 0.2 0.0 5.0 (forward at 0.2 m/s for 5 seconds)")
    rospy.loginfo("Enter 'q' to quit")
    
    while not rospy.is_shutdown():
        try:
            user_input = input("\nEnter command (linear_x angular_z duration) or 'q' to quit: ")
            
            if user_input.lower() == 'q':
                break
                
            # Parse input
            parts = user_input.split()
            if len(parts) != 3:
                rospy.logwarn("Invalid input. Please use format: linear_x angular_z duration")
                continue
                
            try:
                linear_x = float(parts[0])
                angular_z = float(parts[1])
                duration = float(parts[2])
                
                send_velocity_command(pub, linear_x, angular_z, duration)
            except ValueError:
                rospy.logwarn("Invalid numbers. Please enter numeric values.")
                
        except KeyboardInterrupt:
            break
    
    # Ensure robot stops before exiting
    send_velocity_command(pub, 0.0, 0.0, 1.0)
    rospy.loginfo("Interactive mode ended")

if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Test velocity-based walking')
    parser.add_argument('--mode', type=str, default='auto', choices=['auto', 'interactive'],
                      help='Test mode: auto (automatic sequence) or interactive')
    parser.add_argument('--linear', type=float, default=0.2,
                      help='Linear velocity for manual command (default: 0.2)')
    parser.add_argument('--angular', type=float, default=0.0,
                      help='Angular velocity for manual command (default: 0.0)')
    parser.add_argument('--duration', type=float, default=5.0,
                      help='Duration for manual command in seconds (default: 5.0)')
    args = parser.parse_args()
    
    # Initialize ROS node
    rospy.init_node('velocity_test', anonymous=True)
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    
    # Wait for publisher to connect
    rospy.loginfo("Waiting for connections...")
    while pub.get_num_connections() == 0 and not rospy.is_shutdown():
        rospy.sleep(0.1)
    
    rospy.loginfo("Publisher connected!")
    
    try:
        if args.mode == 'auto':
            run_automatic_test()
        elif args.mode == 'interactive':
            run_interactive_mode()
        else:
            # Single command mode
            send_velocity_command(pub, args.linear, args.angular, args.duration)
            # Stop after the command completes
            send_velocity_command(pub, 0.0, 0.0, 1.0)
    except rospy.ROSInterruptException:
        pass 