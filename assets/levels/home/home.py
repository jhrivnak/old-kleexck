import pygame

def draw_home(screen, font, player_rect, door_rect):
    # Draw the home level
    screen.fill((0,0,0))
    pygame.draw.circle(screen, (100,100,100), (screen.get_width()//2, screen.get_height()//2), 200)
    pygame.draw.rect(screen, (150,75,0), door_rect)
    if player_rect.colliderect(door_rect):
        open_text = font.render("Open [F]", True, (255,255,255))
        screen.blit(open_text, (door_rect.x+door_rect.width//2 - 30, door_rect.y - 20))

def home_interact(px, py, door_rect, transition_to_yard):
    # If player is at the door and presses F, go to yard
    player_rect = pygame.Rect(px, py, 32,32)
    if player_rect.colliderect(door_rect):
        transition_to_yard()
