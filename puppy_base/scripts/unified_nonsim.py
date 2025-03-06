#!/usr/bin/env python3
from adafruit_servokit import ServoKit
import time

class StandaloneRobotController:
    def __init__(self):
        # Initialize physical robot control
        self.kit = ServoKit(channels=16)
        
        # Physical servo mappings
        self.servo_map = {
            'lf1': 4,  # front left upper
            'lf2': 5,  # front left lower
            'rf1': 6,  # front right upper
            'rf2': 7,  # front right lower
            'lr1': 12, # back left upper
            'lr2': 13, # back left lower
            'rr1': 14, # back right upper
            'rr2': 15  # back right lower
        }

    def set_servo_angle(self, servo_name, angle):
        """Set the angle for a specific servo"""
        if servo_name in self.servo_map:
            self.kit.servo[self.servo_map[servo_name]].angle = angle

    def set_joint_angles(self, angles_dict):
        """Set angles for multiple servos at once"""
        for servo_name, angle in angles_dict.items():
            self.set_servo_angle(servo_name, angle)

    def trot_forward(self):
        """Execute the trot forward gait"""
        print("Starting trot forward gait")
        
        # Initial angles
        lf1_a = 152
        lf2_a = 66
        lr1_a = 152
        lr2_a = 66
        rf1_a = 13
        rf2_a = 96
        rr1_a = 13
        rr2_a = 96
        interval_time = 0.00005  # Very small delay for smoother motion
        
        physical_angles = {
            'lf1': lf1_a, 'lf2': lf2_a,
            'lr1': lr1_a, 'lr2': lr2_a,
            'rf1': rf1_a, 'rf2': rf2_a,
            'rr1': rr1_a, 'rr2': rr2_a
        }
        
        # Set initial position
        self.set_joint_angles(physical_angles)
        time.sleep(1)  # Give time for the robot to reach initial position
        
        for _ in range(1):  # Just one cycle for now
            # Phase 1: swing rf lr
            # Lift
            i = 40  # lr and rf diff
            j = 30  # lf and rr diff
            
            while i >= 0 or j >= 0:
                if i >= 0:
                    lr2_a += 1  # Lift back left leg
                    rf2_a -= 1  # Lift front right leg
                    i -= 1
                    
                if j >= 0:
                    rr2_a += 1  # Adjust back right leg
                    lf2_a -= 1  # Adjust front left leg
                    j -= 1
                    
                self.set_joint_angles({
                    'lr2': lr2_a, 'rf2': rf2_a,
                    'rr2': rr2_a, 'lf2': lf2_a
                })
                time.sleep(interval_time)
            
            # Move rf and lr down (finish swing)
            i = 30  # rf1 and lr1 diff
            j = 40  # rf2 and lr2 diff
            
            while i >= 0 or j >= 0:
                if i >= 0:
                    rf1_a += 1  # Move front right leg forward
                    lr1_a -= 1  # Move back left leg backward
                    i -= 1
                    
                if j >= 0:
                    rf2_a += 1  # Lower front right leg
                    lr2_a -= 1  # Lower back left leg
                    j -= 1
                    
                self.set_joint_angles({
                    'rf1': rf1_a, 'lr1': lr1_a,
                    'rf2': rf2_a, 'lr2': lr2_a
                })
                time.sleep(interval_time)
            
            # Phase 2: swing lf rr
            i = 11  # lf1 and rr1 diff
            j = 30  # rf1 and lr1 diff
            k = 5   # rf2 and lr2 diff
            
            while i >= 0 or j >= 0 or k >= 0:
                if i >= 0:
                    lf1_a += 1  # Adjust front left upper
                    rr1_a -= 1  # Adjust back right upper
                    i -= 1
                    
                if j >= 0:
                    rf1_a -= 1  # Return front right leg
                    lr1_a += 1  # Return back left leg
                    j -= 1
                    
                if k >= 0:
                    # Commented out in original:
                    # rf2_a += 1
                    # lr2_a -= 1
                    k -= 1
                    
                self.set_joint_angles({
                    'lf1': lf1_a, 'rr1': rr1_a,
                    'rf1': rf1_a, 'lr1': lr1_a
                })
                time.sleep(interval_time)
            
            # Retract lf2 and rr2
            i = 40  # lf2 and rr2 diff
            while i >= 0:
                lf2_a += 1  # Lift front left leg
                rr2_a -= 1  # Lift back right leg
                i -= 1
                
                self.set_joint_angles({
                    'lf2': lf2_a, 'rr2': rr2_a
                })
                time.sleep(interval_time)
            
            # Swing lf1 and rr1 (return to standing)
            i = 12  # lf1 and rr1 diff
            j = 10  # lf2 and rr2 diff
            
            while i > 0 or j > 0:
                if i > 0:
                    lf1_a -= 1  # Return front left leg
                    rr1_a += 1  # Return back right leg
                    i -= 1
                    
                if j > 0:
                    lf2_a -= 1  # Lower front left leg
                    rr2_a += 1  # Lower back right leg
                    j -= 1
                    
                self.set_joint_angles({
                    'lf1': lf1_a, 'rr1': rr1_a,
                    'lf2': lf2_a, 'rr2': rr2_a
                })
                time.sleep(interval_time)
        
        print("Trot cycle completed")

    def turn_left(self):
        """Execute the turn left gait"""
        print("Turn left not implemented yet")
        # TODO: Implement turn left gait based on your existing implementation
        pass
        
    def stand(self):
        """Put the robot in a standing position"""
        print("Standing up")
        # Standard standing position
        physical_angles = {
            'lf1': 152, 'lf2': 66,
            'lr1': 152, 'lr2': 66,
            'rf1': 13,  'rf2': 96,
            'rr1': 13,  'rr2': 96
        }
        self.set_joint_angles(physical_angles)
        time.sleep(1)  # Give time to reach position

    def continuous_trot(self, cycles=5):
        """Execute multiple trot cycles"""
        print(f"Starting continuous trot for {cycles} cycles")
        
        for i in range(cycles):
            print(f"Cycle {i+1}/{cycles}")
            self.trot_forward()
            time.sleep(0.1)  # Short pause between cycles

if __name__ == '__main__':
    try:
        print("Initializing standalone robot controller")
        controller = StandaloneRobotController()
        time.sleep(1)  # Wait for initialization
        
        # Execute sequence of movements
        controller.stand()
        controller.continuous_trot(cycles=3)  # Do 3 trot cycles
        controller.stand()  # Return to standing position
        
        print("Movement sequence completed")
    except KeyboardInterrupt:
        print("Program interrupted by user")
    except Exception as e:
        print(f"Error: {e}")