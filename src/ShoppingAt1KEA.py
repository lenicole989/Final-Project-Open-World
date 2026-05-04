import pygame
import sys
import random
import math

blue = (0, 81, 186)
yellow = (255, 218, 0)
brown = (101, 67, 33)

class character:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.size = [10, 10]
        self.speed = 100

    # Defining how user moves using keys
    def move(self, dt, shelves):
        seconds = dt / 1000
        keys = pygame.key.get_pressed()

        # Store position if shelf is in front
        old_x = self.pos.x
        old_y = self.pos.y

        # Up Key
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.pos.y -= self.speed * seconds
        # Down Key
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.pos.y += self.speed * seconds
        # Left Key
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.pos.x -= self.speed * seconds
        # Right Key
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.pos.x += self.speed * seconds
        
        player_rect = pygame.Rect(self.pos.x, self.pos.y, self.size[0], self.size[1])
        for shelf in shelves:
            if player_rect.colliderect(shelf.rect):
                self.pos.x = old_x
        for shelf in shelves:
            if player_rect.colliderect(shelf.rect):
                self.pos.y = old_y
    
    
    def check_bounds(self, screen_w, screen_h):
        if self.pos.x < 0: self.pos.x = 0
        if self.pos.x > screen_w - self.size[0]: self.pos.x = screen_w - self.size[0]
        if self.pos.y < 0: self.pos.y = 0
        if self.pos.y > screen_h - self.size[1]: self.pos.y = screen_h - self.size[1]
    def draw(self, screen):
        pygame.draw.rect(screen, yellow, (self.pos.x, self.pos.y, self.size[0], self.size[1]))

     
class shelf:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        pygame.draw.rect(screen, brown, self.rect)




def main():
    pygame.init()
    pygame.display.set_caption("Shopping at 1KEA")

    resolution = (0,0)
    screen = pygame.display.set_mode(resolution, pygame.FULLSCREEN)
    width, height = screen.get_size()
    clock = pygame.time.Clock()
    dt = 0
    player = character(width//2, height//2)
    shelves = [
        shelf(200,200,100,200)
        shelf(600,400,300,50)
    ]
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
        player.move(dt, shelves)
        player.check_bounds(width, height)
        screen.fill(blue)
        for s in shelves:
            s.draw(screen)
        player.draw(screen)
        pygame.display.flip()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()