from PIL import Image
import pygame
import sys
import os

blue = (0, 81, 186)
yellow = (255, 218, 0)
brown = (101, 67, 33)
exterior = "parking lot"
interior = "marketplace"

class character:
    def __init__(self, x, y, images):
        self.pos = pygame.Vector2(x, y)
        self.size = [70, 45]
        self.images = images
        self.speed = 200
        # Default starting position
        self.direction = "down"

    # Defining how user moves using keys
    def move(self, dt, obstacles):
        seconds = dt / 1000
        keys = pygame.key.get_pressed()

        # Store position if shelf is in front
        old_x = self.pos.x
        old_y = self.pos.y

        # Up Key
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.pos.y -= self.speed * seconds
            self.direction = "up"
        # Down Key
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.pos.y += self.speed * seconds
            self.direction = "down"
        # Left Key
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.pos.x -= self.speed * seconds
            self.direction = "left"
        # Right Key
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.pos.x += self.speed * seconds
            self.direction = "right"
        
        player_rect = pygame.Rect(self.pos.x, self.pos.y, self.size[0], self.size[1])
        for obj in obstacles:
            if player_rect.colliderect(obj.rect):
                self.pos.x = old_x
        for obj in obstacles:
            if player_rect.colliderect(obj.rect):
                self.pos.y = old_y

    def draw(self, screen):
        # Draw iamge based on direction user is going
        current_image = self.images[self.direction]
        screen.blit(current_image, (self.pos.x, self.pos.y))
    
    def check_bounds(self, screen_w, screen_h):
        if self.pos.x < 0: self.pos.x = 0
        if self.pos.x > screen_w - self.size[0]: self.pos.x = screen_w - self.size[0]
        if self.pos.y < 0: self.pos.y = 0
        if self.pos.y > screen_h - self.size[1]: self.pos.y = screen_h - self.size[1]
    #def draw(self, screen):
        #pygame.draw.rect(screen, yellow, (self.pos.x, self.pos.y, self.size[0], self.size[1]))


class shelf:
    def __init__(self, x, y, width, height, color=yellow):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, brown, self.rect)


class items:
    def __init__(self, x, y, image, name):
        self.rect = pygame.Rect(x, y, 50, 50)
        self.image = image
        self.name = name
        self.collected = False

    def draw(self, screen):
        if not self.collected:
            screen.blit(self.image, (self.rect.x, self.rect.y))

def main():
    pygame.init()
    pygame.display.set_caption("Shopping at 1KEA")

    resolution = (0,0)
    screen = pygame.display.set_mode(resolution, pygame.FULLSCREEN)
    width, height = screen.get_size()
    clock = pygame.time.Clock()
    base_path = os.path.dirname(os.path.abspath(__file__))

    def load(filename, alpha=False, size=None):
        path = os.path.join(base_path, filename)
        pil_img = Image.open(path)
        # Convert alpha for transparency on shark
        if alpha:
            py_img = pygame.image.fromstring(pil_img.convert("RGBA").tobytes(), pil_img.size, "RGBA")
        else:
            py_img = pygame.image.fromstring(pil_img.convert("RGB").tobytes(), pil_img.size, "RGB")
        if size:
            return pygame.transform.scale(py_img, size)
        return pygame.transform.scale(py_img, (width, height))
    
    
    char_size = (85,60)

    # Import shark images
    shark_images = {
        "up": load("shark_back.png", alpha=True, size=char_size),
        "down": load("shark_front.png", alpha=True, size=char_size),
        "left": load("shark_left.png", alpha=True, size=char_size),
        "right": load("shark_right.png", alpha=True, size=char_size)
    }

    for key in shark_images:
        shark_images[key] = pygame.transform.scale(shark_images[key], char_size)
    
    # Items list
    inventory = []
    bag_img = load("itemsbag.png", alpha=True, size=(70,80))
    bear_img = load("itemsbear.png", alpha=True, size=(80,100)) 
    shark_img = load("itemsshark.png", alpha=True, size=(90,80)) 
    
    items_in_store = [
        items(200, 240, bag_img, "1KEA bag"),
        items(820, 200, bear_img, "Djunkelskog"),
        items(1270, 230, shark_img, "Blahaj")
    ]

    # Import background assets with furniture
    try:
        bg_ext = load("exterior.png")
        bg_int = load("interior.png")
    except Exception as e:
        print(f"Error loading images: {e}")
        bg_ext =pygame.Surface((width, height))
        bg_ext.fill(blue)

    # Set starting screen as exterior
    current_scene = exterior
    player = character(width//2, height//2, shark_images)

    # Door mat trigger
    door_to_int = pygame.Rect(width//2 - 50, height//2 - 100, 100, 50)
    door_to_ext = pygame.Rect(30, 100, 50, 100)

    #Invisible walls for exterior
    obstacles_ext = [
        #Building
        shelf(454, 80, 822, 300),
        shelf(454, 350, 210, 103),
        shelf(808, 350, 468, 103),
        shelf(595, 575, 43, 64),
        shelf(433, 280, 10, 290),
        shelf(235, 280, 200, 10),
        shelf(235, 280, 10, 289),
        shelf(235, 646, 10, 220),
        shelf(293, 655, 210, 255),
        shelf(433, 560, 205, 10),
        shelf(834, 560, 430, 10),
        shelf(1254, 560, 10, 290),
        shelf(590, 767, 43, 70),
        shelf(568, 430, 32, 55),
        shelf(888, 767, 43, 70),
        #shelf(983, 880, 193, 39),
        shelf(1037, 767, 43, 70),
        ]
    # Invisible walls for interior
    obstacles_int = [
        shelf(0,0,100,100),
        shelf(100, 0, 1450, 220),
        shelf(90, 120, 93, 400),
        shelf(90, 620, 93, 305),
        shelf(289, 620, 93, 305),
        
        shelf(289, 120, 93, 400),
        shelf(488, 120, 93, 400),
        shelf(687, 120, 93, 400),
        shelf(930, 120, 108, 400),
        shelf(1150, 120, 100, 390),
        shelf(1375, 119, 135, 390),

        shelf(1393, 595, 30, 266),
        shelf(1430, 720, 150, 100),
        shelf(1435, 840, 30, 120),
        shelf(640, 805, 380, 100),
        shelf(1120, 590, 150, 100),
        shelf(1120, 690, 255, 80)
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
            player.move(dt, obstacles_ext)
            player.check_bounds(width, height)
            screen.blit(bg_ext, (0,0))

            for obj in obstacles_ext:
               obj.draw(screen)

            # Door triggers entry into interior 
            player_rect = pygame.Rect(player.pos.x, player.pos.y, player.size[0], player.size[1])
            if player_rect.colliderect(door_to_int):
                current_scene = interior
                player.pos = pygame.Vector2(width//3, height-200)
                
        elif current_scene == interior:
            player.move(dt, obstacles_int)
            player.check_bounds(width, height)
            screen.blit(bg_int, (0,0))

            for obj in obstacles_int:
                obj.draw(screen)

            player_rect = pygame.Rect(player.pos.x, player.pos.y, player.size[0], player.size[1])
            
            for item in items_in_store:
                if not item.collected:
                    item.draw(screen)
                    # Check if user touches item
                    if player_rect.colliderect(item.rect):
                        item.collected = True
                        inventory.append(item.name)
                        print(f"Collected: {item.name}! Inventory: {inventory}")
            
            
            
            if player_rect.colliderect(door_to_ext):
                current_scene = exterior
                player.pos = pygame.Vector2(width//2, height//2)
            
        player.draw(screen)
        pygame.display.flip()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()