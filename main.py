import pygame, sys, time, random, math

pygame.init()
pygame.mixer.init()

# Global settings
sound_muted = False
music_muted = False
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 24)
font_large = pygame.font.SysFont(None, 48)

# Asset paths
BASE_PATH = "assets/"
IMG_PATH = BASE_PATH + "images/"
AUDIO_PATH = BASE_PATH + "audio/"

# Load images
walk_frames = [pygame.image.load(f"{IMG_PATH}character/cutout_walk-{i}.png") for i in range(1, 7)]
run_frames = [pygame.image.load(f"{IMG_PATH}character/cutout_run-{i}.png") for i in range(1, 7)]
greeter_img = pygame.image.load(f"{IMG_PATH}creatures/greeter.png")
gun_img = pygame.transform.scale(pygame.image.load(f"{IMG_PATH}items/gun.png"), (30,30))
bullet_img = pygame.transform.scale(pygame.image.load(f"{IMG_PATH}items/bullet.png"), (5,5))
bullets_img = pygame.transform.scale(pygame.image.load(f"{IMG_PATH}items/bullets.png"), (20,20))

heart_full = pygame.transform.scale(pygame.image.load(f"{IMG_PATH}character/heartFull.png"), (10,10))
heart_half = pygame.transform.scale(pygame.image.load(f"{IMG_PATH}character/heartHalf.png"), (10,10))
mana_full = pygame.transform.scale(pygame.image.load(f"{IMG_PATH}character/mana.png"), (10,10))
mana_half = pygame.transform.scale(pygame.image.load(f"{IMG_PATH}character/manaHalf.png"), (10,10))

# Load and start music
pygame.mixer.music.load(f"{AUDIO_PATH}music/home.mp3")
pygame.mixer.music.play(-1)

# Load sound effects
greeter_greet_sound = pygame.mixer.Sound(f"{AUDIO_PATH}creatures/greeter/greeter-greet.ogg")
greeter_beg_sound = pygame.mixer.Sound(f"{AUDIO_PATH}creatures/greeter/greeter-beg.ogg")
greeter_oof_sounds = [pygame.mixer.Sound(f"{AUDIO_PATH}creatures/greeter/greeter-oof{i}.ogg") for i in range(1, 4)]
greeter_death_sound = pygame.mixer.Sound(f"{AUDIO_PATH}creatures/greeter/greeter-death.ogg")
gun_drop_sound = pygame.mixer.Sound(f"{AUDIO_PATH}effects/gun/drop.ogg")

gun_sounds = [pygame.mixer.Sound(f"{AUDIO_PATH}effects/gun/gunshot{i}.ogg") for i in range(1, 7)]
reload_sounds = [pygame.mixer.Sound(f"{AUDIO_PATH}effects/gun/reload{i}.ogg") for i in range(1, 7)]
no_ammo_sound = pygame.mixer.Sound(f"{AUDIO_PATH}effects/gun/noAmmo.ogg")

# Player settings
player_x, player_y = screen_width//2, screen_height//2
player_speed = 3
facing_right = True
frame_time = 0.5
last_frame_change = time.time()
current_frame = 0
running = False

# Game state
health = 12
mana = 6
inventory_ammo = 0
equipped_main_hand = None
magazine_size = 6
current_magazine = 0

# Gun handling
reloading = False
reload_start_time = 0
reload_total_time = 2.0
reload_interval = 0.4
reload_segment = 0
last_reload_sound_time = 0

# Greeter settings and conversation state
greeter_x, greeter_y = 200, 200
greeter_hp = 75
text_full_1 = "hello please kill me"
text_full_2 = "please use this to kill me"
text_display_1 = ""
text_display_2 = ""
text_index_1 = 0
text_index_2 = 0
text_speed = 0.05
last_text_update_1 = time.time()
last_text_update_2 = time.time()
text_done_1 = False
text_done_2 = False
played_greet_sound = False
played_beg_sound = False
show_second_text = False
greeter_text_start_time = 0
greeter_second_text_start_time = 0
greeter_show_time = 4  # Changed to 4 seconds
talk_prompt = False
fade_start = None
dead_fade_duration = 3

# Game state flags
conversation_stage = 0
show_greeter_text = False
bullets_placed = False
gun_placed = False
picked_gun = False

