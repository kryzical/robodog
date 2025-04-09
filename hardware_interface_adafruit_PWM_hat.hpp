#ifndef CUSTOM_HARDWARE_INTERFACE_ADAFRUIT_PWM_HAT_HPP
#define CUSTOM_HARDWARE_INTERFACE_ADAFRUIT_PWM_HAT_HPP

#include "hardware_interface?handle.hpp"
#include "hardware_interface/hardware_info.hpp"
#include "hardware_interface/system_interface.hpp"
#include "hardware_interface/types/hardware_interface_return_values.hpp"
#include "rclpp/rclcpp.hpp"
#include "rclcpp/macros.hpp"
#include "rclcpp_lifecycle/node_interfaces/lifecycle_node_interface.hpp"
#include "rclcpp_lifecycle/state.hpp"
#include "custom_hardware/visibility_control.hpp"

namespace custom_hardware{
    class CustomHardwareInterfaceAdafruitPWMHat : public hardware_interface::SystemInterface{
        public:
            RCLCPP_SHARED_PTR_DEFINITIONS(CustomHardwareInterfaceAdafruitPWMHat)

            //the below function basically initializes the hardware interface and make sure that parameters are correct

            CUSTOM_HARDWARE_PUBLIC
            hardware_interface::CallbackReturn on_init(const hardware_interface::HardwareInfo & info) override;

            CUSTOM_HARDWARE_PUBLIC
            hardware_interface::CallbackReturn on_configure(const rclcpp_lifecycle::State & previous_state) override;

            CUSTOM_HARDWARE_PUBLIC
            std::vector<hardware_interface::StateInterface> export_state_interfaces() override;

            CUSTOM_HARDWARE_PUBLIC
            std::vector<hardware_interface::CommandInterface> export_command_interfaces() override;

            CUSTOM_HARDWARE_PUBLIC
            hardware_interface::CallbackReturn on_activate(const rclcpp_lifecycle::State & previous_state) override;

            CUSTOM_HARDWARE_PUBLIC
            hardware_interface::CallbackReturn on_deactivate(const rclcpp_lifecycle::State & previous_state) override;

            CUSTOM_HARDWARE_PUBLIC
            hardware_interface::return_type read(const rclcpp::Time & time, const rclcpp::Duration & period) override;

            CUSTOM_HARDWARE_PUBLIC
            hardware_interface::return_type write(const rclcpp::Time & time, const rclcpp::Duration & period) override;
        
            private:
                //below are basically vectors that store controllers and hardware states and information
                std::vector<double> hw_commands_;
                std::vector<double> hw_states_position_;
                std::vector<double> hw_states_velocity;
    };
}
#endif // CUSTOM_HARDWARE_INTERFACE_ADAFRUIT_PWM_HAT_HPP