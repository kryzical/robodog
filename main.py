import pygame
pygame.init()

WIDTH = 800
HEIGHT = 800


def main():
    #display window
    pygame.display.set_mode((WIDTH,HEIGHT))
    global running
    global up
    global down
    global right
    global left
    up = False
    down = False
    left = False
    right = False
    running = True
    while running:
        get_keyevent()
        if left == True:
            print("left")

def get_keyevent():
    global running
    global up
    global down
    global right
    global left
    for event in pygame.event.get():
        #quitting UI
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
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                up = False
            if event.key == pygame.K_s:
                down = False
            if event.key == pygame.K_a:
                left = False
            if event.key == pygame.K_d:
                right = False

if __name__ == "__main__":
    main()