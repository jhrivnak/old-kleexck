# "C:\Users\jhriv\OneDrive\Desktop\kleexck\src\levels\home\home.py"
import pygame
import os
import sys
import time

# Add the src directory to the Python path when running directly
if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
    from src.world import IMG_PATH, screen_width, screen_height, font
    from src.game_state import GameState
else:
    try:
        from ...world import IMG_PATH, screen_width, screen_height, font
        from src.game_state import GameState
    except ImportError:
        from src.world import IMG_PATH, screen_width, screen_height, font
        from src.game_state import GameState

from src.game_objects import InteractableObject  # Use absolute import

class HomeLevel:
    def __init__(self):
        self.door_rect = pygame.Rect(screen_width//2 - 50, 5, 100, 100)
        # Load images from the current directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.door = pygame.image.load(os.path.join(current_dir, "door.png"))
        self.crack = pygame.image.load(os.path.join(current_dir, "crack.png"))
        self.bed = pygame.image.load(os.path.join(current_dir, "bed.png"))
        self.nightstand = pygame.image.load(os.path.join(current_dir, "nightstand.png"))
        
        # Scale images
        self.door = pygame.transform.scale(self.door, (100, 100))
        self.crack = pygame.transform.scale(self.crack, (80, 50))
        self.bed = pygame.transform.scale(self.bed, (200, 100))
        self.nightstand = pygame.transform.scale(self.nightstand, (100, 100))
        
        # Initialize bullets list
        self.bullets = []
        
        # Add crack rectangle for collision detection
        self.crack_rect = pygame.Rect(screen_width - 100, screen_height//2, 80, 50)
        self.showing_crack_options = False
        
        # Load door sound
        self.door_sound = pygame.mixer.Sound("assets/audio/effects/objects/door1.ogg")
        self.alarm_sound = pygame.mixer.Sound("assets/audio/effects/objects/alarm.ogg")
        self.bed_sound = pygame.mixer.Sound("assets/audio/effects/objects/bed.ogg")
        
        # Text animation variables
        self.current_text = ""
        self.target_text = ""
        self.text_char_index = 0
        self.last_char_time = 0
        self.char_delay = 0.033  # Faster text speed (was 0.05)
        self.text_box_padding = 10
        
        # Load sounds
        self.cough_sound = pygame.mixer.Sound(os.path.join(current_dir, "cough.ogg"))
        self.clink_sound = pygame.mixer.Sound(os.path.join(current_dir, "clink.ogg"))
        
        # Crack effect timer
        self.crack_effect_start = None
        self.crack_effect_duration = 30  # seconds
        self.crack_effect_active = False
        
        # Tooltip variables
        self.show_tooltip = False
        self.tooltip_text = [
            "[Low Quality Crack]",
            "Increases movement speed for 30 seconds",
            "Causes cancer"
        ]
        self.crack_visible = True  # Track if crack is visible on ground
        
        # Mouse hover text
        self.hover_text = None
        self.hover_font = pygame.font.SysFont(None, 20)
        
        # Create interactable objects
        self.door_object = InteractableObject(screen_width//2 - 50, 5, 100, 100, "Door to Yard")
        self.bed_object = InteractableObject(50, screen_height//2, 200, 100, "Bed")
        self.nightstand_object = InteractableObject(125, screen_height//2 - 60, 100, 100, "Nightstand")
        self.crack_object = InteractableObject(screen_width - 100, screen_height//2, 80, 50, "Low Quality Crack")
        
    def handle_event(self, event, player, gun, greeter):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f and player.rect.colliderect(self.door_rect):
                self.door_sound.play()
                return "yard"
            
            # Handle crack options - only if crack is still visible
            if self.showing_crack_options and self.crack_visible:
                if event.key == pygame.K_y:  # Smoke it
                    self.cough_sound.play()
                    self.target_text = "Smoked some crack\n* Movement speed increased!"
                    self.current_text = ""
                    self.text_char_index = 0
                    player.speed *= 1.2
                    GameState.get_instance().add_effect("crack_speed", 30, player)
                    GameState.get_instance().add_cancer(5)
                    self.crack_visible = False
                elif event.key == pygame.K_s:  # Store it
                    self.clink_sound.play()
                    player.inventory.add_item("crackpipe", self.crack)
                    self.crack_visible = False
                self.showing_crack_options = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if event.button == 1:  # Left click
                if self.bed_object.rect.collidepoint(mouse_pos):
                    self.bed_sound.play()
                elif self.nightstand_object.rect.collidepoint(mouse_pos):
                    self.alarm_sound.play()
                # Add shooting
                elif gun.picked_up:
                    new_bullet = gun.shoot(mouse_pos[0], mouse_pos[1], player)
                    if new_bullet:
                        self.bullets.append(new_bullet)
        return None
        
    def update(self, dt, player=None):
        # Handle text animation
        current_time = time.time()
        if self.target_text and current_time - self.last_char_time > self.char_delay:
            if self.text_char_index < len(self.target_text):
                self.current_text += self.target_text[self.text_char_index]
                self.text_char_index += 1
                self.last_char_time = current_time
        
        # Check crack effect timer
        if self.crack_effect_active and time.time() - self.crack_effect_start > self.crack_effect_duration:
            self.crack_effect_active = False
            self.target_text = "Low quality crack has worn off"
            self.current_text = ""
            self.text_char_index = 0
            if player:
                player.speed /= 1.2  # Return to normal speed
                
        # Update bullets
        for bullet in self.bullets[:]:
            bullet.update()
            # Remove bullets that are off screen
            if (bullet.rect.x < 0 or bullet.rect.x > screen_width or 
                bullet.rect.y < 0 or bullet.rect.y > screen_height):
                self.bullets.remove(bullet)
                
    def draw_text_box(self, screen, text, options=None, width=None):
        # Fixed position at bottom of screen
        box_height = 100  # Fixed height for text box
        box_margin = 20   # Margin from bottom/sides of screen
        
        # If width not specified, use most of screen width
        if width is None:
            width = screen_width - (box_margin * 2)
        
        # Create box at bottom of screen
        box_rect = pygame.Rect(
            box_margin,                          # x position
            screen_height - box_height - box_margin,  # y position
            width,                               # width
            box_height                           # height
        )
        
        # Draw text box background and border
        pygame.draw.rect(screen, (0, 0, 0), box_rect)  # Black background
        pygame.draw.rect(screen, (255, 255, 255), box_rect, 2)  # White border
        
        # Handle multi-line text
        lines = text.split('\n')
        line_height = font.get_height()
        
        # Draw each line of text
        for i, line in enumerate(lines):
            text_surface = font.render(line, True, (255, 255, 255))
            text_pos_x = box_rect.x + (width // 2) - (text_surface.get_width() // 2)
            text_pos_y = box_rect.y + 10 + (i * line_height)  # Add vertical spacing between lines
            screen.blit(text_surface, (text_pos_x, text_pos_y))
        
        # Draw options text below, if provided and text is fully revealed
        if options and self.current_text == self.target_text:
            # Convert [Y]es [N]o [S]tore to better format
            formatted_options = []
            if "[Y]es" in options:
                formatted_options.append("Y - Yes")
            if "[N]o" in options:
                formatted_options.append("N - No")
            if "[S]tore" in options:
                formatted_options.append("S - Store")
            
            options_text = "     ".join(formatted_options)  # Space them out nicely
            options_surface = font.render(options_text, True, (255, 255, 255))
            options_pos_x = box_rect.x + (width // 2) - (options_surface.get_width() // 2)
            options_pos_y = text_pos_y + (line_height * 3)  # Three line breaks before options
            screen.blit(options_surface, (options_pos_x, options_pos_y))

    def draw_tooltip(self, screen, mouse_pos):
        if not self.show_tooltip:
            return
        
        padding = 10
        line_height = font.get_height()
        max_width = max(font.size(line)[0] for line in self.tooltip_text)
        box_height = (line_height * len(self.tooltip_text)) + (padding * 2)
        
        # Position tooltip near mouse but ensure it stays on screen
        tooltip_x = min(mouse_pos[0], screen_width - max_width - padding * 2)
        tooltip_y = max(0, mouse_pos[1] - box_height - padding)
        
        # Draw tooltip background
        tooltip_rect = pygame.Rect(tooltip_x, tooltip_y, max_width + padding * 2, box_height)
        pygame.draw.rect(screen, (0, 0, 0), tooltip_rect)
        pygame.draw.rect(screen, (255, 255, 255), tooltip_rect, 1)
        
        # Draw tooltip text
        for i, line in enumerate(self.tooltip_text):
            text_surface = font.render(line, True, (255, 255, 255))
            screen.blit(text_surface, (tooltip_x + padding, tooltip_y + padding + (i * line_height)))

    def draw(self, screen, player, gun, greeter):
        self.player = player  # Store reference to player for item dropping
        # Draw background and environment first
        screen.fill((0,0,0))
        pygame.draw.circle(screen, (100,100,100), (screen_width//2, screen_height//2), 300)
        
        # Draw furniture and doors
        screen.blit(self.bed, (50, screen_height//2))
        screen.blit(self.nightstand, (125, screen_height//2 - 60))
        screen.blit(self.door, self.door_rect)
        
        # Only draw crack if it's visible
        if self.crack_visible:
            screen.blit(self.crack, self.crack_rect)
            
            # Draw hover text if mouse is over crack
            mouse_pos = pygame.mouse.get_pos()
            if self.crack_rect.collidepoint(mouse_pos):
                text = self.hover_font.render("Low Quality Crack", True, (0, 0, 0))
                outline = self.hover_font.render("Low Quality Crack", True, (255, 255, 150))
                
                # Position text near mouse cursor but ensure it stays on screen
                text_width = text.get_width()
                text_height = text.get_height()
                text_x = min(mouse_pos[0] + 15, screen_width - text_width - 10)
                text_y = min(max(mouse_pos[1] - 15, text_height), screen_height - text_height - 10)
                
                # Draw outline by offsetting text slightly in each direction
                for dx, dy in [(-1,-1), (-1,1), (1,-1), (1,1)]:
                    screen.blit(outline, (text_x + dx, text_y + dy))
                screen.blit(text, (text_x, text_y))
        
        # Handle text display - fix door text priority
        if player.rect.colliderect(self.door_rect):
            self.target_text = "Open door to outside [F]"
            if not self.current_text:
                self.current_text = ""
                self.text_char_index = 0
            self.draw_text_box(screen, self.current_text)
        elif self.crack_visible and player.rect.colliderect(self.crack_rect):  # Only show crack text if it exists
            if not self.target_text:
                self.target_text = "Smoke some crack?"
                self.current_text = ""
                self.text_char_index = 0
            
            self.showing_crack_options = True
            self.draw_text_box(screen, self.current_text, options="[Y]es  [N]o  [S]tore")
        else:
            self.target_text = ""
            self.current_text = ""
            self.showing_crack_options = False
        
        # Draw hover text for all objects
        mouse_pos = pygame.mouse.get_pos()
        self.door_object.draw_hover_text(screen, mouse_pos)
        self.bed_object.draw_hover_text(screen, mouse_pos)
        self.nightstand_object.draw_hover_text(screen, mouse_pos)
        if self.crack_visible:
            self.crack_object.draw_hover_text(screen, mouse_pos)
            
        # Draw bullets
        for bullet in self.bullets:
            bullet.draw(screen)

if __name__ == "__main__":
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
    from src.main import run_game
    run_game()