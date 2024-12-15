import pygame

def transition_to_yard(music_muted):
    pygame.mixer.music.stop()
    pygame.mixer.music.load("assets/audio/music/yard.mp3")
    pygame.mixer.music.play(-1 if not music_muted else 0)

def transition_to_home(music_muted):
    pygame.mixer.music.stop()
    pygame.mixer.music.load("assets/audio/music/home.mp3")
    pygame.mixer.music.play(-1 if not music_muted else 0)

def draw_home(screen, font, player_rect, door_rect):
    screen.fill((0,0,0))
    pygame.draw.circle(screen, (100,100,100), (screen.get_width()//2, screen.get_height()//2), 200)
    pygame.draw.rect(screen, (150,75,0), door_rect)
    if player_rect.colliderect(door_rect):
        open_text = font.render("Open [F]", True, (255,255,255))
        screen.blit(open_text, (door_rect.x+door_rect.width//2 - 30, door_rect.y - 20))

def draw_yard(screen, font, player_rect, back_door_rect):
    screen.fill((0,200,0))
    pygame.draw.rect(screen, (139,69,19), (100,100,50,100))
    pygame.draw.circle(screen, (34,139,34), (200,200), 50)
    pygame.draw.rect(screen, (150,75,0), back_door_rect)
    if player_rect.colliderect(back_door_rect):
        back_text = font.render("Open [F]", True, (255,255,255))
        screen.blit(back_text, (back_door_rect.x+back_door_rect.width//2-30, back_door_rect.y - 20))
