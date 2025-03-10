#include "quadruped_controller.h"
#include "puppy_config/gait_config.h"

namespace robodog
{
    QuadrupedController::QuadrupedController(ros::NodeHandle *nh, ros::NodeHandle *pnh):
        nh_(nh),
        pnh_(pnh)
    {
        // Load parameters
        pnh_->param<double>("loop_rate", loop_rate_, 100.0);
        pnh_->param<bool>("hardware_connected", hardware_connected_, false);
        
        // Use centralized gait parameters
        stance_height_ = GAIT_CONFIG_NOMINAL_HEIGHT;
        swing_height_ = GAIT_CONFIG_SWING_HEIGHT;
        stance_duration_ = GAIT_CONFIG_STANCE_DURATION;
        swing_duration_ = GAIT_CONFIG_SWING_DURATION;
        max_linear_velocity_x_ = GAIT_CONFIG_MAX_LINEAR_VEL_X;
        max_linear_velocity_y_ = GAIT_CONFIG_MAX_LINEAR_VEL_Y;
        max_angular_velocity_z_ = GAIT_CONFIG_MAX_ANGULAR_VEL_Z;
        
        // Initialize hardware interface
        if (hardware_connected_) {
            actuator_ = new ServoActuator();
        } else {
            actuator_ = new SimulationActuator();
        }
        actuator_->init();
        
        // Setup ROS communication
        cmd_vel_sub_ = nh_->subscribe("cmd_vel", 1, &QuadrupedController::cmdVelCallback_, this);
        cmd_pose_sub_ = nh_->subscribe("body_pose", 1, &QuadrupedController::cmdPoseCallback_, this);
        joint_states_pub_ = nh_->advertise<sensor_msgs::JointState>("joint_states", 1);
        
        // Initialize control loop
        control_timer_ = pnh_->createTimer(ros::Duration(1.0/loop_rate_),
                                         &QuadrupedController::controlLoop_,
                                         this);
    }

    void QuadrupedController::controlLoop_(const ros::TimerEvent& event)
    {
        // TODO: Implement gait generation and leg motion control
        // For now, just publish current joint states
        publishJointStates_();
    }

    void QuadrupedController::cmdVelCallback_(const geometry_msgs::Twist::ConstPtr& msg)
    {
        // Store commanded velocity
        current_velocity_ = *msg;
        
        // Apply velocity limits
        current_velocity_.linear.x = std::min(std::max(current_velocity_.linear.x, 
            -max_linear_velocity_x_), max_linear_velocity_x_);
        current_velocity_.linear.y = std::min(std::max(current_velocity_.linear.y, 
            -max_linear_velocity_y_), max_linear_velocity_y_);
        current_velocity_.angular.z = std::min(std::max(current_velocity_.angular.z, 
            -max_angular_velocity_z_), max_angular_velocity_z_);
    }

    void QuadrupedController::cmdPoseCallback_(const geometry_msgs::Pose::ConstPtr& msg)
    {
        current_pose_ = *msg;
    }

    void QuadrupedController::publishJointStates_()
    {
        sensor_msgs::JointState joint_state_msg;
        joint_state_msg.header.stamp = ros::Time::now();
        joint_state_msg.name = joint_names_;
        joint_state_msg.position = joint_positions_;
        joint_states_pub_.publish(joint_state_msg);
    }
}

int main(int argc, char** argv)
{
    ros::init(argc, argv, "quadruped_controller");
    ros::NodeHandle nh("");
    ros::NodeHandle pnh("~");
    
    robodog::QuadrupedController controller(&nh, &pnh);
    
    ros::spin();
    return 0;
}