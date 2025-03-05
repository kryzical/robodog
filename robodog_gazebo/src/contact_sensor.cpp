#include <gazebo/gazebo.hh>
#include <gazebo/physics/physics.hh>
#include <gazebo/common/common.hh>
#include <ros/ros.h>
#include <robodog_msgs/Contacts.h>

namespace gazebo
{
    class ContactSensor : public ModelPlugin
    {
        public:
            ContactSensor() : ModelPlugin() {}

            void Load(physics::ModelPtr _model, sdf::ElementPtr _sdf)
            {
                // Store the model pointer
                model_ = _model;

                // Initialize ROS node
                if (!ros::isInitialized())
                {
                    int argc = 0;
                    char **argv = NULL;
                    ros::init(argc, argv, "contact_sensor",
                            ros::init_options::NoSigintHandler);
                }
                
                rosnode_.reset(new ros::NodeHandle("contact_sensor"));
                contact_pub_ = rosnode_->advertise<robodog_msgs::Contacts>("foot_contacts", 1);

                // Get foot link names
                foot_links_.push_back("lf_foot_link");
                foot_links_.push_back("rf_foot_link");
                foot_links_.push_back("lh_foot_link");
                foot_links_.push_back("rh_foot_link");

                // Connect to world update event
                updateConnection_ = event::Events::ConnectWorldUpdateBegin(
                    boost::bind(&ContactSensor::OnUpdate, this, _1));

                ROS_INFO("Contact sensor plugin initialized");
            }

            void OnUpdate(const common::UpdateInfo &)
            {
                robodog_msgs::Contacts contact_msg;
                contact_msg.contacts.resize(4);

                for (size_t i = 0; i < foot_links_.size(); ++i)
                {
                    physics::LinkPtr foot = model_->GetLink(foot_links_[i]);
                    if (foot)
                    {
                        // Check if foot is in contact with ground
                        contact_msg.contacts[i] = foot->GetWorldPose().pos.z < 0.01;
                    }
                }

                contact_pub_.publish(contact_msg);
            }

        private:
            physics::ModelPtr model_;
            std::unique_ptr<ros::NodeHandle> rosnode_;
            ros::Publisher contact_pub_;
            event::ConnectionPtr updateConnection_;
            std::vector<std::string> foot_links_;
    };

    GZ_REGISTER_MODEL_PLUGIN(ContactSensor)
}