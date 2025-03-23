#!/usr/bin/env python3
"""
Virtual Joystick GUI for PuppyPi Robot.
This script provides a GUI interface to simulate a joystick/gamepad
and publish ROS joystick messages.
"""

import rospy
import tkinter as tk
from sensor_msgs.msg import Joy
import time

class VirtualJoystickGUI:
    def __init__(self):
        """Initialize the virtual joystick GUI"""
        rospy.init_node('virtual_joystick', anonymous=True)
        rospy.loginfo("Starting Virtual Joystick GUI")
        
        # Set up ROS publisher
        self.joy_pub = rospy.Publisher('/joy', Joy, queue_size=10)
        
        # Set up GUI
        self.root = tk.Tk()
        self.root.title("PuppyPi Virtual Joystick")
        self.root.geometry("400x400")
        self.root.configure(bg="#222222")
        
        # Create a frame for the joystick controls
        joystick_frame = tk.Frame(self.root, bg="#222222")
        joystick_frame.pack(pady=20)
        
        # Create a canvas for the analog stick
        self.stick_size = 200
        self.canvas = tk.Canvas(joystick_frame, width=self.stick_size, height=self.stick_size, 
                               bg="#333333", highlightthickness=2, highlightbackground="#555555")
        self.canvas.pack()
        
        # Draw the base circle
        self.center_x = self.stick_size // 2
        self.center_y = self.stick_size // 2
        self.outer_radius = self.stick_size // 2 - 10
        self.inner_radius = 30
        
        self.canvas.create_oval(
            self.center_x - self.outer_radius, 
            self.center_y - self.outer_radius,
            self.center_x + self.outer_radius, 
            self.center_y + self.outer_radius,
            fill="#444444", outline="#666666", width=2
        )
        
        # Draw the joystick handle
        self.handle = self.canvas.create_oval(
            self.center_x - self.inner_radius,
            self.center_y - self.inner_radius,
            self.center_x + self.inner_radius,
            self.center_y + self.inner_radius,
            fill="#007acc", outline="#0099ff", width=2
        )
        
        # Add crosshairs
        self.canvas.create_line(
            self.center_x, self.center_y - self.outer_radius, 
            self.center_x, self.center_y + self.outer_radius,
            fill="#666666", dash=(4, 4)
        )
        self.canvas.create_line(
            self.center_x - self.outer_radius, self.center_y,
            self.center_x + self.outer_radius, self.center_y,
            fill="#666666", dash=(4, 4)
        )
        
        # Setup mouse events for joystick
        self.canvas.bind("<Button-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_move)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)
        
        # Current joystick position (normalized -1.0 to 1.0)
        self.joystick_x = 0.0
        self.joystick_y = 0.0
        self.dragging = False
        
        # Create a frame for the directional buttons
        button_frame = tk.Frame(self.root, bg="#222222")
        button_frame.pack(pady=10)
        
        # Create directional buttons
        button_style = {
            "width": 8, 
            "height": 2, 
            "font": ("Arial", 10, "bold"),
            "bg": "#555555",
            "fg": "white",
            "activebackground": "#777777"
        }
        
        # Button definitions with mappings for PS4-like controller:
        # These indices match standard joy_node mapping:
        # Triangle (4), Circle (5), X (6), Square (7)
        self.buttons = [
            {"text": "▲", "index": 4, "row": 0, "col": 1, "command": self.forward_pressed},
            {"text": "◄", "index": 7, "row": 1, "col": 0, "command": self.left_pressed},
            {"text": "■", "index": 2, "row": 1, "col": 1, "command": self.stop_pressed},
            {"text": "►", "index": 5, "row": 1, "col": 2, "command": self.right_pressed},
            {"text": "▼", "index": 6, "row": 2, "col": 1, "command": self.backward_pressed}
        ]
        
        # Create the buttons
        self.button_states = [0] * 12  # Store button states for 12 possible buttons
        self.button_widgets = {}
        
        for btn in self.buttons:
            button = tk.Button(
                button_frame, 
                text=btn["text"], 
                command=btn["command"],
                **button_style
            )
            button.grid(row=btn["row"], column=btn["col"], padx=5, pady=5)
            self.button_widgets[btn["index"]] = button
        
        # Status indicator
        self.status_var = tk.StringVar()
        self.status_var.set("Ready - Click and drag joystick or press buttons")
        status_label = tk.Label(self.root, textvariable=self.status_var, 
                              fg="#00ff00", bg="#222222", font=("Arial", 10))
        status_label.pack(pady=10)
        
        # Coordinates display
        self.coords_var = tk.StringVar()
        self.coords_var.set("X: 0.00, Y: 0.00")
        coords_label = tk.Label(self.root, textvariable=self.coords_var, 
                              fg="#ffffff", bg="#222222", font=("Arial", 10))
        coords_label.pack()
        
        # Setup a timer to regularly publish joy messages
        self.last_publish_time = time.time()
        self.publish_interval = 0.05  # 20 Hz publishing rate
        self.root.after(10, self.publish_joy)
        
        # Message count display
        self.msg_count = 0
        self.msg_count_var = tk.StringVar()
        self.msg_count_var.set("Messages sent: 0")
        msg_count_label = tk.Label(self.root, textvariable=self.msg_count_var,
                                 fg="#aaaaaa", bg="#222222", font=("Arial", 9))
        msg_count_label.pack(side=tk.BOTTOM, pady=5)
    
    def on_mouse_down(self, event):
        """Handle mouse down event on the joystick canvas"""
        self.dragging = True
        self.update_joystick_position(event.x, event.y)
    
    def on_mouse_move(self, event):
        """Handle mouse drag event on the joystick canvas"""
        if self.dragging:
            self.update_joystick_position(event.x, event.y)
    
    def on_mouse_up(self, event):
        """Handle mouse release event on the joystick canvas"""
        self.dragging = False
        # Return to center position
        self.joystick_x = 0.0
        self.joystick_y = 0.0
        self.update_joystick_display()
        self.status_var.set("Joystick released - returned to center")
    
    def update_joystick_position(self, x, y):
        """Update the joystick position based on mouse coordinates"""
        # Calculate distance from center
        dx = x - self.center_x
        dy = y - self.center_y
        distance = (dx**2 + dy**2)**0.5
        
        # Normalize to -1.0 to 1.0 range
        if distance > self.outer_radius:
            # Clamp to edge of circle
            dx = dx * self.outer_radius / distance
            dy = dy * self.outer_radius / distance
            distance = self.outer_radius
        
        # Calculate joystick coordinates (-1.0 to 1.0)
        self.joystick_x = dx / self.outer_radius
        self.joystick_y = -dy / self.outer_radius  # Invert Y for proper orientation
        
        # Update display
        self.update_joystick_display()
        self.status_var.set(f"Joystick active - {distance:.1f}% of max range")
    
    def update_joystick_display(self):
        """Update the visual position of the joystick handle"""
        # Calculate new handle position
        handle_x = self.center_x + self.joystick_x * self.outer_radius
        handle_y = self.center_y - self.joystick_y * self.outer_radius  # Invert Y
        
        # Update handle position
        self.canvas.coords(
            self.handle,
            handle_x - self.inner_radius,
            handle_y - self.inner_radius,
            handle_x + self.inner_radius,
            handle_y + self.inner_radius
        )
        
        # Update coordinates display
        self.coords_var.set(f"X: {self.joystick_x:.2f}, Y: {self.joystick_y:.2f}")
    
    def forward_pressed(self):
        """Handle forward button press"""
        self.button_press_action(self.buttons[0]["index"], "Forward")
    
    def left_pressed(self):
        """Handle left button press"""
        self.button_press_action(self.buttons[1]["index"], "Left")
    
    def stop_pressed(self):
        """Handle stop button press"""
        self.button_press_action(self.buttons[2]["index"], "Stop")
    
    def right_pressed(self):
        """Handle right button press"""
        self.button_press_action(self.buttons[3]["index"], "Right")
    
    def backward_pressed(self):
        """Handle backward button press"""
        self.button_press_action(self.buttons[4]["index"], "Backward")
    
    def button_press_action(self, button_index, action_name):
        """Generic button press handler"""
        # Toggle button state
        self.button_states[button_index] = 1
        self.status_var.set(f"{action_name} button pressed")
        
        # Schedule button release after a short delay
        self.root.after(500, lambda: self.button_release_action(button_index))
        
        # Highlight the button visually
        button = self.button_widgets[button_index]
        original_bg = button.cget("bg")
        button.config(bg="#00aa44")
        self.root.after(200, lambda: button.config(bg=original_bg))
    
    def button_release_action(self, button_index):
        """Handle button release"""
        self.button_states[button_index] = 0
    
    def publish_joy(self):
        """Publish Joy messages at a regular interval"""
        current_time = time.time()
        
        # Publish at the specified rate
        if current_time - self.last_publish_time >= self.publish_interval:
            self.last_publish_time = current_time
            
            # Create Joy message
            joy_msg = Joy()
            joy_msg.header.stamp = rospy.Time.now()
            
            # Set axes: [left_stick_x, left_stick_y, ...]
            # Standard order is 0=left-right, 1=up-down
            joy_msg.axes = [self.joystick_x, -self.joystick_y]
            
            # Add dummy axes to match expected number (8 total)
            for _ in range(6):
                joy_msg.axes.append(0.0)
            
            # Set buttons state
            joy_msg.buttons = self.button_states
            
            # Publish message
            self.joy_pub.publish(joy_msg)
            
            # Update message count
            self.msg_count += 1
            self.msg_count_var.set(f"Messages sent: {self.msg_count}")
        
        # Schedule next update
        self.root.after(10, self.publish_joy)
    
    def run(self):
        """Run the main GUI loop"""
        self.root.mainloop()

if __name__ == "__main__":
    try:
        virtual_joystick = VirtualJoystickGUI()
        virtual_joystick.run()
    except rospy.ROSInterruptException:
        pass
    except Exception as e:
        rospy.logerr(f"Error in virtual joystick: {e}") 