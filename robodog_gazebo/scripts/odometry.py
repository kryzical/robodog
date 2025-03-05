#!/usr/bin/env python3

import rospy
from nav_msgs.msg import Odometry
from gazebo_msgs.msg import ModelStates
from geometry_msgs.msg import TransformStamped, Twist
import tf2_ros

class OdometryComputation:
    def __init__(self):
        rospy.init_node('odometry_computation')
        
        # Publisher for odometry data
        self.odom_pub = rospy.Publisher('odom', Odometry, queue_size=1)
        
        # Subscribe to Gazebo model states
        rospy.Subscriber('/gazebo/model_states', ModelStates, self.model_states_callback)
        
        self.robot_name = 'robodog'
        self.odom_msg = Odometry()
        self.odom_msg.header.frame_id = 'odom'
        self.odom_msg.child_frame_id = 'base_link'
        
        # Set up TF broadcaster
        self.tf_broadcaster = tf2_ros.TransformBroadcaster()
        self.transform_stamped = TransformStamped()
        self.transform_stamped.header.frame_id = 'odom'
        self.transform_stamped.child_frame_id = 'base_link'

    def model_states_callback(self, msg):
        try:
            idx = msg.name.index(self.robot_name)
        except ValueError:
            return

        current_time = rospy.Time.now()
        
        # Set header
        self.odom_msg.header.stamp = current_time
        
        # Set pose
        self.odom_msg.pose.pose = msg.pose[idx]
        
        # Set twist
        self.odom_msg.twist.twist = msg.twist[idx]
        
        # Publish odometry message
        self.odom_pub.publish(self.odom_msg)
        
        # Broadcast transform
        self.transform_stamped.header.stamp = current_time
        self.transform_stamped.transform.translation.x = msg.pose[idx].position.x
        self.transform_stamped.transform.translation.y = msg.pose[idx].position.y
        self.transform_stamped.transform.translation.z = msg.pose[idx].position.z
        self.transform_stamped.transform.rotation = msg.pose[idx].orientation
        
        self.tf_broadcaster.sendTransform(self.transform_stamped)

if __name__ == '__main__':
    try:
        odometry = OdometryComputation()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass