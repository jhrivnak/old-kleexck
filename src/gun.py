# src/gun.py
import pygame, math, random
from .world import IMG_PATH, AUDIO_PATH

class Gun:
    def __init__(self):
        self.magazine_size = 6
        self.current_magazine = 0
        self.inventory_ammo = 0
        self.reloading = False
        self.reload_start_time = 0
        self.reload_total_time = 2.0
        self.reload_interval = 0.4
        self.reload_segment = 0
        self.picked_up = False
        self.load_assets()
        
    # src/gun.py
    def load_assets(self):
        self.image = pygame.transform.scale(
            pygame.image.load(f"{IMG_PATH}items/gun.png"), (30, 30))
        self.bullet_image = pygame.transform.scale(
            pygame.image.load(f"{IMG_PATH}items/bullet.png"), (5, 5))
        self.bullets_image = pygame.transform.scale(
            pygame.image.load(f"{IMG_PATH}items/bullets.png"), (20, 20))
        self.gun_sounds = [pygame.mixer.Sound(f"{AUDIO_PATH}effects/gun/gunshot{i}.ogg") 
                        for i in range(1, 7)]
        self.reload_sounds = [pygame.mixer.Sound(f"{AUDIO_PATH}effects/gun/reload{i}.ogg") 
                            for i in range(1, 7)]
        self.no_ammo_sound = pygame.mixer.Sound(f"{AUDIO_PATH}effects/gun/noAmmo.ogg")
        self.drop_sound = pygame.mixer.Sound(f"{AUDIO_PATH}effects/gun/drop.ogg")  # Add this line
        
    def reload(self):
        if not self.picked_up or self.reloading:
            return
        needed = self.magazine_size - self.current_magazine
        if self.inventory_ammo <= 0 and self.current_magazine == 0:
            return
        if self.inventory_ammo < needed:
            needed = self.inventory_ammo
        self.current_magazine += needed
        self.inventory_ammo = max(0, self.inventory_ammo - needed)
        self.reloading = True
        self.reload_start_time = pygame.time.get_ticks()
        self.reload_segment = 0

    def shoot(self, target_x, target_y, player):
        if not self.picked_up or self.reloading:
            return None
        if self.current_magazine <= 0:
            if self.inventory_ammo == 0:
                self.no_ammo_sound.play()
                return None
            self.reload()
            return None
        
        self.current_magazine -= 1
        random.choice(self.gun_sounds).play()
        if self.current_magazine == 0:
            self.reload()
            
        return Bullet(player.x + 16, player.y + 16, target_x, target_y)
        
    def update(self, dt, player):
        if self.reloading:
            elapsed = (pygame.time.get_ticks() - self.reload_start_time) / 1000
            segments = int(elapsed // self.reload_interval)
            if segments > self.reload_segment and segments < 6:
                self.reload_segment = segments
                self.reload_sounds[self.reload_segment].play()
            if elapsed >= self.reload_total_time:
                self.reloading = False

class Bullet:
    def __init__(self, x, y, target_x, target_y):
        self.rect = pygame.Rect(x, y, 5, 5)
        angle = math.atan2(target_y - y, target_x - x)
        speed = 10
        self.velocity = (math.cos(angle) * speed, math.sin(angle) * speed)
        self.image = pygame.transform.scale(
            pygame.image.load(f"{IMG_PATH}items/bullet.png"), (5, 5))
        
    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)