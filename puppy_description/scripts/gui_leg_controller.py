#!/usr/bin/env python3
import rospy
from std_msgs.msg import Float64
import tkinter as tk
from tkinter import ttk

class LegControlGUI:
    def __init__(self):
        rospy.init_node('leg_control_gui')
        
        # Parameters
        self.max_angle_change = rospy.get_param('~max_angle_change', 0.7)  # radians
        self.standing_hip_angle = 0.8  # Standing position from gazebo.launch
        self.standing_knee_angle = 0.0  # Standing position from gazebo.launch
        self.step_size = 0.05  # Amount to change per button press
        
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
        
        # Create GUI
        self.root = tk.Tk()
        self.root.title("Leg Control GUI")
        self.root.geometry("300x400")
        self.create_widgets()
        
        # Keep publishing the position (to counter any other control nodes)
        self.timer_id = self.root.after(500, self.publish_periodically)
        
        rospy.loginfo("Leg control GUI started. Use the buttons to move the right front leg.")
        
    def create_widgets(self):
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Robot Leg Control", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Leg position display
        self.position_var = tk.StringVar(value=f"Current knee angle: {self.current_knee_angle:.2f}")
        position_label = ttk.Label(main_frame, textvariable=self.position_var, font=("Arial", 12))
        position_label.pack(pady=10)
        
        # Control buttons frame
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(pady=20)
        
        # Up button
        up_button = ttk.Button(control_frame, text="Move Up", command=self.move_up)
        up_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        
        # Down button
        down_button = ttk.Button(control_frame, text="Move Down", command=self.move_down)
        down_button.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        
        # Reset button
        reset_button = ttk.Button(control_frame, text="Reset Position", command=self.reset_position)
        reset_button.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
        
        # Keyboard bindings
        self.root.bind("<w>", lambda event: self.move_up())
        self.root.bind("<s>", lambda event: self.move_down())
        self.root.bind("<r>", lambda event: self.reset_position())
        
        # Keyboard instructions
        key_frame = ttk.LabelFrame(main_frame, text="Keyboard Controls")
        key_frame.pack(pady=10, fill="x")
        
        ttk.Label(key_frame, text="W : Move Up").pack(anchor="w", padx=10)
        ttk.Label(key_frame, text="S : Move Down").pack(anchor="w", padx=10)
        ttk.Label(key_frame, text="R : Reset Position").pack(anchor="w", padx=10)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def move_up(self):
        self.current_knee_angle = min(self.current_knee_angle + self.step_size, 
                                      self.standing_knee_angle + self.max_angle_change)
        self.publish_positions()
        self.position_var.set(f"Current knee angle: {self.current_knee_angle:.2f}")
        self.status_var.set(f"Moved leg UP | Knee angle: {self.current_knee_angle:.2f}")
    
    def move_down(self):
        self.current_knee_angle = max(self.current_knee_angle - self.step_size, 
                                      self.standing_knee_angle - self.max_angle_change)
        self.publish_positions()
        self.position_var.set(f"Current knee angle: {self.current_knee_angle:.2f}")
        self.status_var.set(f"Moved leg DOWN | Knee angle: {self.current_knee_angle:.2f}")
    
    def reset_position(self):
        self.current_knee_angle = self.standing_knee_angle
        self.publish_positions()
        self.position_var.set(f"Current knee angle: {self.current_knee_angle:.2f}")
        self.status_var.set(f"RESET to standing position")
    
    def publish_positions(self):
        # Keep hip at standing angle, only adjust knee
        self.hip_pub.publish(Float64(self.standing_hip_angle))
        self.knee_pub.publish(Float64(self.current_knee_angle))
    
    def publish_periodically(self):
        # Publish positions continuously to maintain control
        self.publish_positions()
        # Schedule next publish
        self.timer_id = self.root.after(500, self.publish_periodically)
    
    def run(self):
        try:
            # Start GUI main loop
            self.root.mainloop()
        except rospy.ROSInterruptException:
            pass
        finally:
            if self.timer_id:
                self.root.after_cancel(self.timer_id)

if __name__ == '__main__':
    try:
        controller = LegControlGUI()
        controller.run()
    except rospy.ROSInterruptException:
        pass