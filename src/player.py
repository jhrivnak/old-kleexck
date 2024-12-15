import pygame

walk_frames = [
    pygame.image.load("assets/images/character/cutout_walk-1.png"),
    pygame.image.load("assets/images/character/cutout_walk-2.png"),
    pygame.image.load("assets/images/character/cutout_walk-3.png"),
    pygame.image.load("assets/images/character/cutout_walk-4.png"),
    pygame.image.load("assets/images/character/cutout_walk-5.png"),
    pygame.image.load("assets/images/character/cutout_walk-6.png"),
]
run_frames = [
    pygame.image.load("assets/images/character/cutout_run-1.png"),
    pygame.image.load("assets/images/character/cutout_run-2.png"),
    pygame.image.load("assets/images/character/cutout_run-3.png"),
    pygame.image.load("assets/images/character/cutout_run-4.png"),
    pygame.image.load("assets/images/character/cutout_run-5.png"),
    pygame.image.load("assets/images/character/cutout_run-6.png"),
]

current_frame = 0

def player_rect(px, py):
    # Make hitbox taller: 
    # Let's say the character is 32x32, we make a 32x64 rect starting at py-32 so feet at py
    return pygame.Rect(px, py-32, 32, 64)

def handle_input(keys, player_speed):
    running = False
    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
        running = True
    speed = player_speed * 1.5 if running else player_speed
    vx = 0
    vy = 0
    facing_right = True
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        vy = -speed
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        vy = speed
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        vx = -speed
        facing_right = False
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        vx = speed
        facing_right = True
    return vx, vy, facing_right, running

def advance_frame():
    global current_frame
    current_frame = (current_frame + 1) % 6

def draw_player(screen, px, py, facing_right, running):
    frames = run_frames if running else walk_frames
    frame_img = frames[current_frame]
    if not facing_right:
        frame_img = pygame.transform.flip(frame_img, True, False)
    screen.blit(frame_img, (px, py))
