#ifndef STATE_ESTIMATION_H
#define STATE_ESTIMATION_H

#include <ros/ros.h>
#include <nav_msgs/Odometry.h>
#include <sensor_msgs/Imu.h>
#include <tf2_ros/transform_broadcaster.h>
#include <robodog_msgs/Contacts.h>
#include <robodog_msgs/Pose.h>

namespace robodog_base
{
    class StateEstimation
    {
        public:
            StateEstimation(ros::NodeHandle &nh, ros::NodeHandle &pnh);
            ~StateEstimation();

        private:
            void imuCallback(const sensor_msgs::Imu::ConstPtr &msg);
            void contactsCallback(const robodog_msgs::Contacts::ConstPtr &msg);
            void poseCallback(const robodog_msgs::Pose::ConstPtr &msg);
            void updateOdometry(const ros::TimerEvent &event);

            ros::NodeHandle nh_;
            ros::NodeHandle pnh_;
            
            ros::Subscriber imu_sub_;
            ros::Subscriber contacts_sub_;
            ros::Subscriber pose_sub_;
            
            ros::Publisher odom_pub_;
            
            ros::Timer update_timer_;
            tf2_ros::TransformBroadcaster tf_broadcaster_;

            // State variables
            nav_msgs::Odometry current_odom_;
            sensor_msgs::Imu current_imu_;
            robodog_msgs::Contacts foot_contacts_;
            double update_rate_;
    };
}

#endif // STATE_ESTIMATION_H