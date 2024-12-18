# "C:\Users\jhriv\OneDrive\Desktop\kleexck\src\levels\home\home.py"
import pygame
import os
import sys

# Add the src directory to the Python path when running directly
if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
    from src.world import IMG_PATH, screen_width, screen_height, font
else:
    try:
        from ...world import IMG_PATH, screen_width, screen_height, font
    except ImportError:
        from src.world import IMG_PATH, screen_width, screen_height, font

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

if __name__ == "__main__":
    from main import run_game
    run_game()