#!/usr/bin/env python3
"""
Test controller for the puppy robot.
Runs a sequence of movement tests to verify robot functionality.
"""

import rospy
import math
import time
from std_msgs.msg import Float64
from geometry_msgs.msg import Twist
from visualization_msgs.msg import Marker, MarkerArray
from robot_controller_lib import PuppyJointController

class TestController(PuppyJointController):
    def __init__(self):
        """Initialize the test controller"""
        super().__init__(node_name='test_controller')
        
        # Publisher for robot commands
        self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
        
        # Debug visualization
        self.marker_pub = rospy.Publisher('debug_markers', MarkerArray, queue_size=1)
        
        # Test sequence state
        self.test_running = False
        
    def publish_cmd_vel(self, linear_x, angular_z, duration):
        """Publish velocity command for a specified duration"""
        msg = Twist()
        msg.linear.x = linear_x
        msg.angular.z = angular_z
        
        start_time = time.time()
        rate = rospy.Rate(10)
        
        while time.time() - start_time < duration and not rospy.is_shutdown():
            self.cmd_vel_pub.publish(msg)
            rate.sleep()
            
        # Stop motion
        msg.linear.x = 0
        msg.angular.z = 0
        self.cmd_vel_pub.publish(msg)

    def publish_debug_markers(self, positions):
        """Publish debug visualization markers"""
        marker_array = MarkerArray()
        
        for i, (x, y, z) in enumerate(positions):
            marker = Marker()
            marker.header.frame_id = "base_link"
            marker.type = Marker.SPHERE
            marker.action = Marker.ADD
            marker.scale.x = marker.scale.y = marker.scale.z = 0.03
            marker.color.a = 1.0
            marker.color.r = 1.0
            marker.pose.position.x = x
            marker.pose.position.y = y
            marker.pose.position.z = z
            marker.id = i
            marker_array.markers.append(marker)
            
        self.marker_pub.publish(marker_array)

    def run_test_sequence(self):
        """Run a series of movement tests"""
        if self.test_running:
            return
            
        self.test_running = True
        rospy.loginfo("Starting test sequence...")
        
        # Make sure the robot is in a stable position first
        self.reset_pose()
        rospy.sleep(1.0)
        
        # Put robot in standing position before tests
        x = -0.08
        y = 0
        z = -0.12
        
        front_hip, front_knee = self.calculate_leg_ik(x, y, z, is_front=True)
        back_hip, back_knee = self.calculate_leg_ik(x, y, z, is_front=False)
        
        standing_positions = {
            'rf_hip': front_hip, 'rf_knee': front_knee,
            'lf_hip': front_hip, 'lf_knee': front_knee,
            'rb_hip': back_hip, 'rb_knee': back_knee,
            'lb_hip': back_hip, 'lb_knee': back_knee
        }
        
        # Move to standing position
        self.send_joint_commands(standing_positions)
        rospy.sleep(2.0)
        
        # Test 1: Forward motion
        rospy.loginfo("Test 1: Moving forward...")
        self.publish_cmd_vel(0.2, 0.0, 3.0)
        rospy.sleep(1.0)
        
        # Test 2: Rotation
        rospy.loginfo("Test 2: Rotating...")
        self.publish_cmd_vel(0.0, 0.5, 3.0)
        rospy.sleep(1.0)
        
        # Test 3: Combined motion
        rospy.loginfo("Test 3: Combined movement...")
        self.publish_cmd_vel(0.1, 0.2, 3.0)
        rospy.sleep(1.0)
        
        # Test 4: Stop and stabilize
        rospy.loginfo("Test 4: Testing stability...")
        self.publish_cmd_vel(0.0, 0.0, 2.0)
        # Return to stable standing position
        self.send_joint_commands(standing_positions)
        
        rospy.loginfo("Test sequence completed!")
        self.test_running = False

    def run(self):
        """Main run loop"""
        rospy.sleep(2.0)  # Wait for everything to initialize
        
        try:
            self.run_test_sequence()
            rospy.spin()
        except rospy.ROSInterruptException:
            pass

if __name__ == '__main__':
    controller = TestController()
    controller.run()