#!/usr/bin/env bash
# This is a wrapper script that ensures ROS environment is loaded before running Python

# Force ROS to use localhost instead of any other IP
export ROS_MASTER_URI=http://localhost:11311
export ROS_HOSTNAME=localhost
export ROS_IP=127.0.0.1

# Source ROS environment
source /opt/ros/noetic/setup.bash

# Show network configuration for debugging
echo "ROS network configuration:"
echo "ROS_MASTER_URI=$ROS_MASTER_URI"
echo "ROS_HOSTNAME=$ROS_HOSTNAME"
echo "ROS_IP=$ROS_IP"

# Now execute the Python script with the ROS environment loaded
exec python3 -c '
import os
import sys
import math
import time

try:
    import rospy
    from std_msgs.msg import Float64
    from sensor_msgs.msg import JointState
except ImportError:
    print("ERROR: ROS Python modules not found!")
    print("Make sure ROS is installed and the environment is properly set up.")
    print("Try sourcing the ROS environment: source /opt/ros/noetic/setup.bash")
    sys.exit(1)

class MovementBridge:
    """Bridge between holder code servo angles and ROS joint controllers"""
    
    def __init__(self):
        # Initialize ROS node
        rospy.init_node("movement_bridge", anonymous=True)
        
        # Define the joint publishers for simulation
        self.publishers = {
            # Left front leg
            "lf1": rospy.Publisher("/puppy/joint2_position_controller/command", Float64, queue_size=1),
            "lf2": rospy.Publisher("/puppy/joint6_position_controller/command", Float64, queue_size=1),
            # Right front leg
            "rf1": rospy.Publisher("/puppy/joint1_position_controller/command", Float64, queue_size=1),
            "rf2": rospy.Publisher("/puppy/joint5_position_controller/command", Float64, queue_size=1),
            # Left rear leg
            "lr1": rospy.Publisher("/puppy/joint4_position_controller/command", Float64, queue_size=1),
            "lr2": rospy.Publisher("/puppy/joint8_position_controller/command", Float64, queue_size=1),
            # Right rear leg
            "rr1": rospy.Publisher("/puppy/joint3_position_controller/command", Float64, queue_size=1),
            "rr2": rospy.Publisher("/puppy/joint7_position_controller/command", Float64, queue_size=1),
        }
        
        # Standing position angles (from holder/stand.py)
        self.stand_angles = {
            "lf1": 152,  # front left upper
            "lf2": 66,   # front left lower
            "lr1": 152,  # back left upper
            "lr2": 66,   # back left lower
            "rf1": 13,   # front right upper
            "rf2": 96,   # front right lower
            "rr1": 13,   # back right upper
            "rr2": 96    # back right lower
        }
        
        rospy.loginfo("Movement bridge initialized successfully")
    
    def physical_to_sim_angle(self, servo_name, angle):
        """Convert physical servo angles to simulation joint angles"""
        if servo_name in ["lf1", "lr1"]:
            # Left upper servos: 0(forward) 180(backward)
            return math.radians(-(angle - 90))
        elif servo_name in ["lf2", "lr2"]:
            # Left lower servos: 0(extended) 180(in)
            return math.radians(angle - 90)
        elif servo_name in ["rf1", "rr1"]:
            # Right upper servos: 0(backward) 180(forward)
            return math.radians(angle - 90)
        elif servo_name in ["rf2", "rr2"]:
            # Right lower servos: 0(in) 180(extended)
            return math.radians(-(angle - 90))
        return 0
    
    def set_servo_angle(self, servo_name, angle):
        """Set the angle of a specific servo in simulation"""
        if servo_name in self.publishers:
            # Convert physical angle to simulation angle
            sim_angle = self.physical_to_sim_angle(servo_name, angle)
            
            # Publish the command
            self.publishers[servo_name].publish(Float64(sim_angle))
            rospy.logdebug(f"Set {servo_name} to {angle} degrees ({sim_angle} radians)")
    
    def stand(self):
        """Make the robot stand by sending all joint commands"""
        rospy.loginfo("Standing up robot in simulation")
        
        # Set all joints to standing position
        for servo_name, angle in self.stand_angles.items():
            self.set_servo_angle(servo_name, angle)
        
        # Wait for robot to reach position
        rospy.sleep(1.0)
        rospy.loginfo("Robot should be standing")
    
    def trot_forward(self):
        """Perform trot forward gait with the robot"""
        rospy.loginfo("Trotting forward")
        
        # Simplified trot forward pattern - actual pattern would be more complex
        # This demonstrates the servo control pattern from holder/movement.py
        
        # Initial standing position angles
        lf1_a = 152
        lf2_a = 66
        lr1_a = 152
        lr2_a = 66
        rf1_a = 13
        rf2_a = 96
        rr1_a = 13
        rr2_a = 96
        
        interval_time = 0.005  # Slower than physical robot for visualization
        
        for _ in range(1):
            # Phase 1: Swing right front (rf) and left rear (lr) legs
            for i in range(40):
                lr2_a += 1  # Lift left rear leg
                rf2_a -= 1  # Lift right front leg
                
                self.set_servo_angle("lr2", lr2_a)
                self.set_servo_angle("rf2", rf2_a)
                
                if i < 30:  # Move other legs less (shorter stride)
                    rr2_a += 1  # Move right rear leg
                    lf2_a -= 1  # Move left front leg
                    self.set_servo_angle("rr2", rr2_a)
                    self.set_servo_angle("lf2", lf2_a)
                    
                rospy.sleep(interval_time)
                
            # Move rf and lr forward and down
            for i in range(30):
                rf1_a += 1
                lr1_a -= 1
                self.set_servo_angle("rf1", rf1_a)
                self.set_servo_angle("lr1", lr1_a)
                
                if i < 40:
                    rf2_a += 1  # Lower right front leg
                    lr2_a -= 1  # Lower left rear leg
                    self.set_servo_angle("rf2", rf2_a)
                    self.set_servo_angle("lr2", lr2_a)
                
                rospy.sleep(interval_time)
                
            # Phase 2: Swing left front (lf) and right rear (rr) legs
            for i in range(11):
                lf1_a += 1
                rr1_a -= 1
                self.set_servo_angle("lf1", lf1_a)
                self.set_servo_angle("rr1", rr1_a)
                
                if i < 30:
                    rf1_a -= 1
                    lr1_a += 1
                    self.set_servo_angle("rf1", rf1_a)
                    self.set_servo_angle("lr1", lr1_a)
                
                if i < 5:
                    rf2_a += 1
                    lr2_a -= 1
                    self.set_servo_angle("rf2", rf2_a)
                    self.set_servo_angle("lr2", lr2_a)
                
                rospy.sleep(interval_time)
                
            rospy.loginfo("Trot cycle complete")
            
            # Return to standing position
            self.stand()
            
    def run(self):
        """Main run method to demonstrate movements"""
        try:
            # Wait for publishers to connect
            rospy.sleep(1.0)
            
            # Stand up
            self.stand()
            rospy.sleep(2.0)
            
            # Trot forward
            self.trot_forward()
            rospy.sleep(1.0)
            
            # Stand up again
            self.stand()
            
            rospy.loginfo("Movement demo completed")
        
        except rospy.ROSInterruptException:
            rospy.loginfo("Movement bridge interrupted")

# Main execution
if __name__ == "__main__":
    try:
        bridge = MovementBridge()
        bridge.run()
        
        # Keep the node running
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
'