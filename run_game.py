import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pygame
from src.main import run_game

# Set window title and icon before running game
pygame.init()
pygame.display.set_caption("Kleexck")
icon = pygame.image.load("assets/images/infrastructure/icon.png")
pygame.display.set_icon(icon)

if __name__ == "__main__":
    run_game() 