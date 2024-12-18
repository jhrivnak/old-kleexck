# src/character_sheet.py
import pygame
try:
    from .world import font, font_large
except ImportError:
    from world import font, font_large

class CharacterSheet:
    def __init__(self):
        self.is_open = False
        
    def toggle(self):
        self.is_open = not self.is_open
        
    def draw(self, screen, player):
        if not self.is_open:
            return
            
        sheet_bg = pygame.Surface((400,300))
        sheet_bg.fill((50,50,50))
        screen.blit(sheet_bg,(200,150))
        
        sheet_title = font_large.render("Character Sheet", True, (255,255,255))
        screen.blit(sheet_title,(300,160))
        
        main_hand_text = font.render(f"Main Hand: {'Gun' if player.gun else 'None'}", 
                                   True, (255,255,255))
        screen.blit(main_hand_text,(220,210))
        
        inv_text = font.render("Backpack (12 slots):", True, (255,255,255))
        screen.blit(inv_text,(220,250))

if __name__ == "__main__":
    import sys
    import os
    # Add the project root directory to Python path
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from main import run_game
    run_game()