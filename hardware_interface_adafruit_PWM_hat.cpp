//add includes from packages----------------

//-----------terminology------------------
//  callback - functions that are automatically called by the system when an event happens (a call and response)
//  state transition - the process of moving from one state to another (for example, from inactive to active)
//        example when system moves from intializtion to configuration
//-----------NOTES------------------
//  the lifecycle which includes state transitions and callbacks are important because the purpose of using ros control is to control when to establish connections, communication, power, etc 
//---------------------------------------------------


namespace custom_hardware{
    //this is the init function for the CustomHardwareInterfaceAdafruitPWMHat class, this fucntion intializes all member variables and process parameters from info argument
    //basically a callback called by the system to initialize motors and sensors
    hardware_interface::CallbackReturn CustomHardwareInterfaceAdafruitPWMHat::on_init(const hardware_interface::HardwareInfo & info){
        //statement calls parent class to intialize basic variables, if there is something wronge then EROOR is returned, (ERROR is property that is understood within the hardware_interface parent class)
        if(hardware_interface::SystemInterface::on_init(info) != hardware_interface::CallbackReturn::SUCESS){
            return hardware_interface::CallbackReturn::ERROR;
        }

        //statements below set the sizes of the vectors (state, position, command) to the number of joints the robot has
        hw_states_position_.resize(info_.joints.size(), std::numeric_limits<double>quiet_NaN());
        hw_states_velocity_.resize(info_.joints.size(), std::numeric_limits<double>quiet_NaN());
        hw_commands_.resize(info_.joints.size(), std::numeric_limits<double>quiet_NaN());

        //for loop will iterate though all the joint to make sure parameters are set correctly
        for (const hardware_interface::ComponentInfo & joint : info_.joints){
            //statement will make sure that each joint will only except 1 type of command
            if(joint.command_interface.size() != 1){
                RCLCPP_FATAL(rclcpp::get_logger("HardwareInterface"), "Joint '%s' has %zu command interfaces found. 1 excepted", joint.name.c_str(), joint.command_interfaces.size());
                return hardware_interface::CallbackReturn::ERROR;
            }

            if(joint.command_interfaces[0].name != hardware_interface::HW_IF_POSITION){
                RCLCPP_FATAL(rclcpp::get_logger("UnrealInterface"), "Joint '%s' have '%s' command interfaces found. '%s' expected.", joint.name.c_str(), joint.command_interfaces[0].name.c_str(), hardware_interface::HW_IF_POSITION);
                return hardware_interface::CallbackReturn::ERROR;
            }

            if(joint.state_interfaces.size() != 2){
                RCLCPP_FATAL(rclcpp::get_logger("HardwareInterface"), "Joint '%s' has %zu command interfaces found. 2 excepted", joint.name.c_str(), joint.state_interfaces.size());
                return hardware_interface::CallbackReturn::ERROR;
            }

            if(joint.state_interfaces[0].name != hardware_interface::HW_IF_POSITION){
                RCLCPP_FATAL(rclcpp::get_logger("UnrealInterface"), "Joint '%s' have '%s' command interfaces found. '%s' expected.", joint.name.c_str(), joint.command_interfaces[0].name.c_str(), hardware_interface::HW_IF_POSITION);
                return hardware_interface::CallbackReturn::ERROR;
            }

            if(joint.state_interfaces[0].name != hardware_interface::HW_IF_VELOCITY){
                RCLCPP_FATAL(rclcpp::get_logger("UnrealInterface"), "Joint '%s' have '%s' state interfaces. '%s' expected.", joint.name.c_str(), joint.command_interfaces[0].name.c_str(), hardware_interface::HW_IF_POSITION);
                return hardware_interface::CallbackReturn::ERROR;
            }
        }
        return hardware_interface::CallbackReturn::SUCCESS;
    }


    //callback function that will execute when the on_init function is done and sucessful 
    //configures / collaborates vector state elements
    hardware_interface::CallbackReturn CustomHardwareInterfaceAdafruitPWMHat::on_configure(const rclcpp_lifecycle::State & previous_state){
        //iterates through motor vectors and intializes every value within to 0
        for (uint i = 0; i < hw_states_position_.size(); i++){
            hw_states_position_[i] = 0;
            hw_state_velocity_[i] = 0;
            hw_commands_[i] = 0;
        }

        RCLCPP_INFO(rclcpp::get_logger("HardwareInterface"), "Sucessfully configured!")

        return hardware_interface::CallbackReturn::SUCESS;
    }

    //callback function that exectues when state trasition occurs when on_configure is done and sucessful
    hardware_interface::CallbackReturn CustomHardwareInterfaceAdafruitPWMHat::on_activate(const rclcpp_lifecycle::State & previous_state){

    }

    hardware_interface::CallbackReturn CustomHardwareInterfaceAdafruitPWMHat::on_deactivate(const rclcpp_lifecycle::State & previous_state){

    }
}