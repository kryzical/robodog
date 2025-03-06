#include <robodog_base/message_relay.h>

namespace robodog_base
{
    MessageRelay::MessageRelay(ros::NodeHandle &nh, ros::NodeHandle &pnh)
        : nh_(nh), pnh_(pnh)
    {
        // Initialize joint names
        joint_names_ = {
            "lf_hip_joint", "lf_upper_leg_joint", "lf_lower_leg_joint",
            "rf_hip_joint", "rf_upper_leg_joint", "rf_lower_leg_joint",
            "lh_hip_joint", "lh_upper_leg_joint", "lh_lower_leg_joint",
            "rh_hip_joint", "rh_upper_leg_joint", "rh_lower_leg_joint"
        };

        // Initialize subscribers
        joint_states_sub_ = nh_.subscribe("joint_states_raw", 1, &MessageRelay::jointStatesCallback, this);
        joint_commands_sub_ = nh_.subscribe("joint_commands_raw", 1, &MessageRelay::jointCommandsCallback, this);
        contacts_sub_ = nh_.subscribe("contacts_raw", 1, &MessageRelay::contactsCallback, this);
        velocities_sub_ = nh_.subscribe("velocities_raw", 1, &MessageRelay::velocitiesCallback, this);

        // Initialize publishers
        joint_states_pub_ = nh_.advertise<sensor_msgs::JointState>("joint_states", 1);
        joint_commands_pub_ = nh_.advertise<robodog_msgs::Joints>("joint_commands", 1);
        contacts_pub_ = nh_.advertise<robodog_msgs::Contacts>("foot_contacts", 1);
        velocities_pub_ = nh_.advertise<robodog_msgs::Velocities>("velocities", 1);
    }

    MessageRelay::~MessageRelay()
    {
    }

    void MessageRelay::jointStatesCallback(const sensor_msgs::JointState::ConstPtr &msg)
    {
        sensor_msgs::JointState joint_states;
        joint_states.header = msg->header;
        joint_states.name = joint_names_;
        joint_states.position = msg->position;
        joint_states.velocity = msg->velocity;
        joint_states.effort = msg->effort;
        
        joint_states_pub_.publish(joint_states);
    }

    void MessageRelay::jointCommandsCallback(const robodog_msgs::Joints::ConstPtr &msg)
    {
        joint_commands_pub_.publish(*msg);
    }

    void MessageRelay::contactsCallback(const robodog_msgs::Contacts::ConstPtr &msg)
    {
        contacts_pub_.publish(*msg);
    }

    void MessageRelay::velocitiesCallback(const robodog_msgs::Velocities::ConstPtr &msg)
    {
        velocities_pub_.publish(*msg);
    }
}

int main(int argc, char** argv)
{
    ros::init(argc, argv, "message_relay");
    ros::NodeHandle nh;
    ros::NodeHandle pnh("~");

    robodog_base::MessageRelay message_relay(nh, pnh);
    ros::spin();

    return 0;
}