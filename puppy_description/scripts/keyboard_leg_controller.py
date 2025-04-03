#!/usr/bin/env python3
import rospy
from std_msgs.msg import Float64
import sys
import tty
import termios
import threading
import signal

class KeyboardLegController:
    def __init__(self):
        rospy.init_node('keyboard_leg_controller')
        
        # Parameters - can be adjusted
        self.max_angle_change = rospy.get_param('~max_angle_change', 0.7)  # radians
        self.standing_hip_angle = 0.8  # Standing position from gazebo.launch
        self.standing_knee_angle = 0.0  # Standing position from gazebo.launch
        self.step_size = 0.05  # Amount to change per keystroke
        
        # Set up publishers for right front leg joints
        self.hip_pub = rospy.Publisher(
            '/puppy/joint1_position_controller/command',  # RF hip joint
            Float64, 
            queue_size=1
        )
        self.knee_pub = rospy.Publisher(
            '/puppy/joint5_position_controller/command',  # RF knee joint
            Float64, 
            queue_size=1
        )
        
        # Initialize variables for current joint positions
        self.current_knee_angle = self.standing_knee_angle
        
        # Set initial position
        rospy.sleep(1)  # Wait for publishers to initialize
        self.publish_positions()
        
        rospy.loginfo("Keyboard controller initialized for right front leg")
        rospy.loginfo("Use 'w' to move leg up, 's' to move leg down, 'q' to quit")
        
        # Start keyboard listening thread
        self.is_running = True
        self.keyboard_thread = threading.Thread(target=self.keyboard_listener)
        self.keyboard_thread.daemon = True
        self.keyboard_thread.start()
        
        # Set up signal handler for Ctrl+C
        signal.signal(signal.SIGINT, self.signal_handler)
    
    def signal_handler(self, sig, frame):
        self.is_running = False
        rospy.signal_shutdown("User terminated")
        sys.exit(0)
    
    def get_key(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            key = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return key
    
    def keyboard_listener(self):
        # Print instructions
        print("\033c", end="")  # Clear screen
        print("──────────────────────────────────")
        print("  PUPPY LEG KEYBOARD CONTROLLER   ")
        print("──────────────────────────────────")
        print("  w : Move leg UP                 ")
        print("  s : Move leg DOWN               ")
        print("  r : Reset to standing position  ")
        print("  q : Quit                        ")
        print("──────────────────────────────────")
        print(f"Current knee angle: {self.current_knee_angle:.2f}")
        
        while self.is_running:
            key = self.get_key()
            
            if key == 'w':  # Move leg up
                self.current_knee_angle = min(self.current_knee_angle + self.step_size, 
                                             self.standing_knee_angle + self.max_angle_change)
                self.publish_positions()
                print(f"Leg UP   | Knee angle: {self.current_knee_angle:.2f}")
            
            elif key == 's':  # Move leg down
                self.current_knee_angle = max(self.current_knee_angle - self.step_size, 
                                             self.standing_knee_angle - self.max_angle_change)
                self.publish_positions()
                print(f"Leg DOWN | Knee angle: {self.current_knee_angle:.2f}")
            
            elif key == 'r':  # Reset position
                self.current_knee_angle = self.standing_knee_angle
                self.publish_positions()
                print(f"RESET    | Knee angle: {self.current_knee_angle:.2f}")
            
            elif key == 'q':  # Quit
                print("Exiting...")
                self.is_running = False
                rospy.signal_shutdown("User requested shutdown")
                break
    
    def publish_positions(self):
        # Keep hip at standing angle, only adjust knee
        self.hip_pub.publish(Float64(self.standing_hip_angle))
        self.knee_pub.publish(Float64(self.current_knee_angle))

if __name__ == '__main__':
    try:
        controller = KeyboardLegController()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
    except KeyboardInterrupt:
        print("Keyboard interrupt received, shutting down.")
        sys.exit(0)