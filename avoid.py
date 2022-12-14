import random

import pygame
from pygame.locals import(
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT
)

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800



hiscore = 0

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("raketti.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
        
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0,-5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0,5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5,0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5,0)
        
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT   
                 

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("kivi.png").convert()
        self.surf.set_colorkey((255,255,255),RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
                )
        )             
        self.speed = random.randint(5, 10)
        
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
            
class Star(pygame.sprite.Sprite):
    def __init__(self):
        super(Star, self).__init__()
        self.surf = pygame.image.load("tähti.png").convert()
        self.surf.set_colorkey((0,0,0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        
        
    def update(self):
        self.rect.move_ip(-5,0)
        if self.rect.right < 0:
            self.kill()
        
    
        
pygame.init()
pygame.display.set_caption("Väistä komeettaa")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)
ADDSTAR = pygame.USEREVENT + 2
pygame.time.set_timer(ADDSTAR, 1000)

player = Player()

enemies = pygame.sprite.Group()
stars = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

clock = pygame.time.Clock()

running = True

while running:
    hiscore +=1 
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
        
        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
            
        elif event.type == ADDSTAR:
            new_star = Star()
            stars.add(new_star)
            all_sprites.add(new_star)
            
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    
    enemies.update()
    stars.update()
    
    screen.fill((11,11,69))
    
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    
    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()
        running = False
    
     
 
    screen.blit(player.surf, player.rect)
    pygame.display.flip()

    clock.tick(60)

print("hiscore", hiscore)
