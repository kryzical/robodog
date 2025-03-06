#!/usr/bin/env python3
# coding=utf8

import sys
import math
import rospy
import timevs.srv import SetBool
import numpy as npg import Velocity, Pose, Gait
from std_msgs.msg import Float64
ROS_NODE_NAME = 'puppy_demo'
class PuppyStander:
    def __init__(self)::0, 'yaw_rate':0}
        rospy.init_node('puppy_stand', log_level=rospy.INFO) forward direction as the positive direction, measured in cm/s)
        ，左侧方向为正方向，单位cm/s，目前无此功能(lateral movement control, with the left direction as the positive direction, measured in cm/s. currently, this feature is bot available)
        # Define joint publishers - arranged by legwith counterclockwise direction as the positive direction, measured in rad/s)
        self.pubs = {}
        e = {'roll':math.radians(0), 'pitch':math.radians(0), 'yaw':0.000, 'height':-10, 'x_shift':0.5, 'stance_x':0, 'stance_y':0}
        # Right front legh.radians(0), 'pitch':math.radians(0), 'yaw':0.000, 'height':-10, 'x_shift':-0.5, 'stance_x':0, 'stance_y':0}
        self.pubs['rf_hip'] = rospy.Publisher('/puppy/joint1_position_controller/command', Float64, queue_size=1)imeters)
        self.pubs['rf_knee'] = rospy.Publisher('/puppy/joint5_position_controller/command', Float64, queue_size=1)meters)
        t: 4条腿在x轴上同向移动的距离，越小，走路越前倾，越大越后仰,通过调节x_shift可以调节小狗走路的平衡，单位cm(the distance traveled by the four legs along the x-axis determines the degree of forward or backward tilt during walking: smaller distances lead to more forward tilt, while larger distances result in more backward tilt. Adjusting the x_shift parameter can help maintain balance during the dog's movement, measured in centimeters)
        # Left front leg垂直距离，单位cm(the height of the dog, measured from the toe to the axis  of rotation of the thigh, is in centimeters)
        self.pubs['lf_hip'] = rospy.Publisher('/puppy/joint2_position_controller/command', Float64, queue_size=1)
        self.pubs['lf_knee'] = rospy.Publisher('/puppy/joint6_position_controller/command', Float64, queue_size=1)
        Trot'
        # Right back leg，单位秒(the time when all four legs touch the ground, measured in seconds)
        self.pubs['rb_hip'] = rospy.Publisher('/puppy/joint3_position_controller/command', Float64, queue_size=1)
        self.pubs['rb_knee'] = rospy.Publisher('/puppy/joint7_position_controller/command', Float64, queue_size=1)r, measured in seconds)
        rance：走路时，脚尖要抬高的距离，单位cm(the distance the paw needs to be raised during walking, measured in centimeters)
        # Left back leg
        self.pubs['lb_hip'] = rospy.Publisher('/puppy/joint4_position_controller/command', Float64, queue_size=1)
        self.pubs['lb_knee'] = rospy.Publisher('/puppy/joint8_position_controller/command', Float64, queue_size=1)
        yPose['x_shift'] = -0.6
        rospy.sleep(1.0)ime = 0(Trot gait clearance_time = 0)

    def send_commands(self, positions):
        """Send commands to all joints"""ing_time':0.2, 'clearance_time':0.1, 'z_clearance':5}
        for joint, pos in positions.items():
            if joint in self.pubs: swing_time( Amble gait 0 ＜ clearance_time ＜ swing time)
                self.pubs[joint].publish(Float64(pos))
