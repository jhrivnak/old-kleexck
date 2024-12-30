import pygame
import sys
from .world import screen, screen_width, screen_height, clock, initialize_pygame
from .player import Player
from .levels.home.home import HomeLevel
from .levels.yard.yard import YardLevel
from .greeter import Greeter
from .game_state import GameState

def run_game():
    pygame.init()
    initialize_pygame()
    
    # Initialize game objects
    player = Player(screen_width//2, screen_height//2)
    home_level = HomeLevel()
    yard_level = YardLevel()
    greeter = Greeter(600, 300)
    
    current_level = home_level
    player.inventory.set_current_level(current_level)
    
    running = True
    
    while running:
        dt = clock.tick(60) / 1000.0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Handle level-specific events
            next_level = current_level.handle_event(event, player, player.gun, greeter)
            if next_level:
                current_level = yard_level if next_level == "yard" else home_level
                player.inventory.set_current_level(current_level)
        
        # Update
        GameState.get_instance().update_effects()
        player.update(dt)
        current_level.update(dt, player)
        
        # Draw
        screen.fill((0, 0, 0))
        current_level.draw(screen, player, player.gun, greeter)
        player.draw(screen)
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    run_game()