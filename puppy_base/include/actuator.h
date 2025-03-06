#ifndef ACTUATOR_H
#define ACTUATOR_H

#include <ros/ros.h>

namespace robodog
{
    class Actuator
    {
        public:
            Actuator(){}
            virtual void moveJoint(float joint_position, uint8_t joint_id) = 0;
            virtual float getJointPosition(uint8_t joint_id) = 0;
            virtual void registerJoint(uint8_t joint_id) = 0;
            virtual void init() = 0;
    };

    class SimulationActuator : public Actuator
    {
        public:
            SimulationActuator(){}
            void moveJoint(float joint_position, uint8_t joint_id){}
            float getJointPosition(uint8_t joint_id){ return 0.0; }
            void registerJoint(uint8_t joint_id){}
            void init(){}
    };

    class DynamixelActuator : public Actuator
    {
        public:
            DynamixelActuator(){}
            void moveJoint(float joint_position, uint8_t joint_id){}
            float getJointPosition(uint8_t joint_id){ return 0.0; }
            void registerJoint(uint8_t joint_id){}
            void init(){}
    };

    class ServoActuator : public Actuator
    {
        public:
            ServoActuator(){}
            void moveJoint(float joint_position, uint8_t joint_id){}
            float getJointPosition(uint8_t joint_id){ return 0.0; }
            void registerJoint(uint8_t joint_id){}
            void init(){}
    };
}