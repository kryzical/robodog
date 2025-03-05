#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import JointState
from robodog_msgs.msg import Contacts
import math
import time

class TestMovement:
    def __init__(self):
        rospy.init_node('test_movement')
        
        # Publishers
        self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
        
        # Subscribers
        rospy.Subscriber('joint_states', JointState, self.joint_states_callback)
        rospy.Subscriber('foot_contacts', Contacts, self.contacts_callback)
        
        self.joint_states = None
        self.foot_contacts = None
        self.test_sequence_running = False
    
    def joint_states_callback(self, msg):
        self.joint_states = msg
    
    def contacts_callback(self, msg):
        self.foot_contacts = msg
    
    def publish_cmd_vel(self, linear_x, angular_z, duration):
        msg = Twist()
        msg.linear.x = linear_x
        msg.angular.z = angular_z
        
        start_time = time.time()
        rate = rospy.Rate(10)  # 10Hz
        
        while time.time() - start_time < duration and not rospy.is_shutdown():
            self.cmd_vel_pub.publish(msg)
            rate.sleep()
    
    def run_test_sequence(self):
        if self.test_sequence_running:
            return
            
        self.test_sequence_running = True
        rospy.loginfo("Starting movement test sequence...")
        
        # Wait for all subscribers to be ready
        rospy.sleep(2.0)
        
        # Test 1: Forward movement
        rospy.loginfo("Test 1: Moving forward...")
        self.publish_cmd_vel(0.2, 0.0, 3.0)
        rospy.sleep(1.0)
        
        # Test 2: Rotation in place
        rospy.loginfo("Test 2: Rotating in place...")
        self.publish_cmd_vel(0.0, 0.5, 3.0)
        rospy.sleep(1.0)
        
        # Test 3: Combined movement
        rospy.loginfo("Test 3: Combined movement...")
        self.publish_cmd_vel(0.1, 0.2, 3.0)
        rospy.sleep(1.0)
        
        # Stop all movement
        self.publish_cmd_vel(0.0, 0.0, 0.1)
        
        rospy.loginfo("Test sequence completed!")
        self.test_sequence_running = False

if __name__ == '__main__':
    try:
        test = TestMovement()
        rospy.sleep(5)  # Wait for Gazebo to fully initialize
        test.run_test_sequence()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass