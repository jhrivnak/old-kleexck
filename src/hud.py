# src/hud.py
import pygame
from .world import screen_height, screen_width, font, IMG_PATH

class HUD:
    def __init__(self):
        self.heart_full = pygame.transform.scale(
            pygame.image.load(f"{IMG_PATH}character/heartFull.png"), (10,10))
        self.heart_half = pygame.transform.scale(
            pygame.image.load(f"{IMG_PATH}character/heartHalf.png"), (10,10))
        self.mana_full = pygame.transform.scale(
            pygame.image.load(f"{IMG_PATH}character/mana.png"), (10,10))
        self.mana_half = pygame.transform.scale(
            pygame.image.load(f"{IMG_PATH}character/manaHalf.png"), (10,10))
            
    def draw(self, screen, player, gun):
        # Draw health
        hearts_to_draw = player.health // 2
        half_heart_rem = (player.health % 2) != 0
        x_offset = 10
        y_offset = screen_height - 40
        
        for i in range(hearts_to_draw):
            screen.blit(self.heart_full, (x_offset + i*12, y_offset))
        if half_heart_rem:
            screen.blit(self.heart_half, (x_offset + hearts_to_draw*12, y_offset))
            
        # Draw mana
        manas_to_draw = player.mana // 2
        half_mana = (player.mana % 2) != 0
        x_offset_m = 10
        y_offset_m = y_offset + 12
        
        for i in range(manas_to_draw):
            screen.blit(self.mana_full, (x_offset_m + i*12, y_offset_m))
        if half_mana:
            screen.blit(self.mana_half, (x_offset_m + manas_to_draw*12, y_offset_m))
            
        # Draw gun/ammo info
        if gun.picked_up:
            x_offset_gun = 10
            y_offset_gun = y_offset - 20
            screen.blit(gun.image, (x_offset_gun, y_offset_gun))
            ammo_text = f"{gun.current_magazine}:{gun.inventory_ammo}"
            at_surf = font.render(ammo_text, True, (255,255,255))
            screen.blit(at_surf, (x_offset_gun+35, y_offset_gun+5))
            
        # Draw reload prompt
        if gun.picked_up and gun.current_magazine == 0 and not gun.reloading and gun.inventory_ammo > 0:
            reload_prompt = font.render("Reload [R]", True, (255,0,0))
            screen.blit(reload_prompt, (screen_width//2-50, screen_height-80))