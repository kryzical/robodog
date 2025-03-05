#ifndef QUADRUPED_DESCRIPTION_H
#define QUADRUPED_DESCRIPTION_H

namespace robodog
{
    namespace URDF
    {
        void loadFromHeader(QuadrupedBase &base)
        {
            // Left Front Leg
            base.lf.hip.setOrigin(0.175, 0.105, 0, 0, 0, 0);
            base.lf.upper_leg.setOrigin(0, 0.06, 0, 0, 0, 0);
            base.lf.lower_leg.setOrigin(0, 0, -0.141, 0, 0, 0);
            base.lf.foot.setOrigin(0, 0, -0.141, 0, 0, 0);

            // Right Front Leg    
            base.rf.hip.setOrigin(0.175, -0.105, 0, 0, 0, 0);
            base.rf.upper_leg.setOrigin(0, -0.06, 0, 0, 0, 0);
            base.rf.lower_leg.setOrigin(0, 0, -0.141, 0, 0, 0);
            base.rf.foot.setOrigin(0, 0, -0.141, 0, 0, 0);

            // Left Hind Leg
            base.lh.hip.setOrigin(-0.175, 0.105, 0, 0, 0, 0);
            base.lh.upper_leg.setOrigin(0, 0.06, 0, 0, 0, 0);
            base.lh.lower_leg.setOrigin(0, 0, -0.141, 0, 0, 0);
            base.lh.foot.setOrigin(0, 0, -0.141, 0, 0, 0);

            // Right Hind Leg
            base.rh.hip.setOrigin(-0.175, -0.105, 0, 0, 0, 0);
            base.rh.upper_leg.setOrigin(0, -0.06, 0, 0, 0, 0);
            base.rh.lower_leg.setOrigin(0, 0, -0.141, 0, 0, 0);
            base.rh.foot.setOrigin(0, 0, -0.141, 0, 0, 0);

            // Set joint names (matching the URDF)
            base.lf.hip.joint_name = "lf_hip_joint";
            base.lf.upper_leg.joint_name = "lf_upper_leg_joint";
            base.lf.lower_leg.joint_name = "lf_lower_leg_joint";
            
            base.rf.hip.joint_name = "rf_hip_joint";
            base.rf.upper_leg.joint_name = "rf_upper_leg_joint";
            base.rf.lower_leg.joint_name = "rf_lower_leg_joint";
            
            base.lh.hip.joint_name = "lh_hip_joint";
            base.lh.upper_leg.joint_name = "lh_upper_leg_joint";
            base.lh.lower_leg.joint_name = "lh_lower_leg_joint";
            
            base.rh.hip.joint_name = "rh_hip_joint";
            base.rh.upper_leg.joint_name = "rh_upper_leg_joint";
            base.rh.lower_leg.joint_name = "rh_lower_leg_joint";
        }
    }
}

#endif