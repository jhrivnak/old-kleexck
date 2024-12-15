# main.py
import pygame, sys
from src.world import (
    initialize_pygame, 
    screen_width, 
    screen_height, 
    screen, 
    clock,
    AUDIO_PATH
)
from src.player import Player 
from src.gun import Gun, Bullet
from src.greeter import Greeter
from src.hud import HUD
from src.character_sheet import CharacterSheet
from assets.levels.home.home import HomeLevel
from assets.levels.yard.yard import YardLevel

# Initialize game
initialize_pygame()

# Create game objects
player = Player(screen_width//2, screen_height//2)
gun = Gun()
greeter = Greeter(200, 200)
hud = HUD()
character_sheet = CharacterSheet()

# Create levels
home_level = HomeLevel()
yard_level = YardLevel()
current_level = home_level

def main():
    global current_level
    
    while True:
        dt = clock.tick(60)/1000.0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    character_sheet.toggle()
                    
            # Handle level transitions
            next_level = current_level.handle_event(event, player, gun, greeter)
            if next_level == "yard":
                current_level = yard_level
                player.x, player.y = 50, screen_height//2
                player.rect.x, player.rect.y = player.x, player.y
                pygame.mixer.music.load(f"{AUDIO_PATH}music/yard.mp3")
                pygame.mixer.music.play(-1)
            elif next_level == "home":
                current_level = home_level
                player.x, player.y = screen_width//2, screen_height//2
                player.rect.x, player.rect.y = player.x, player.y
                pygame.mixer.music.load(f"{AUDIO_PATH}music/home.mp3")
                pygame.mixer.music.play(-1)
        
        # Update game state
        player.update(dt)
        gun.update(dt, player)
        greeter.update(dt, player)
        if isinstance(current_level, YardLevel):
            current_level.update(dt, player, gun, greeter)
        else:
            current_level.update(dt)
        
        # Draw everything
        current_level.draw(screen, player, gun, greeter)
        player.draw(screen)
        hud.draw(screen, player, gun)
        
        if character_sheet.is_open:
            character_sheet.draw(screen, player)
            
        pygame.display.flip()

if __name__ == "__main__":
    main()