# Game objects
gun_x, gun_y = greeter_x+60, greeter_y
gun_rect = pygame.Rect(gun_x, gun_y, 30, 30)
bullets_x, bullets_y = greeter_x+100, greeter_y
bullets_rect = pygame.Rect(bullets_x, bullets_y, 20, 20)
door_width, door_height = 100, 100
door_rect = pygame.Rect(screen_width//2 - door_width//2, 200, door_width, door_height)
back_door_rect = pygame.Rect(screen_width-110, 200, 100, 100)

# UI state
character_sheet_open = False
backpack_slots = 12

# Level handling
current_level = "home"
player_rect = pygame.Rect(player_x, player_y, 32, 32)
bullets_fired = []
bullets_velocity = []

def reload_gun():
    global current_magazine, reloading, reload_start_time, reload_segment, last_reload_sound_time
    if not picked_gun:
        return
    needed = magazine_size - current_magazine
    if inventory_ammo <= 0 and current_magazine == 0:
        return
    if inventory_ammo < needed:
        needed = inventory_ammo
    current_magazine += needed
    set_ammo(inventory_ammo - needed)
    reloading = True
    reload_start_time = time.time()
    reload_segment = 0
    last_reload_sound_time = reload_start_time

def set_ammo(a):
    global inventory_ammo
    inventory_ammo = a
    if inventory_ammo < 0:
        inventory_ammo = 0

def shoot_bullet(target_x, target_y):
    global current_magazine
    if not picked_gun or reloading:
        return
    if current_magazine <= 0:
        if inventory_ammo == 0:
            if not sound_muted:
                no_ammo_sound.play()
            return
        reload_gun()
        return
    
    current_magazine -= 1
    angle = math.atan2(target_y - (player_y+16), target_x - (player_x+16))
    speed = 10
    vx = math.cos(angle)*speed
    vy = math.sin(angle)*speed
    rect = pygame.Rect(player_x+16, player_y+16, 5,5)
    bullets_fired.append(rect)
    bullets_velocity.append((vx, vy))
    if not sound_muted:
        random.choice(gun_sounds).play()
    if current_magazine == 0:
        reload_gun()

def draw_hud():
    hearts_to_draw = health // 2
    half_heart_rem = (health % 2) != 0
    x_offset = 10
    y_offset = screen_height - 40
    for i in range(hearts_to_draw):
        screen.blit(heart_full, (x_offset + i*12, y_offset))
    if half_heart_rem:
        screen.blit(heart_half, (x_offset + hearts_to_draw*12, y_offset))

    manas_to_draw = mana // 2
    half_mana = (mana % 2) != 0
    x_offset_m = 10
    y_offset_m = y_offset + 12
    for i in range(manas_to_draw):
        screen.blit(mana_full, (x_offset_m + i*12, y_offset_m))
    if half_mana:
        screen.blit(mana_half, (x_offset_m + manas_to_draw*12, y_offset_m))

    if picked_gun:
        x_offset_gun = 10
        y_offset_gun = y_offset - 20
        screen.blit(gun_img, (x_offset_gun, y_offset_gun))
        ammo_text = f"{current_magazine}:{inventory_ammo}"
        at_surf = font.render(ammo_text, True, (255,255,255))
        screen.blit(at_surf, (x_offset_gun+35, y_offset_gun+5))

def transition_to_yard():
    global current_level, player_x, player_y, player_rect
    current_level = "yard"
    pygame.mixer.music.stop()
    pygame.mixer.music.load(f"{AUDIO_PATH}music/yard.mp3")
    pygame.mixer.music.play(-1 if not music_muted else 0)
    player_x, player_y = 50, screen_height//2
    player_rect.x, player_rect.y = player_x, player_y

def transition_to_home():
    global current_level, player_x, player_y, player_rect, conversation_stage, show_greeter_text, text_done_1
    global text_done_2, greeter_text_start_time
    current_level = "home"
    pygame.mixer.music.stop()
    pygame.mixer.music.load(f"{AUDIO_PATH}music/home.mp3")
    pygame.mixer.music.play(-1 if not music_muted else 0)
    player_x, player_y = screen_width//2, screen_height//2
    player_rect.x, player_rect.y = player_x, player_y
    # Reset conversation state when going home
    conversation_stage = 0
    show_greeter_text = False
    text_done_1 = False
    text_done_2 = False
    greeter_text_start_time = 0

while True:
    dt = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = pygame.mouse.get_pos()
            shoot_bullet(mx, my)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s and (event.mod & pygame.KMOD_CTRL):
                sound_muted = not sound_muted
                vol = 0 if sound_muted else 1
                greeter_greet_sound.set_volume(vol)
                greeter_beg_sound.set_volume(vol)
                greeter_death_sound.set_volume(vol)
                no_ammo_sound.set_volume(vol)
                gun_drop_sound.set_volume(vol)
                for s in gun_sounds:
                    s.set_volume(vol)
                for s in reload_sounds:
                    s.set_volume(vol)
                for s in greeter_oof_sounds:
                    s.set_volume(vol)
            if event.key == pygame.K_m and (event.mod & pygame.KMOD_CTRL):
                music_muted = not music_muted
                pygame.mixer.music.set_volume(0 if music_muted else 1)
            if event.key == pygame.K_c:
                character_sheet_open = not character_sheet_open

            if event.key == pygame.K_f:
                if current_level == "yard" and talk_prompt and greeter_hp > 0:
                    now = time.time()
                    
                    if conversation_stage == 0:
                        if text_done_1:
                            conversation_stage = 1
                            text_display_1 = ""  # Clear first message
                            show_second_text = True
                            text_display_2 = ""
                            text_index_2 = 0
                            text_done_2 = False
                            played_beg_sound = False
                            show_greeter_text = True
                            greeter_second_text_start_time = time.time()
                    elif conversation_stage == 1:
                        if text_done_2:
                            conversation_stage = 2
                            gun_placed = True
                            if not sound_muted:
                                gun_drop_sound.play()
                            show_greeter_text = False
                    elif conversation_stage == 2:
                        if gun_placed and not bullets_placed:
                            bullets_placed = True
                            conversation_stage = 3
                elif current_level == "home" and player_rect.colliderect(door_rect):
                    transition_to_yard()
                elif current_level == "yard" and player_rect.colliderect(back_door_rect):
                    transition_to_home()

            if event.key == pygame.K_r and picked_gun and not reloading:
                reload_gun()

    # Movement handling
    keys = pygame.key.get_pressed()
    vx, vy = 0, 0
    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
        running = True
    else:
        running = False
    speed = player_speed * 1.5 if running else player_speed
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

    player_x += vx
    player_y += vy
    player_x = max(0, min(player_x, screen_width-32))
    player_y = max(0, min(player_y, screen_height-32))
    player_rect.x = player_x
    player_rect.y = player_y

    # Greeter interaction check
    # Greeter interaction check
    if current_level == "yard":
        dist_to_greeter = math.hypot(player_rect.x - greeter_x, player_rect.y - greeter_y)
        if dist_to_greeter < 100 and greeter_hp > 0:
            if conversation_stage == 0 and not show_greeter_text:
                show_greeter_text = True
                greeter_text_start_time = time.time()
                text_display_1 = ""
                text_index_1 = 0
                text_done_1 = False
                played_greet_sound = False
            talk_prompt = True
        else:
            talk_prompt = False
    else:
        talk_prompt = False

    # Animation handling
    if (vx != 0 or vy != 0) and time.time() - last_frame_change > frame_time:
        last_frame_change = time.time()
        current_frame = (current_frame + 1) % 6

    frames = run_frames if running else walk_frames
    frame_img = frames[current_frame] if (vx != 0 or vy != 0) else frames[0]
    if not facing_right:
        frame_img = pygame.transform.flip(frame_img, True, False)

    # Drawing
    if current_level == "home":
        screen.fill((0,0,0))
        pygame.draw.circle(screen, (100,100,100), (screen_width//2, screen_height//2), 200)
        pygame.draw.rect(screen, (150,75,0), door_rect)
        if player_rect.colliderect(door_rect):
            open_text = font.render("Open [F]", True, (255,255,255))
            screen.blit(open_text, (door_rect.x+door_width//2 - 30, door_rect.y - 20))
    else:
        screen.fill((0,200,0))
        pygame.draw.rect(screen, (139,69,19), (100,100,50,100))
        pygame.draw.circle(screen, (34,139,34), (200,200), 50)
        pygame.draw.rect(screen, (150,75,0), back_door_rect)
        if player_rect.colliderect(back_door_rect):
            open_text = font.render("Open [F]", True, (255,255,255))
            screen.blit(open_text, (back_door_rect.x+back_door_rect.width//2-30, back_door_rect.y - 20))

        # Greeter rendering
        greeter_alpha = 255
        if fade_start is not None:
            elapsed = time.time() - fade_start
            if elapsed < dead_fade_duration:
                greeter_alpha = max(0, 255 - int((elapsed/dead_fade_duration)*255))
            else:
                greeter_alpha = 0
        if greeter_hp > 0 or greeter_alpha > 0:
            greeter_surf = greeter_img.copy()
            greeter_surf.set_alpha(greeter_alpha)
            screen.blit(greeter_surf, (greeter_x, greeter_y))
        if greeter_hp <= 0 and fade_start is None:
            fade_start = time.time()
            if not sound_muted:
                greeter_death_sound.play()

        # Text display
        if show_greeter_text:
            if not played_greet_sound and not show_second_text and not sound_muted:
                greeter_greet_sound.play()
                played_greet_sound = True
                
            # Handle first message
            if not show_second_text:
                if not text_done_1:
                    if time.time() - last_text_update_1 > text_speed and text_index_1 < len(text_full_1):
                        last_text_update_1 = time.time()
                        text_display_1 += text_full_1[text_index_1]
                        text_index_1 += 1
                        if text_index_1 == len(text_full_1):
                            text_done_1 = True
                            greeter_text_start_time = time.time()
                
                if text_display_1:
                    # Check if we should hide the text after delay
                    if text_done_1 and time.time() - greeter_text_start_time > greeter_show_time:
                        text_display_1 = ""
                    else:
                        text_surf = font.render(text_display_1, True, (255,255,255))
                        text_rect = text_surf.get_rect(midbottom=(greeter_x+greeter_img.get_width()//2, greeter_y))
                        screen.blit(text_surf, text_rect)

            # Handle second message
            if show_second_text:
                if not played_beg_sound and not sound_muted:
                    greeter_beg_sound.play()
                    played_beg_sound = True
                    
                if not text_done_2:
                    if time.time() - last_text_update_2 > text_speed and text_index_2 < len(text_full_2):
                        last_text_update_2 = time.time()
                        text_display_2 += text_full_2[text_index_2]
                        text_index_2 += 1
                        if text_index_2 == len(text_full_2):
                            text_done_2 = True
                            greeter_second_text_start_time = time.time()
                            
                if text_display_2:
                    # Check if we should hide the text after delay
                    if text_done_2 and time.time() - greeter_second_text_start_time > greeter_show_time:
                        text_display_2 = ""
                        show_greeter_text = False
                    else:
                        text_surf2 = font.render(text_display_2, True, (255,255,255))
                        text_rect2 = text_surf2.get_rect(midbottom=(greeter_x+greeter_img.get_width()//2, greeter_y - 20))
                        screen.blit(text_surf2, text_rect2)

        # Item placements
        if conversation_stage >= 2 and gun_placed and not picked_gun:
            screen.blit(gun_img, (gun_x, gun_y))
            gun_label = font.render("<gun>", True, (255,255,255))
            screen.blit(gun_label, (gun_x, gun_y - 15))
            if player_rect.colliderect(gun_rect):
                picked_gun = True
                equipped_main_hand = "Gun"
                current_magazine = magazine_size

        if conversation_stage >= 3 and bullets_placed:
            screen.blit(bullets_img, (bullets_x, bullets_y))
            ammo_label = font.render("<pistol ammo>", True, (255,255,255))
            screen.blit(ammo_label, (bullets_x, bullets_y - 15))
            if player_rect.colliderect(bullets_rect):
                set_ammo(inventory_ammo+12)
                bullets_placed = False

        # Bullet handling
        for i in range(len(bullets_fired)-1, -1, -1):
            b_rect = bullets_fired[i]
            vx, vy = bullets_velocity[i]
            b_rect.x += vx
            b_rect.y += vy
            if b_rect.x < 0 or b_rect.x > screen_width or b_rect.y < 0 or b_rect.y > screen_height:
                bullets_fired.pop(i)
                bullets_velocity.pop(i)
            else:
                screen.blit(bullet_img,(b_rect.x,b_rect.y))
                if greeter_hp > 0 and b_rect.colliderect(pygame.Rect(greeter_x,greeter_y,greeter_img.get_width(),greeter_img.get_height())):
                    bullets_fired.pop(i)
                    bullets_velocity.pop(i)
                    greeter_hp -= 10
                    if greeter_hp < 0:
                        greeter_hp = 0
                    if greeter_hp == 0:
                        fade_start = time.time()
                    else:
                        if not sound_muted:
                            random.choice(greeter_oof_sounds).play()

    # Player and UI elements
    screen.blit(frame_img, (player_x, player_y))

    if talk_prompt and greeter_hp > 0:
        talk_text = font.render("Talk [F]", True, (255,255,255))
        screen.blit(talk_text, (player_x, player_y - 40))

    if reloading:
        elapsed = time.time() - reload_start_time
        segments = int(elapsed // reload_interval)
        if segments > reload_segment and segments < 6:
            reload_segment = segments
            if not sound_muted:
                reload_sounds[reload_segment].play()
        if elapsed >= reload_total_time:
            reloading = False

    if picked_gun and current_magazine == 0 and not reloading and inventory_ammo > 0:
        reload_prompt = font.render("Reload [R]", True, (255,0,0))
        screen.blit(reload_prompt, (screen_width//2-50, screen_height-80))

    draw_hud()

    # Character sheet
    if character_sheet_open:
        sheet_bg = pygame.Surface((400,300))
        sheet_bg.fill((50,50,50))
        screen.blit(sheet_bg,(200,150))
        sheet_title = font_large.render("Character Sheet", True, (255,255,255))
        screen.blit(sheet_title,(200+100,150+10))
        main_hand_text = font.render(f"Main Hand: {equipped_main_hand if equipped_main_hand else 'None'}", True, (255,255,255))
        screen.blit(main_hand_text,(200+20,150+60))
        inv_text = font.render("Backpack (12 slots):", True, (255,255,255))
        screen.blit(inv_text,(200+20,150+100))

    pygame.display.flip()