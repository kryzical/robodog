#ifndef PUPPY_GAIT_CONFIG_H
#define PUPPY_GAIT_CONFIG_H

// Gait timing parameters
#define GAIT_CONFIG_STANCE_DURATION     0.25
#define GAIT_CONFIG_SWING_DURATION      0.25
#define GAIT_CONFIG_OVERLAP_TIME        0.1

// Motion parameters
#define GAIT_CONFIG_NOMINAL_HEIGHT      0.20
#define GAIT_CONFIG_SWING_HEIGHT        0.04
#define GAIT_CONFIG_STANCE_DEPTH        0.0
#define GAIT_CONFIG_STEP_LENGTH         0.1

// Velocity limits
#define GAIT_CONFIG_MAX_LINEAR_VEL_X    0.5
#define GAIT_CONFIG_MAX_LINEAR_VEL_Y    0.25
#define GAIT_CONFIG_MAX_ANGULAR_VEL_Z   1.0

// Gait patterns
#define GAIT_TROT_PHASE_PAIRS { \
    {{"rf_joint1", "rf_joint2", "lb_joint1", "lb_joint2"}, 0.0}, \
    {{"lf_joint1", "lf_joint2", "rb_joint1", "rb_joint2"}, 0.5} \
}

#endif // PUPPY_GAIT_CONFIG_H