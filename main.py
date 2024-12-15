import pygame, sys, time, math
from src import player, greeter, gun, hud, world, character_sheet

pygame.init()
pygame.mixer.init()

gun.load_sounds()
greeter.load_sounds()

sound_muted = False
music_muted = False

screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 24)

pygame.mixer.music.load("assets/audio/music/home.mp3")
pygame.mixer.music.play(-1)

player_speed = 3

# Game state
in_outside = False
character_sheet_open = False
health = 12
mana = 6
inventory_ammo = 0
equipped_main_hand = None
picked_gun = False
magazine_size = 6
current_magazine = 0

# Reloading logic
reloading = False
reload_start_time = 0
reload_duration = 2
reload_sound_timer = 0
reload_sound_index = 0
reload_in_progress = False
pending_reload_ammo = 0  # Ammo that will be added after reload finishes

door_rect = pygame.Rect(screen_width//2 - 50, 100, 100, 100)
back_door_rect = pygame.Rect(100, screen_height//2 - 50, 100, 100)

greeter_x, greeter_y = screen_width//2, 200
greeter_hp = 75
fade_start = None
bullets_placed = False
gun_placed = False
talk_prompt = False

# Initialize greeter dialog
greeter.init_state()

gun_x, gun_y = greeter_x+60, greeter_y
gun_rect = pygame.Rect(gun_x, gun_y, 50, 50)
bullets_x, bullets_y = greeter_x+100, greeter_y
bullets_rect = pygame.Rect(bullets_x, bullets_y, 30, 30)

bullets_fired = []

frame_time = 0.5
last_frame_change = time.time()
facing_right = True
running = False
player_x, player_y = screen_width//2, screen_height//2

def set_ammo(a):
    global inventory_ammo
    inventory_ammo = a
    if inventory_ammo < 0:
        inventory_ammo = 0

while True:
    dt = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if picked_gun and not reloading:
                mx, my = pygame.mouse.get_pos()
                if current_magazine <= 0:
                    if not sound_muted:
                        gun.play_no_ammo()
                else:
                    current_magazine -= 1
                    angle = math.atan2(my - (player_y+16), mx - (player_x+16))
                    speed = 10
                    vx = math.cos(angle)*speed
                    vy = math.sin(angle)*speed
                    bullet_rect = pygame.Rect(player_x+16, player_y+16, 10,10)
                    bullets_fired.append((bullet_rect,vx,vy))
                    if not sound_muted:
                        gun.play_gunshot()
                    if current_magazine == 0:
                        needed = gun.reload_gun(inventory_ammo, magazine_size, current_magazine, sound_muted, reload_duration, set_ammo)
                        if needed is not None and needed > 0:
                            pending_reload_ammo = needed
                            reloading = True
                            reload_start_time = time.time()
                            reload_sound_timer = time.time()
                            reload_sound_index = 0
                            reload_in_progress = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s and (event.mod & pygame.KMOD_CTRL):
                sound_muted = not sound_muted
                vol = 0 if sound_muted else 1
                gun.set_volume(vol)
                greeter.set_volume(vol)
            if event.key == pygame.K_m and (event.mod & pygame.KMOD_CTRL):
                music_muted = not music_muted
                pygame.mixer.music.set_volume(0 if music_muted else 1)
            if event.key == pygame.K_c:
                character_sheet_open = not character_sheet_open
            if event.key == pygame.K_f:
                p_rect = player.player_rect(player_x, player_y)
                if not in_outside and p_rect.colliderect(door_rect):
                    in_outside = True
                    world.transition_to_yard(music_muted)
                    player_x, player_y = 50, screen_height//2
                elif in_outside and p_rect.colliderect(back_door_rect):
                    in_outside = False
                    world.transition_to_home(music_muted)
                    player_x, player_y = screen_width//2, screen_height//2
                else:
                    # Interact with greeter
                    dist = math.hypot(player_x - greeter_x, player_y - greeter_y)
                    if in_outside and dist < 100 and greeter_hp > 0:
                        action = greeter.interact()
                        if action == "show_second_text":
                            # Should not happen now because greeter handles logic internally
                            pass
                        elif action == "repeat_dialog":
                            # Already handled by greeter state
                            pass
                        elif action == "give_ammo":
                            # Give ammo if dialog done
                            set_ammo(inventory_ammo+12)
            if event.key == pygame.K_r and picked_gun and not reloading:
                if current_magazine < magazine_size and inventory_ammo>0:
                    needed = gun.reload_gun(inventory_ammo, magazine_size, current_magazine, sound_muted, reload_duration, set_ammo)
                    if needed is not None and needed > 0:
                        pending_reload_ammo = needed
                        reloading = True
                        reload_start_time = time.time()
                        reload_sound_timer = time.time()
                        reload_sound_index = 0
                        reload_in_progress = True

    keys = pygame.key.get_pressed()
    vx, vy, facing_right, running = player.handle_input(keys, player_speed)
    player_x += vx
    player_y += vy
    player_x = max(0, min(player_x, screen_width-32))
    player_y = max(0, min(player_y, screen_height-32))

    if (vx != 0 or vy != 0) and time.time() - last_frame_change > frame_time:
        last_frame_change = time.time()
        player.advance_frame()

    # Draw scene
    if not in_outside:
        world.draw_home(screen, font, player.player_rect(player_x, player_y), door_rect)
    else:
        world.draw_yard(screen, font, player.player_rect(player_x, player_y), back_door_rect)
        dist = math.hypot(player_x - greeter_x, player_y - greeter_y)
        talk_prompt = (dist < 100 and greeter_hp > 0)

        (text_display_1, text_display_2, text_done_1, text_done_2,
         played_greet_sound, played_beg_sound,
         greeter_hp, fade_start, gun_placed) = greeter.update_and_draw(
            screen, font, greeter_x, greeter_y, greeter_hp, fade_start,
            picked_gun, gun_placed, bullets_placed,
            sound_muted, set_ammo, inventory_ammo, magazine_size, current_magazine
        )

        # Gun pickup
        if gun_placed and not picked_gun:
            if player.player_rect(player_x, player_y).colliderect(gun_rect):
                # Only after reload done show ammo in gun
                set_ammo(inventory_ammo+6)
                picked_gun = True
                equipped_main_hand = "Gun"
                # Initially gun is empty, must reload first or start empty?
                # Let's start it empty and require reload or start full?
                # The user said gun placed after second line, let's give no ammo in mag to start:
                current_magazine = 0

        # Ammo pickup
        if bullets_placed:
            hud.draw_item_label(screen, font, "<pistol ammo>", bullets_x, bullets_y)
            hud.draw_bullets_img(screen, bullets_x, bullets_y)
            if player.player_rect(player_x, player_y).colliderect(bullets_rect):
                set_ammo(inventory_ammo+12)
                bullets_placed = False

        # Bullets fired
        i = len(bullets_fired)-1
        while i>=0:
            b_rect,b_vx,b_vy = bullets_fired[i]
            b_rect.x += b_vx
            b_rect.y += b_vy
            if b_rect.x < 0 or b_rect.x > screen_width or b_rect.y < 0 or b_rect.y > screen_height:
                bullets_fired.pop(i)
            else:
                hud.draw_bullet_img(screen, b_rect.x, b_rect.y)
                # Check hit greeter
                if greeter_hp>0 and b_rect.colliderect(greeter.get_greeter_rect(greeter_x, greeter_y)):
                    bullets_fired.pop(i)
                    greeter_hp -= 10
                    if greeter_hp <=0:
                        fade_start = time.time()
                        greeter.play_death_sound(sound_muted)
                    else:
                        greeter.damage_greeter(sound_muted)
            i-=1

    player.draw_player(screen, player_x, player_y, facing_right, running)

    # Reload logic
    if reloading:
        if time.time() - reload_start_time >= reload_duration:
            reloading = False
            reload_in_progress = False
            # Now apply the ammo increase
            if pending_reload_ammo > 0:
                current_magazine += pending_reload_ammo
                set_ammo(inventory_ammo - pending_reload_ammo)
                pending_reload_ammo = 0
        else:
            if reload_in_progress:
                now = time.time()
                segment_delay = 0.4
                if reload_sound_index<6 and now - reload_sound_timer>=segment_delay:
                    reload_sound_timer=now
                    if not sound_muted:
                        gun.play_reload_sound(reload_sound_index)
                    reload_sound_index+=1

    if picked_gun and current_magazine == 0 and not reloading:
        reload_prompt = font.render("Reload [R]", True, (255,0,0))
        screen.blit(reload_prompt, (screen_width//2-50, screen_height-80))

    hud.draw_hud(screen, font, health, mana, picked_gun, current_magazine, inventory_ammo, screen_width, screen_height)

    if in_outside and talk_prompt:
        talk_text = font.render("Talk [F]", True, (255,255,255))
        screen.blit(talk_text, (player_x, player_y - 40))

    if character_sheet_open:
        character_sheet.draw_character_sheet(screen, font, equipped_main_hand)

    pygame.display.flip()
