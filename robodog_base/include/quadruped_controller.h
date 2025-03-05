#ifndef QUADRUPED_CONTROLLER_H
#define QUADRUPED_CONTROLLER_H

#include <ros/ros.h>
#include <geometry_msgs/Twist.h>
#include <geometry_msgs/Pose.h>
#include <sensor_msgs/JointState.h>
#include <trajectory_msgs/JointTrajectory.h>
#include <tf2/LinearMath/Quaternion.h>
#include <actuator.h>

namespace robodog
{
    class QuadrupedController
    {
        public:
            QuadrupedController(ros::NodeHandle *nh, ros::NodeHandle *pnh);

        private:
            void controlLoop_(const ros::TimerEvent& event);
            void cmdVelCallback_(const geometry_msgs::Twist::ConstPtr& msg);
            void cmdPoseCallback_(const geometry_msgs::Pose::ConstPtr& msg);
            void publishJointStates_();

            ros::NodeHandle* nh_;
            ros::NodeHandle* pnh_;
            
            ros::Subscriber cmd_vel_sub_;
            ros::Subscriber cmd_pose_sub_;
            ros::Publisher joint_states_pub_;
            
            ros::Timer control_timer_;
            
            double loop_rate_;
            std::vector<std::string> joint_names_;
            
            // Current state
            geometry_msgs::Twist current_velocity_;
            geometry_msgs::Pose current_pose_;
            std::vector<double> joint_positions_;
            
            // Hardware interface
            Actuator* actuator_;
            bool hardware_connected_;
            
            // Gait parameters
            double stance_height_;
            double swing_height_;
            double stance_duration_;
            double swing_duration_;
            
            // Motion limits
            double max_linear_velocity_x_;
            double max_linear_velocity_y_;
            double max_angular_velocity_z_;
    };
}

#endif