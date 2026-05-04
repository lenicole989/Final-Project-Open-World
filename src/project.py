import pygame
import sys
import random
import math

blue = (0, 81, 186)

class character:
    def __init__(self, x, y):
        # Store coordinates
        self.pos = [x, y]
        self.size = [30, 20]
        self.speed = 5



def main():
    pygame.init()
    pygame.display.set_caption("Shopping at 1KEA")
    resolution = (0,0)
    screen = pygame.display.set_mode(resolution, pygame.FULLSCREEN)
    width, height = screen.get_size()
    clock = pygame.time.Clock()
    dt = 0
    player = character(width//2, height//2)
    # Event Loop
    running =True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False







if __name__ == "__main__":
    main()