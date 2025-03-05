#ifndef HARDWARE_CONFIG_H
#define HARDWARE_CONFIG_H

#define USE_SIMULATION_ACTUATOR
// #define USE_DYNAMIXEL_ACTUATOR
// #define USE_SERVO_ACTUATOR

#define ACTUATOR_DRIVER  simulation
#define SENSOR_DRIVER    simulation

#ifdef USE_SIMULATION_ACTUATOR
    #define LEG_CONTROLLER_TYPE   LegController
    #define VELOCITY_CONTROLLER_TYPE  VelocityController
    #define ACTUATOR_CONTROLLER_TYPE  SimulationController
#endif 

#ifdef USE_DYNAMIXEL_ACTUATOR
    #define LEG_CONTROLLER_TYPE   LegController
    #define VELOCITY_CONTROLLER_TYPE  VelocityController
    #define ACTUATOR_CONTROLLER_TYPE  DynamixelController
#endif

#ifdef USE_SERVO_ACTUATOR
    #define LEG_CONTROLLER_TYPE   LegController
    #define VELOCITY_CONTROLLER_TYPE  VelocityController
    #define ACTUATOR_CONTROLLER_TYPE  ServoController
#endif

#define MAX_LINEAR_VELOCITY_X  0.5
#define MAX_LINEAR_VELOCITY_Y  0.25
#define MAX_ANGULAR_VELOCITY_Z 1.0

#define SERVO_PIN_MAP {2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13}
#define DYNAMIXEL_ID_MAP {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12}

#define JOINT_ORIENTATION {1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}

#define GAIT_CONFIG_NOMINAL_HEIGHT       0.20
#define GAIT_CONFIG_STANCE_DURATION     0.25
#define GAIT_CONFIG_SWING_HEIGHT        0.04
#define GAIT_CONFIG_STANCE_DEPTH        0.0

#define IMU_MOUNTING_ORIENTATION    EULER_X90_Y0_Z0

#endif