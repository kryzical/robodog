#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64
from time import sleep

# Initialize ROS node
rospy.init_node('walking_node')

# Publishers for each joint using controller names from launch file
pub_lf1 = rospy.Publisher('/puppy/joint2_position_controller/command', Float64, queue_size=10)
pub_lf2 = rospy.Publisher('/puppy/joint6_position_controller/command', Float64, queue_size=10)
pub_rf1 = rospy.Publisher('/puppy/joint1_position_controller/command', Float64, queue_size=10)
pub_rf2 = rospy.Publisher('/puppy/joint5_position_controller/command', Float64, queue_size=10)
pub_lr1 = rospy.Publisher('/puppy/joint4_position_controller/command', Float64, queue_size=10)
pub_lr2 = rospy.Publisher('/puppy/joint8_position_controller/command', Float64, queue_size=10)
pub_rr1 = rospy.Publisher('/puppy/joint3_position_controller/command', Float64, queue_size=10)
pub_rr2 = rospy.Publisher('/puppy/joint7_position_controller/command', Float64, queue_size=10)

# Function to publish joint angles
def publish_joint_angles(lf1, lf2, rf1, rf2, lr1, lr2, rr1, rr2):
    pub_lf1.publish(lf1)
    pub_lf2.publish(lf2)
    pub_rf1.publish(rf1)
    pub_rf2.publish(rf2)
    pub_lr1.publish(lr1)
    pub_lr2.publish(lr2)
    pub_rr1.publish(rr1)
    pub_rr2.publish(rr2)

# Improved walking sequence
# Define a more realistic walking sequence with better synchronization
# Each step consists of lifting, moving forward, and placing down the legs

def improved_trot():
    steps = [
        # Step 1: Lift front right and back left legs
        (1.0, 1.0, 0.5, 0.5, 1.0, 1.0, 0.5, 0.5),
        # Step 2: Move front right and back left legs forward
        (1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0),
        # Step 3: Place front right and back left legs down
        (1.0, 1.0, 1.5, 1.5, 1.0, 1.0, 1.5, 1.5),
        # Step 4: Lift front left and back right legs
        (0.5, 0.5, 1.5, 1.5, 0.5, 0.5, 1.5, 1.5),
        # Step 5: Move front left and back right legs forward
        (1.0, 1.0, 1.5, 1.5, 1.0, 1.0, 1.5, 1.5),
        # Step 6: Place front left and back right legs down
        (1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5)
    ]
    for step in steps:
        publish_joint_angles(*step)
        sleep(0.5)

# Improved stand function
# Ensure the robot is in a stable standing position before starting to walk

def improved_stand():
    publish_joint_angles(1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0)
    sleep(1)

# Main function

def main():
    rospy.sleep(1)  # Wait for ROS to initialize
    improved_stand()
    while not rospy.is_shutdown():
        improved_trot()

if __name__ == "__main__":
    main()