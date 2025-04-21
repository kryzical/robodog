import rclpy 
from rclpy.node import Node 
import cv2
import numpy as np 
import pygame

def main():
    # print('hello')
    cap = cv2.VideoCapture(0)
    global WIDTH
    global HEIGHT
    global movement_states
    WIDTH = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    HEIGHT = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    window = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption("Camera Feed")

    while True:
        ret, frame = cap.read()
        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0,1))
        window.blit(frame_surface, (0, 0))
        pygame.display.update()

if __name__ == "__main__":
    main()
