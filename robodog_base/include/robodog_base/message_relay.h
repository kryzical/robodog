#ifndef MESSAGE_RELAY_H
#define MESSAGE_RELAY_H

#include <ros/ros.h>
#include <sensor_msgs/JointState.h>
#include <robodog_msgs/Joints.h>
#include <robodog_msgs/Contacts.h>
#include <robodog_msgs/Velocities.h>

namespace robodog_base
{
    class MessageRelay
    {
        public:
            MessageRelay(ros::NodeHandle &nh, ros::NodeHandle &pnh);
            ~MessageRelay();

        private:
            void jointStatesCallback(const sensor_msgs::JointState::ConstPtr &msg);
            void jointCommandsCallback(const robodog_msgs::Joints::ConstPtr &msg);
            void contactsCallback(const robodog_msgs::Contacts::ConstPtr &msg);
            void velocitiesCallback(const robodog_msgs::Velocities::ConstPtr &msg);

            ros::NodeHandle nh_;
            ros::NodeHandle pnh_;
            
            ros::Subscriber joint_states_sub_;
            ros::Subscriber joint_commands_sub_;
            ros::Subscriber contacts_sub_;
            ros::Subscriber velocities_sub_;
            
            ros::Publisher joint_states_pub_;
            ros::Publisher joint_commands_pub_;
            ros::Publisher contacts_pub_;
            ros::Publisher velocities_pub_;
            
            std::vector<std::string> joint_names_;
    };
}

#endif // MESSAGE_RELAY_H