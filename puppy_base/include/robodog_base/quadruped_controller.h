#ifndef QUADRUPED_CONTROLLER_H
#define QUADRUPED_CONTROLLER_H

#include <ros/ros.h>
#include <geometry_msgs/Twist.h>
#include <sensor_msgs/JointState.h>
#include <robodog_msgs/Joints.h>
#include <robodog_msgs/Pose.h>
#include <robodog_msgs/Velocities.h>

namespace robodog_base
{
    class QuadrupedController
    {
        public:
            QuadrupedController(ros::NodeHandle &nh, ros::NodeHandle &pnh);
            ~QuadrupedController();

        private:
            void cmdVelCallback(const geometry_msgs::Twist::ConstPtr &msg);
            void jointStatesCallback(const sensor_msgs::JointState::ConstPtr &msg);
            void updateTimer(const ros::TimerEvent &event);

            ros::NodeHandle nh_;
            ros::NodeHandle pnh_;
            
            ros::Subscriber cmd_vel_sub_;
            ros::Subscriber joint_states_sub_;
            
            ros::Publisher joint_commands_pub_;
            ros::Publisher robot_pose_pub_;
            
            ros::Timer update_timer_;

            // Control parameters
            double update_rate_;
            std::vector<double> joint_positions_;
            geometry_msgs::Twist current_velocity_;
    };
}

#endif // QUADRUPED_CONTROLLER_H