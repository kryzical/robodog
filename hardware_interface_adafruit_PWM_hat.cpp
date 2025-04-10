//add includes from packages----------------

//-----------terminology------------------
//  callback - functions that are automatically called by the system when an event happens (a call and response)
//  state transition - the process of moving from one state to another (for example, from inactive to active)
//        example when system moves from intializtion to configuration
//-----------NOTES------------------
//  the lifecycle which includes state transitions and callbacks are important because the purpose of using ros control is to control when to establish connections, communication, power, etc 
//----------------Next steps---------------------------
//  we will need to write xml file and in the urd include the hardware interface in the ros2control tags
//  we need to build the package and make sure things are working correctly
//  in the video, he writes code to have serial communciation with the arduno board, in our case we will nned to write code for adafruit


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
        //this function is used to actiave certain hardware when an ecent happens, this function can be used with setting up the camera or something else
        return hardware_interface::CallbackReturn::SUCESS;
    }

    hardware_interface::CallbackReturn CustomHardwareInterfaceAdafruitPWMHat::on_deactivate(const rclcpp_lifecycle::State & previous_state){
        //this is the opposite action for on_activate, it will just stop the activity that was triggered
        return hardware_interface::CallbackReturn::SUCESS;
    }
    //function basically as it says exports state interfaces, where the state interfaces is states of each joint and other information regarinding to that
    std::vector<hardware_interface::StateInterface> CustomHardwareInterfaceAdafruitPWMHat::export_state_interfaces(){
        std::cvector<hardware_interface::StateInterface> state_interfaces;
        for(uint i = 0; i < info_.joints.size(); i++){
            state_interfaces.emplace_back(hardware_interface::StateInterface(into_.joints[i].name, hardware_interface::HW_IF_POSITION, &hw_states_position_[i]));
            state_interfaces.emplace_back(hardware_interface::StateInterface(info_.joints[i].name, hardware_interface::HW_IF_VELOCITY, &hw_states_velocity_[i]));
        }
        return state_interfaces;
    }

    //function basically as it says exports command interfaces
    std::vector<hardware_interface::CommandInterface> CustomHardwareInterfaceAdafruitPWMHat::export_command_interfaces(){
        std::vector<hardware_interface::CommandInterface> command_interfaces;
        for(uint i = 0; i < info_.joints.size(); i++){
            command_interfaces.emplace_back(hardware_interface::CommandInterface(info_.joints[i].name, hardware_interface::HW_IF_POSITION, &hw_commands_[i]));
        }
        return command_interfaces;
    }

    //the function will read position of each servo motor, we will probably have to write a seperate file using adafruit library 
    hardware_interface::return_type CustomHardwareInterfaceAdafruitPWMHat::read(const rclcpp::Time & time, const rclcpp::Duration & period){
        //Code in here will probably be fully custom, we will need to create a c++ file including adafruit library that connect sto motors,
        //we will use said file to read te states of each servo motor
        return hardware_interface::return_type::OK;
    }

    //same as above but will be writing to the motors
    hardware_interface::return_type CustomHardwareInterfaceAdafruitPWMHat::write(const rclcpp::Time & time, const rclcpp::Duration & period){
        //Same as read function, we will have the file that connects to the servo motors but this function will send states to write to the serv
        //motors
        return hardware_interface::return_type::OK;
    }
}
