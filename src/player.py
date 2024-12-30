# src/player.py
import pygame
import time, random
from .world import screen_width, screen_height, IMG_PATH
try:
    from .world import IMG_PATH
except ImportError:
    from world import IMG_PATH

from .world import AUDIO_PATH, font
from .gun import create_gun
from .inventory import Inventory

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 3
        self.facing_right = True
        self.running = False
        self.health = 12
        self.mana = 6
        self.rect = pygame.Rect(x, y, 64, 64)
        
        # Test gun initialization
        self.gun = create_gun(1)  # Create a revolver with ID 1
        self.gun.picked_up = True
        
        self.load_animations()
        
        self.inventory = Inventory()
        
    def load_animations(self):
        self.walk_frames = [pygame.image.load(f"{IMG_PATH}character/cutout_walk-{i}.png") 
                           for i in range(1, 7)]
        self.run_frames = [pygame.image.load(f"{IMG_PATH}character/cutout_run-{i}.png") 
                          for i in range(1, 7)]
        self.current_frame = 0
        self.frame_time = 0.5
        self.last_frame_change = 0
        
    def update(self, dt):
        keys = pygame.key.get_pressed()
        vx, vy = 0, 0
        
        # Only process movement if not in dialog
        if not (self.inventory.visible or 
                (hasattr(self.inventory.current_level, 'showing_crack_options') and 
                 self.inventory.current_level.showing_crack_options)):
            self.running = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
            speed = self.speed * 1.5 if self.running else self.speed
            
            if keys[pygame.K_w]: vy = -speed
            if keys[pygame.K_s]: vy = speed
            if keys[pygame.K_a]: 
                vx = -speed
                self.facing_right = False
            if keys[pygame.K_d]: 
                vx = speed
                self.facing_right = True
                
            self.x = max(0, min(self.x + vx, screen_width - 64))
            self.y = max(0, min(self.y + vy, screen_height - 64))
            self.rect.x, self.rect.y = self.x, self.y
            
            # Animation update
            if (vx != 0 or vy != 0) and pygame.time.get_ticks() - self.last_frame_change > self.frame_time * 1000:
                self.last_frame_change = pygame.time.get_ticks()
                self.current_frame = (self.current_frame + 1) % 6
        
        # Always process non-movement keys
        if keys[pygame.K_r] and self.gun is not None:
            self.gun.reload()
        
        # Handle inventory
        if keys[pygame.K_i]:
            self.inventory.toggle()
        
        mouse_buttons = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        
        if self.inventory.visible:
            self.inventory.handle_click(mouse_pos, mouse_buttons[0])  # Left click
        
    def draw(self, screen):
        frames = self.run_frames if self.running else self.walk_frames
        frame_img = frames[self.current_frame] if (self.rect.x != self.x or self.rect.y != self.y) else frames[0]
        if not self.facing_right:
            frame_img = pygame.transform.flip(frame_img, True, False)
        screen.blit(frame_img, (self.x, self.y))
        
        self.inventory.draw(screen)
        
        
if __name__ == "__main__":
    from main import run_game
    run_game()