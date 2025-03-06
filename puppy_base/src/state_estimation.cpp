#include <robodog_base/state_estimation.h>

namespace robodog_base
{
    StateEstimation::StateEstimation(ros::NodeHandle &nh, ros::NodeHandle &pnh)
        : nh_(nh), pnh_(pnh)
    {
        // Get parameters
        pnh_.param("update_rate", update_rate_, 50.0);

        // Initialize subscribers
        imu_sub_ = nh_.subscribe("imu/data", 1, &StateEstimation::imuCallback, this);
        contacts_sub_ = nh_.subscribe("foot_contacts", 1, &StateEstimation::contactsCallback, this);
        pose_sub_ = nh_.subscribe("robot_pose", 1, &StateEstimation::poseCallback, this);

        // Initialize publishers
        odom_pub_ = nh_.advertise<nav_msgs::Odometry>("odom", 1);

        // Initialize timer
        update_timer_ = nh_.createTimer(ros::Duration(1.0/update_rate_), 
                                      &StateEstimation::updateOdometry, this);

        // Initialize odometry message
        current_odom_.header.frame_id = "odom";
        current_odom_.child_frame_id = "base_link";
    }

    StateEstimation::~StateEstimation()
    {
    }

    void StateEstimation::imuCallback(const sensor_msgs::Imu::ConstPtr &msg)
    {
        current_imu_ = *msg;
    }

    void StateEstimation::contactsCallback(const robodog_msgs::Contacts::ConstPtr &msg)
    {
        foot_contacts_ = *msg;
    }

    void StateEstimation::poseCallback(const robodog_msgs::Pose::ConstPtr &msg)
    {
        // Update odometry position based on robot pose
        current_odom_.pose.pose.position.x = msg->x;
        current_odom_.pose.pose.position.y = msg->y;
        current_odom_.pose.pose.position.z = msg->z;
        
        // TODO: Convert roll, pitch, yaw to quaternion
    }

    void StateEstimation::updateOdometry(const ros::TimerEvent &event)
    {
        current_odom_.header.stamp = ros::Time::now();
        
        // TODO: Implement proper state estimation using IMU and leg odometry
        
        // Publish odometry message
        odom_pub_.publish(current_odom_);

        // Broadcast transform
        geometry_msgs::TransformStamped odom_trans;
        odom_trans.header = current_odom_.header;
        odom_trans.child_frame_id = current_odom_.child_frame_id;
        odom_trans.transform.translation.x = current_odom_.pose.pose.position.x;
        odom_trans.transform.translation.y = current_odom_.pose.pose.position.y;
        odom_trans.transform.translation.z = current_odom_.pose.pose.position.z;
        odom_trans.transform.rotation = current_odom_.pose.pose.orientation;

        tf_broadcaster_.sendTransform(odom_trans);
    }
}

int main(int argc, char** argv)
{
    ros::init(argc, argv, "state_estimation");
    ros::NodeHandle nh;
    ros::NodeHandle pnh("~");

    robodog_base::StateEstimation state_estimation(nh, pnh);
    ros::spin();

    return 0;
}