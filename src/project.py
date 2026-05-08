import pygame
import sys

blue = (0, 81, 186)
yellow = (255, 218, 0)
brown = (101, 67, 33)
exterior = "parking lot"
interior = "marketplace"

class character:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.size = [15, 15]
        self.speed = 200

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

    # Import background assets with furniture


    bg_int = pygame.image.load("interior.png")
    bg_int = pygame.transform.scale(bg_int, (width, height))
    # Set starting screen as exterior
    current_scene = exterior

    player = character(width//2, height//2)

    # Door mat trigger
    door = pygame.Rect(width//2 - 50, height//2 - 100, 100, 50)

    #Invisible walls for exterior
    obstacle = [
        #Building
        shelf(100, 400, 500,300), 
        #Sidewalk
        shelf(100, 330,450,20),
        #Items
        shelf(180, 700, 50, 50)
        ]
    # Invisible walls for interior
    shelves = [
        shelf(150, 200, 50, 150),
        shelf(400, 250, 150, 40),
        shelf(400, 400, 150, 40),
        shelf(650, 250, 150, 40),
        shelf(650, 400, 150, 40)
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
        if current_scene == exterior:
            player.move(dt, obstacle)
            player.check_bounds(width, height)
            screen.blit(bg_ext, (0,0))

            # Door triggers entry into interior 
            player_rect = pygame.Rect(player.pos.x, player.pos.y, player.size[0], player.size[1])
            if player_rect.colliderect(door):
                current_scene = interior
                player.pos = pygame.Vector2(width//2, height-50)
                
        elif current_scene == interior:
            player.move(dt, shelves)
            player.check_bounds(width, height)
            screen.blit(bg_int, (0,0))
            
        player.draw(screen)
        pygame.display.flip()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()