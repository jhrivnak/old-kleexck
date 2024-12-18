# src/world.py
import pygame
import os

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Screen setup
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont(None, 24)
font_large = pygame.font.SysFont(None, 48)

# Paths
BASE_PATH = "assets/"
IMG_PATH = BASE_PATH + "images/"
AUDIO_PATH = BASE_PATH + "audio/"

# Make everything available globally
__all__ = [
    'screen_width', 'screen_height', 'screen', 'clock',
    'font', 'font_large',
    'IMG_PATH', 'AUDIO_PATH'
]

def initialize_pygame():
    pygame.mixer.music.load(f"{AUDIO_PATH}music/home.mp3")
    pygame.mixer.music.play(-1)

if __name__ == "__main__":
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from main import run_game
    run_game()