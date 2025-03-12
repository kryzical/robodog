#!/usr/bin/env python3
import pygame
import stand as st
import movement as mvt
import sys
import time

# Try to import ROS library
try:
    import rospy
    ROS_AVAILABLE = True
except ImportError:
    ROS_AVAILABLE = False

# Configuration
WIDTH = 800
HEIGHT = 800
SIMULATION_MODE = st.simulation_mode
AUTO_DEMO_ENABLED = "--auto" in sys.argv
AUTO_SEQUENCE = ["stand", "trot", "turn_left", "turn_right", "stand"]
AUTO_TIMES = [3, 5, 3, 3, 3]  # seconds for each action in AUTO_SEQUENCE

def main():
    # Initialize pygame for UI control
    pygame.init()
    
    # Display window
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("RoboDog Controller" + (" (Simulation)" if SIMULATION_MODE else ""))
    
    # Make puppy stand
    st.stand()
    
    # Control flags
    running = True
    up = False
    down = False
    left = False
    right = False
    
    print("RoboDog Controller")
    print("-----------------")
    print("Controls:")
    print("W - Trot Forward")
    print("A - Turn Left")
    print("D - Turn Right")
    print("S - Stop (stand)")
    print("ESC - Exit")
    print()
    
    if AUTO_DEMO_ENABLED:
        run_auto_demo()
        return
    
    # Main control loop
    last_action_time = time.time()
    action_timeout = 0.5  # seconds to wait between actions
    
    while running:
        current_time = time.time()
        time_since_last = current_time - last_action_time
        
        get_keyevent(running, up, down, left, right)
        
        # Only allow movements after the timeout to avoid overloading
        if time_since_last > action_timeout:
            if up:
                mvt.trot_forward()
                last_action_time = current_time
            elif left:
                mvt.turn_left()
                last_action_time = current_time
            elif right:
                mvt.turn_right()
                last_action_time = current_time
            elif down:
                st.stand()
                last_action_time = current_time
                
        # Ensure the display stays responsive during motion
        pygame.display.flip()
        
        # Check for ROS shutdown if in simulation
        if SIMULATION_MODE and ROS_AVAILABLE and rospy.is_shutdown():
            running = False


def get_keyevent(running, up, down, left, right):
    """Handle keyboard input to control the robot"""
    for event in pygame.event.get():
        # Quitting UI
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                up = True
            if event.key == pygame.K_s:
                down = True
            if event.key == pygame.K_a:
                left = True
            if event.key == pygame.K_d:
                right = True
            if event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                up = False
            if event.key == pygame.K_s:
                down = False
            if event.key == pygame.K_a:
                left = False
            if event.key == pygame.K_d:
                right = False
    
    return running, up, down, left, right


def run_auto_demo():
    """Run an automated demo sequence"""
    print("Running automated demo sequence...")
    
    for i, action in enumerate(AUTO_SEQUENCE):
        print(f"Executing: {action} for {AUTO_TIMES[i]} seconds")
        
        if action == "stand":
            st.stand()
        elif action == "trot":
            mvt.trot_forward()
        elif action == "turn_left":
            mvt.turn_left()
        elif action == "turn_right":
            mvt.turn_right()
            
        # Wait between actions
        if i < len(AUTO_SEQUENCE) - 1:
            time.sleep(AUTO_TIMES[i])
    
    print("Demo sequence complete")


if __name__ == "__main__":
    try:
        main()
    finally:
        # Clean up pygame
        pygame.quit()
        
        # Make sure to stand before exiting
        if not AUTO_DEMO_ENABLED:
            print("Standing before exit...")
            st.stand()
        
        print("Exiting RoboDog Controller")
