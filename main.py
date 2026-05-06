import pygame
from random import randint, uniform

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load('images/player.png').convert_alpha()
        self.rect = self.image.get_frect(center =  (width / 2 , height - 100 ))
        self.direction = pygame.math.Vector2(1 , 1)
        self.speed = 300

        # cooldown
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 400
    
    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if  current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True

    def update(self, dt):
        keys = pygame.key.get_pressed()   
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])

        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt
        
        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            Laser(laser_surf, self.rect.midtop, all_sprite)
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()

        self.laser_timer()
        
class Star(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf
        self.rect =  self.image.get_frect(center= (randint(0, width),randint(0, height)))

class Laser(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)
        self.speed = 400

    def update(self, dt):
        self.rect.centery -= self.speed * dt
        if self.rect.bottom < 0:
            self.kill()

class Meteor(pygame.sprite.Sprite):
    def __init__(self, groups, surf, pos):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = pos)
        self.start_time = pygame.time.get_ticks()
        self.lifetime = 3000
        self.direction = pygame.Vector2(uniform(-0.5, 0.5), 1)
        self.speed = randint(400, 500)

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()

pygame.init()

height = 600
width = 900
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space invaders")

Clock = pygame.time.Clock()

# imports
star_surf = pygame.image.load('images/star.png').convert_alpha()
laser_surf = pygame.image.load('images/laser.png').convert_alpha()
meteor_surf = pygame.image.load('images/meteor.png').convert_alpha()

all_sprite = pygame.sprite.Group()

# sprite
for i in range(20):
    Star(all_sprite, star_surf)

player = Player(all_sprite)

# custom events -> meteor event
# interval timer
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)


running = True
while running:
    dt = Clock.tick() / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_event:
            x, y = randint(0, width), randint(-200 , -100)
            Meteor(all_sprite, meteor_surf, (x, y))

    # update
    all_sprite.update(dt)

    # drawings
    screen.fill('Dark gray') # this should be first shown

    all_sprite.draw(screen)

    pygame.display.update()
pygame.quit()