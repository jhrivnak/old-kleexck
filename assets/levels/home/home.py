# assets/levels/home/home.py
import pygame
from src.world import screen_width, screen_height, font

class HomeLevel:
    def __init__(self):
        self.door_rect = pygame.Rect(screen_width//2 - 50, 200, 100, 100)
        
    def handle_event(self, event, player, gun, greeter):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f and player.rect.colliderect(self.door_rect):
                return "yard"  # Signal to change level
        return None
        
    def update(self, dt):
        pass
        
    def draw(self, screen, player, gun, greeter):
        screen.fill((0,0,0))
        pygame.draw.circle(screen, (100,100,100), (screen_width//2, screen_height//2), 200)
        pygame.draw.rect(screen, (150,75,0), self.door_rect)
        
        if player.rect.colliderect(self.door_rect):
            open_text = font.render("Open [F]", True, (255,255,255))
            screen.blit(open_text, (self.door_rect.x + self.door_rect.width//2 - 30, 
                                  self.door_rect.y - 20))