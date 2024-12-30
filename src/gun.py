# src/gun.py
import pygame, math, random
import os
import sys
import json

if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from src.world import *
    from src.game_state import GameState
else:
    try:
        from .world import *
        from .game_state import GameState
    except ImportError:
        from world import *
        from game_state import GameState

def load_gun_data():
    """Load gun configurations from JSON file"""
    with open(os.path.join(os.path.dirname(__file__), 'data/guns.json'), 'r') as f:
        return json.load(f)

def create_gun(gun_id, starting_ammo=None):
    """Factory function to create a gun instance based on gun_id"""
    gun_data = load_gun_data()
    
    # Find the gun configuration that matches the ID
    gun_config = None
    for gun_type, config in gun_data.items():
        if config['id'] == gun_id:
            gun_config = config
            break
    
    if gun_config is None:
        raise ValueError(f"No gun found with ID: {gun_id}")
        
    return Gun(gun_config, starting_ammo)

class Gun:
    def __init__(self, gun_config, starting_ammo=None):
        # Load configuration from gun_config
        self.name = gun_config['name']
        self.magazine_size = gun_config['magazine_size']
        self.current_magazine = self.magazine_size
        self.inventory_ammo = starting_ammo if starting_ammo is not None else gun_config['starting_ammo']
        self.reloading = False
        self.reload_start_time = 0
        self.reload_total_time = gun_config['reload_time']
        self.reload_interval = gun_config['reload_interval']
        self.reload_segment = 0
        self.picked_up = False
        self.gun_config = gun_config  # Store the config for reference
        self.load_assets()
        
    def load_assets(self):
        # Define default paths - use absolute paths from world.py constants
        DEFAULT_IMAGE = os.path.join(IMG_PATH, "default.png")
        DEFAULT_AUDIO = os.path.join(AUDIO_PATH, "default.ogg")
        
        # Debug print to verify paths (you can remove these after confirming)
   #     print(f"Default image path: {DEFAULT_IMAGE}")
    #    print(f"Default audio path: {DEFAULT_AUDIO}")
        
        # Load images based on config with fallbacks
        try:
            self.image = pygame.transform.scale(
                pygame.image.load(f"{IMG_PATH}items/{self.gun_config['image']}"), (30, 30))
        except (pygame.error, FileNotFoundError):
            self.image = pygame.transform.scale(
                pygame.image.load(DEFAULT_IMAGE), (30, 30))
            
        try:
            self.bullet_image = pygame.transform.scale(
                pygame.image.load(f"{IMG_PATH}items/{self.gun_config['bullet_image']}"), (5, 5))
        except (pygame.error, FileNotFoundError):
            self.bullet_image = pygame.transform.scale(
                pygame.image.load(DEFAULT_IMAGE), (5, 5))
            
        try:
            self.bullets_image = pygame.transform.scale(
                pygame.image.load(f"{IMG_PATH}items/bullets.png"), (20, 20))
        except (pygame.error, FileNotFoundError):
            self.bullets_image = pygame.transform.scale(
                pygame.image.load(DEFAULT_IMAGE), (20, 20))
        
        # Load sound effects based on config with fallbacks
        sound_effects = self.gun_config['sound_effects']
        
        # Load gun sounds
        self.gun_sounds = []
        for i in range(1, 7):
            try:
                sound = pygame.mixer.Sound(f"{AUDIO_PATH}effects/gun/{sound_effects['shoot']}{i}.ogg")
            except (pygame.error, FileNotFoundError):
                sound = pygame.mixer.Sound(DEFAULT_AUDIO)
            self.gun_sounds.append(sound)
        
        # Load reload sounds
        self.reload_sounds = []
        for i in range(1, 7):
            try:
                sound = pygame.mixer.Sound(f"{AUDIO_PATH}effects/gun/{sound_effects['reload']}{i}.ogg")
            except (pygame.error, FileNotFoundError):
                sound = pygame.mixer.Sound(DEFAULT_AUDIO)
            self.reload_sounds.append(sound)
        
        # Load other sound effects
        try:
            self.no_ammo_sound = pygame.mixer.Sound(f"{AUDIO_PATH}effects/gun/{sound_effects['no_ammo']}.ogg")
        except (pygame.error, FileNotFoundError):
            self.no_ammo_sound = pygame.mixer.Sound(DEFAULT_AUDIO)
        
        try:
            self.drop_sound = pygame.mixer.Sound(f"{AUDIO_PATH}effects/gun/{sound_effects['drop']}.ogg")
        except (pygame.error, FileNotFoundError):
            self.drop_sound = pygame.mixer.Sound(DEFAULT_AUDIO)

    def reload(self):
        
        if not self.picked_up:
         #   print("Can't reload: Gun not picked up")
            return
        if self.reloading:
           # print("Already reloading")
            return
        if self.current_magazine >= self.magazine_size:
         #   print("Magazine already full!")
            return
        
        needed = self.magazine_size - self.current_magazine
        if self.inventory_ammo <= 0:
        #    print("No ammo available to reload")
            return
        
        if self.inventory_ammo < needed:
            needed = self.inventory_ammo
        
      # print(f"Starting reload: {needed} bullets")
        self.bullets_to_load = needed  # Store how many bullets we'll add
        self.inventory_ammo -= needed  # Subtract from inventory immediately
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
            
        bullet = Bullet(player.x + 16, player.y + 16, target_x, target_y)
        GameState.get_instance().add_bullet(bullet)
        return bullet
        
    def update(self, dt, player):
        # Handle reload key press
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            self.reload()

        # Handle reload animation
        if self.reloading:
            elapsed = (pygame.time.get_ticks() - self.reload_start_time) / 1000
            segments = int(elapsed // self.reload_interval)
            
            if segments > self.reload_segment and segments < 6:
                self.reload_segment = segments
                self.reload_sounds[self.reload_segment].play()
                
            if elapsed >= self.reload_total_time:
                #print("Reload complete!")
                self.current_magazine += self.bullets_to_load  # Add bullets only when reload is complete
                self.reloading = False
                self.reload_segment = 0

        # Update bullets and handle collisions
        game_state = GameState.get_instance()
        bullets_to_remove = []
        
        for bullet in game_state.active_bullets:
            bullet.update()
            
            # Remove bullets that are off screen
            if (bullet.rect.x < 0 or bullet.rect.x > screen_width or 
                bullet.rect.y < 0 or bullet.rect.y > screen_height):
                bullets_to_remove.append(bullet)
                continue
                
            # Check collisions with entities
            for entity in game_state.game_entities:
                # MUCH simpler collision check - only hit living entities
                if (not getattr(entity, 'is_dead', False) and  # Entity must be alive
                    entity.rect and                            # Must have a rect
                    bullet.rect.colliderect(entity.rect)):     # Must collide
                    if hasattr(entity, 'take_damage'):
                        entity.take_damage()
                    bullets_to_remove.append(bullet)
                    break
                    
        # Remove bullets that hit something or went off screen
        for bullet in bullets_to_remove:
            if bullet in game_state.active_bullets:
                game_state.active_bullets.remove(bullet)

class Bullet:
    def __init__(self, x, y, target_x, target_y):
        self.rect = pygame.Rect(x, y, 5, 5)
        angle = math.atan2(target_y - y, target_x - x)
        speed = 10
        self.velocity = (math.cos(angle) * speed, math.sin(angle) * speed)
        self.image = pygame.transform.scale(
            pygame.image.load(f"{IMG_PATH}items/bullet.png"), (5, 5))
        self.x = float(x)  # Store precise floating point positions
        self.y = float(y)
        
    def update(self):
        # Update using floating point positions for precise movement
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        # Update rect position from floating point position
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)

if __name__ == "__main__":
    from main import run_game
    run_game()