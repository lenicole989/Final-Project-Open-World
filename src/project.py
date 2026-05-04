import pygame
import random
import math
import sys

blue = (0, 81, 186)

class character:
    def __init__(self, x, y):
        # Store coordinates
        self.pos = [x, y]
        self.size = [30, 20]
        self.speed = 5

clock = pygame.time.Clock()
player_position = [400, 250]


def main():
    pygame.init()
    pygame.display.set_caption("Shopping at 1KEA")
    clock = pygame.time.Clock()
    dt = 0 
    resolution = (0,0)
    screen = pygame.display.set_mode(resolution, pygame.FULLSCREEN)





if __name__ == "__main__":
    main()