elif gait == 'Walk':
    def calculate_leg_angles(self, x, y, z):_time':0.2, 'clearance_time':0.3, 'z_clearance':5}
        """se['x_shift'] = -0.65
        Simple inverse kinematics for a 2-DOF legait   swing_time ≤ clearance_time)
        x: forward/backward
        y: left/right (not used in 2-DOF case)
        z: up/downub.publish(x=0, y=0, yaw_rate=0)
        Returns: (hip_angle, knee_angle)
        """
        leg_length = 0.15  # Length of each leg segment in meters
        
        # Calculate leg angles using inverse kinematics)
        try:_shutdown(cleanup)
            r = math.sqrt(x*x + z*z)
            if r > 2 * leg_length:('/puppy_control/pose', Pose, queue_size=1)
                r = 2 * leg_lengthlisher('/puppy_control/gait', Gait, queue_size=1)
            ocityPub = rospy.Publisher('/puppy_control/velocity', Velocity, queue_size=1)
            # Calculate knee angle first
            knee_angle = math.acos((2 * leg_length * leg_length - r * r) / (2 * leg_length * leg_length))
            (stepping in place service)
            # Then calculate hip angle
            hip_angle = -math.atan2(x, -z) - math.atan2(leg_length * math.sin(knee_angle),
                                                     leg_length + leg_length * math.cos(knee_angle))pyPose['x_shift']
            ,height=PuppyPose['height'], roll=PuppyPose['roll'], pitch=PuppyPose['pitch'], yaw=PuppyPose['yaw'], run_time = 500)
            return hip_angle, knee_angle
        except:(0.2)
            return 0, 0publish(overlap_time = GaitConfig['overlap_time'], swing_time = GaitConfig['swing_time']
                    , clearance_time = GaitConfig['clearance_time'], z_clearance = GaitConfig['z_clearance'])
    def stand(self):
        """Execute standing sequence using coordinate-based control"""
        print("Starting stand up sequence...") y=PuppyMove['y'], yaw_rate=PuppyMove['yaw_rate'])
        rate = rospy.Rate(10)
        mark_time_srv(False)
        # Start with direct joint control for initial stable positionose['x_shift']即可(if the dog continues to move slowly forward on backward while stepping in place, it is necessary to readjust the dog's center of gravity. simply fine-tune 'x_shift' in PuppyPose)
        initial_positions = {
            'rf_hip': -0.4, 'rf_knee': 1.2,
            'lf_hip': -0.4, 'lf_knee': 1.2,e True:
            'rb_hip': 0.4, 'rb_knee': 1.2,
            'lb_hip': 0.4, 'lb_knee': 1.2
        }    if rospy.is_shutdown():
           sys.exit(0)
        print("Setting initial stable position...")except :
        self.send_commands(initial_positions)        rospy.sleep(2.0)                # Continue with your existing phases but with modified values        # Initial position for IK-based control        front_x = -0.1   # More under body        front_z = -0.12  # Not too low                back_x = 0.1     # Behind body        back_z = -0.12   # Not too low                y = 0                # Calculate angles using IK for these positions        front_hip, front_knee = self.calculate_leg_angles(front_x, y, front_z)        back_hip, back_knee = self.calculate_leg_angles(back_x, y, back_z)                # Ensure knees stay bent        front_knee = max(front_knee, 0.8)        back_knee = max(back_knee, 0.8)                # Update positions        positions = {            'rf_hip': front_hip, 'rf_knee': front_knee,            'lf_hip': front_hip, 'lf_knee': front_knee,            'rb_hip': back_hip, 'rb_knee': back_knee,            'lb_hip': back_hip, 'lb_knee': back_knee        }                print("Transitioning to IK-controlled position...")        self.send_commands(positions)        rospy.sleep(2.0)                # Now continue with your existing PHASE 1, but adjust the values        # PHASE 1: Position legs for strong push-up        target_front_x = -0.08  # Front legs positioned under shoulders        target_front_z = -0.10  # Lower position to prepare for push                target_back_x = 0.12    # Back legs positioned behind for support        target_back_z = -0.15   # Lower to support weight                steps = 15        for i in range(steps):            # Interpolate coordinates            current_front_x = front_x + (target_front_x - front_x) * i/steps            current_front_z = front_z + (target_front_z - front_z) * i/steps                        current_back_x = back_x + (target_back_x - back_x) * i/steps            current_back_z = back_z + (target_back_z - back_z) * i/steps                        # Calculate new angles            front_hip, front_knee = self.calculate_leg_angles(current_front_x, y, current_front_z)            back_hip, back_knee = self.calculate_leg_angles(current_back_x, y, current_back_z)                        # Ensure minimum knee bend (higher value = more bent)            front_knee = max(front_knee, 0)  # More bend for stability            back_knee = max(back_knee, 2)    # More bend for stability                        positions = {                'rf_hip': front_hip, 'rf_knee': front_knee,                'lf_hip': front_hip, 'lf_knee': front_knee,                'rb_hip': back_hip, 'rb_knee': back_knee,                'lb_hip': back_hip, 'lb_knee': back_knee            }                        self.send_commands(positions)            rate.sleep()                    print("Phase 1 complete: Legs positioned for standing")        rospy.sleep(1.0)                # PHASE 2: Standing up - extend legs significantly        target_front_z = -0.0 # Extend front legs significantly to stand up        target_back_z = -0.40   # Extend back legs significantly to stand up                steps = 25  # More steps for smoother motion        for i in range(steps):            # Gradually extend legs to push body up            extension_factor = (i/steps)**2  # Non-linear extension for smoother motion            current_front_z = current_front_z + (target_front_z - current_front_z) * extension_factor            current_back_z = current_back_z + (target_back_z - current_back_z) * extension_factor                        # Recalculate leg angles            front_hip, front_knee = self.calculate_leg_angles(current_front_x, y, current_front_z)            back_hip, back_knee = self.calculate_leg_angles(current_back_x, y, current_back_z)                        # Gradually reduce knee bend as robot stands up            knee_bend_factor = max(0.1, 0.6 - 0.5 * i/steps)            front_knee = max(front_knee, knee_bend_factor)            back_knee = max(back_knee, knee_bend_factor)                        positions = {                'rf_hip': front_hip, 'rf_knee': front_knee,                'lf_hip': front_hip, 'lf_knee': front_knee,                'rb_hip': back_hip, 'rb_knee': back_knee,                'lb_hip': back_hip, 'lb_knee': back_knee            }                        self.send_commands(positions)            rate.sleep()                    print("Phase 2 complete: Standing up")        rospy.sleep(1.0)                # PHASE 3: Final stabilization - adjust for balance        target_front_x = -0.08  # Move front legs for better weight distribution        target_back_x = 0.10    # Move back legs for better weight distribution                steps = 15        for i in range(steps):            # Fine-tune position for stability            current_front_x = current_front_x + (target_front_x - current_front_x) * i/steps            current_back_x = current_back_x + (target_back_x - current_back_x) * i/steps                        # Recalculate angles            front_hip, front_knee = self.calculate_leg_angles(current_front_x, y, current_front_z)            back_hip, back_knee = self.calculate_leg_angles(current_back_x, y, current_back_z)                        # Minimal knee bend for standing tall            front_knee = max(front_knee, 0.1)            back_knee = max(back_knee, 0.1)                        positions = {                'rf_hip': front_hip, 'rf_knee': front_knee,                'lf_hip': front_hip, 'lf_knee': front_knee,                'rb_hip': back_hip, 'rb_knee': back_knee,                'lb_hip': back_hip, 'lb_knee': back_knee            }                        self.send_commands(positions)
            rate.sleep()
        
        print("Standing position reached and stabilized")
        
        # Maintain standing position
        while not rospy.is_shutdown():
            self.send_commands(positions)
            rate.sleep()

def main():
    try:
        stander = PuppyStander()
        stander.stand()
    except Exception as e:
        rospy.logerr(f"Error: {e}")

if __name__ == '__main__':
    main()