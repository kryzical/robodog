import rospy
from std_msgs.msg import Float64
from time import sleep

# Initialize ROS node
rospy.init_node('walking_node')

# Publishers for each joint
pub_lf1 = rospy.Publisher('/puppy/lf1_position_controller/command', Float64, queue_size=10)
pub_lf2 = rospy.Publisher('/puppy/lf2_position_controller/command', Float64, queue_size=10)
pub_rf1 = rospy.Publisher('/puppy/rf1_position_controller/command', Float64, queue_size=10)
pub_rf2 = rospy.Publisher('/puppy/rf2_position_controller/command', Float64, queue_size=10)
pub_lr1 = rospy.Publisher('/puppy/lr1_position_controller/command', Float64, queue_size=10)
pub_lr2 = rospy.Publisher('/puppy/lr2_position_controller/command', Float64, queue_size=10)
pub_rr1 = rospy.Publisher('/puppy/rr1_position_controller/command', Float64, queue_size=10)
pub_rr2 = rospy.Publisher('/puppy/rr2_position_controller/command', Float64, queue_size=10)

def publish_joint_angles(lf1, lf2, rf1, rf2, lr1, lr2, rr1, rr2):
    pub_lf1.publish(lf1)
    pub_lf2.publish(lf2)
    pub_rf1.publish(rf1)
    pub_rf2.publish(rf2)
    pub_lr1.publish(lr1)
    pub_lr2.publish(lr2)
    pub_rr1.publish(rr1)
    pub_rr2.publish(rr2)

def trot():
    for i in range(10):
        # Move joints to simulate walking
        publish_joint_angles(1.47, 1.04, 0.33, 0.76, 1.47, 1.04, 0.33, 0.76)
        sleep(0.1)
        publish_joint_angles(1.37, 1.34, 0.43, 0.76, 1.37, 1.34, 0.43, 0.76)
        sleep(0.1)
        publish_joint_angles(1.04, 1.04, 0.76, 0.76, 1.04, 1.04, 0.76, 0.76)
        sleep(0.1)

def stand():
    publish_joint_angles(1.47, 1.04, 0.33, 0.76, 1.47, 1.04, 0.33, 0.76)
    sleep(0.1)

def main():
    rospy.sleep(1)  # Wait for ROS to initialize
    stand()
    trot()

if __name__ == "__main__":
    main()