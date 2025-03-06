#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import PoseStamped
from gazebo_msgs.msg import ModelStates
from tf.transformations import euler_from_quaternion

class RobotPosePublisher:
    def __init__(self):
        rospy.init_node('robot_pose_publisher')
        
        # Publisher for robot pose
        self.pose_pub = rospy.Publisher('robot_pose', PoseStamped, queue_size=1)
        
        # Subscribe to Gazebo model states
        rospy.Subscriber('/gazebo/model_states', ModelStates, self.model_states_callback)
        
        self.robot_name = 'robodog'
        self.pose_msg = PoseStamped()
        self.pose_msg.header.frame_id = 'map'

    def model_states_callback(self, msg):
        try:
            idx = msg.name.index(self.robot_name)
        except ValueError:
            return

        self.pose_msg.header.stamp = rospy.Time.now()
        self.pose_msg.pose = msg.pose[idx]
        
        # Extract Euler angles for debugging
        orientation = msg.pose[idx].orientation
        (roll, pitch, yaw) = euler_from_quaternion([
            orientation.x, orientation.y, orientation.z, orientation.w])
        
        # Log pose information
        rospy.logdebug("Robot pose - Position: (%.2f, %.2f, %.2f) Orientation (RPY): (%.2f, %.2f, %.2f)",
                      msg.pose[idx].position.x,
                      msg.pose[idx].position.y,
                      msg.pose[idx].position.z,
                      roll, pitch, yaw)
        
        self.pose_pub.publish(self.pose_msg)

if __name__ == '__main__':
    try:
        pose_publisher = RobotPosePublisher()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass