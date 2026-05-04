import pygame
import sys
import random
import math

blue = (0, 81, 186)
yellow = (255, 218, 0)

class character:
    def __init__(self, x, y):
        # Store coordinates
        self.pos = [x, y]
        self.size = [30, 20]
        self.speed = 5

    # Defining how user moves using keys
    def move(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.pos.y -= self.speed * dt
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.pos.y += self.speed * dt
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.pos.x -= self.speed * dt
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.pos.x += self.speed * dt
    
    def draw(self, screen):
        pygame.draw.rect(screen, yellow, (self.pos.x, self.pos.y, self.size[0]))
        




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

        dt = clock.tick(60)
        player.move(dt)
        player.check_bounds(width, height)
        screen.fill(blue)
        player.draw(screen)
        pygame.display.flip()
pygame.quit()






if __name__ == "__main__":
    main()