import pygame
import os
import sys

if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from src.world import font
else:
    try:
        from .world import font
    except ImportError:
        from world import font

class InteractableObject:
    def __init__(self, x, y, width, height, name):
        self.rect = pygame.Rect(x, y, width, height)
        self.name = name
        self.hover_font = pygame.font.SysFont(None, 20)
    
    def draw_hover_text(self, screen, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            text = self.hover_font.render(self.name, True, (0, 0, 0))
            outline = self.hover_font.render(self.name, True, (255, 255, 150))
            
            # Position text near mouse cursor but ensure it stays on screen
            text_width = text.get_width()
            text_height = text.get_height()
            text_x = min(mouse_pos[0] + 15, screen.get_width() - text_width - 10)
            text_y = min(max(mouse_pos[1] - 15, text_height), screen.get_height() - text_height - 10)
            
            # Draw outline by offsetting text slightly in each direction
            for dx, dy in [(-1,-1), (-1,1), (1,-1), (1,1)]:
                screen.blit(outline, (text_x + dx, text_y + dy))
            screen.blit(text, (text_x, text_y))

if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from src.main import run_game
    run_game()