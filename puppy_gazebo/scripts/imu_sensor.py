#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Imu
from gazebo_msgs.msg import ModelStates
from tf.transformations import euler_from_quaternion
import numpy as np

class IMUSensor:
    def __init__(self):
        rospy.init_node('imu_sensor')
        
        # Publisher for IMU data
        self.imu_pub = rospy.Publisher('imu/data', Imu, queue_size=1)
        
        # Subscribe to Gazebo model states
        rospy.Subscriber('/gazebo/model_states', ModelStates, self.model_states_callback)
        
        self.robot_name = 'robodog'
        self.imu_msg = Imu()
        self.imu_msg.header.frame_id = 'imu_link'
        
        # Set covariance matrices
        self.imu_msg.orientation_covariance = [0.0001, 0, 0,
                                             0, 0.0001, 0,
                                             0, 0, 0.0001]
        
        self.imu_msg.angular_velocity_covariance = [0.0001, 0, 0,
                                                   0, 0.0001, 0,
                                                   0, 0, 0.0001]
        
        self.imu_msg.linear_acceleration_covariance = [0.0001, 0, 0,
                                                      0, 0.0001, 0,
                                                      0, 0, 0.0001]
        
        self.prev_time = rospy.Time.now()
        self.prev_angular_vel = [0, 0, 0]

    def model_states_callback(self, msg):
        try:
            idx = msg.name.index(self.robot_name)
        except ValueError:
            return

        current_time = rospy.Time.now()
        dt = (current_time - self.prev_time).to_sec()
        
        # Get orientation
        self.imu_msg.orientation = msg.pose[idx].orientation
        
        # Calculate angular velocity
        roll, pitch, yaw = euler_from_quaternion([msg.pose[idx].orientation.x,
                                                msg.pose[idx].orientation.y,
                                                msg.pose[idx].orientation.z,
                                                msg.pose[idx].orientation.w])
        
        angular_vel = msg.twist[idx].angular
        self.imu_msg.angular_velocity = angular_vel
        
        # Calculate linear acceleration
        linear_vel = msg.twist[idx].linear
        g = 9.81  # gravity
        
        # Add some noise to make it more realistic
        noise_std = 0.01
        acc_noise = np.random.normal(0, noise_std, 3)
        
        self.imu_msg.linear_acceleration.x = linear_vel.x / dt + acc_noise[0]
        self.imu_msg.linear_acceleration.y = linear_vel.y / dt + acc_noise[1]
        self.imu_msg.linear_acceleration.z = linear_vel.z / dt + g + acc_noise[2]
        
        self.imu_msg.header.stamp = current_time
        self.imu_pub.publish(self.imu_msg)
        
        self.prev_time = current_time
        self.prev_angular_vel = [angular_vel.x, angular_vel.y, angular_vel.z]

if __name__ == '__main__':
    try:
        imu_sensor = IMUSensor()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass