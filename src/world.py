# src/world.py
import pygame

pygame.init()
pygame.mixer.init()

screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 24)
font_large = pygame.font.SysFont(None, 48)

# Updated asset paths to match your tree
BASE_PATH = "assets/"  # No need for kleexck/ since we're running from project root
IMG_PATH = BASE_PATH + "images/"
AUDIO_PATH = BASE_PATH + "audio/"

def initialize_pygame():
    pygame.mixer.music.load(f"{AUDIO_PATH}music/home.mp3")
    pygame.mixer.music.play(-1)