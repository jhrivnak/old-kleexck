import pygame, time, random

greeter_greet_sound = None
greeter_beg_sound = None
greeter_death_sound = None
greeter_oof_sounds = []
last_oof_played = None

text_full_1 = "hello please kill me"
text_full_2 = "please use this to kill me"

dialog_stage = 0

show_greeter_text = False
show_second_text = False
text_display_1 = ""
text_display_2 = ""
text_index_1 = 0
text_index_2 = 0
text_done_1 = False
text_done_2 = False
played_greet_sound = False
played_beg_sound = False
greeter_text_start_time = 0
greeter_second_text_start_time = 0
greeter_show_time = 3
line_delay_started = False
line_delay_start_time = 0
line_delay_duration = 1.0

greeter_img = pygame.image.load("assets/images/creatures/greeter.png")

def load_sounds():
    global greeter_greet_sound, greeter_beg_sound, greeter_death_sound, greeter_oof_sounds
    greeter_greet_sound = pygame.mixer.Sound("assets/audio/creatures/greeter/greeter-greet.ogg")
    greeter_beg_sound = pygame.mixer.Sound("assets/audio/creatures/greeter/greeter-beg.ogg")
    greeter_death_sound = pygame.mixer.Sound("assets/audio/creatures/greeter/greeter-death.ogg")
    greeter_oof_sounds = [
        pygame.mixer.Sound("assets/audio/creatures/greeter/greeter-oof1.ogg"),
        pygame.mixer.Sound("assets/audio/creatures/greeter/greeter-oof2.ogg"),
        pygame.mixer.Sound("assets/audio/creatures/greeter/greeter-oof3.ogg")
    ]

def set_volume(vol):
    greeter_greet_sound.set_volume(vol)
    greeter_beg_sound.set_volume(vol)
    greeter_death_sound.set_volume(vol)
    for s in greeter_oof_sounds:
        s.set_volume(vol)

def get_death_sound():
    return greeter_death_sound

def init_state():
    global dialog_stage, show_greeter_text, show_second_text, text_display_1, text_display_2
    global text_index_1, text_index_2, text_done_1, text_done_2, played_greet_sound, played_beg_sound
    global greeter_text_start_time, greeter_second_text_start_time, last_oof_played, line_delay_started
    global line_delay_start_time

    dialog_stage = 0
    show_greeter_text = True
    show_second_text = False
    text_display_1 = ""
    text_display_2 = ""
    text_index_1 = 0
    text_index_2 = 0
    text_done_1 = False
    text_done_2 = False
    played_greet_sound = False
    played_beg_sound = False
    greeter_text_start_time = time.time()
    greeter_second_text_start_time = 0
    last_oof_played = None
    line_delay_started = False
    line_delay_start_time = 0

def interact():
    global dialog_stage
    # If dialog_stage=0, we are in initial phase - interacting again might do nothing special
    # If dialog_stage=1 means lines done and gun placed, now give ammo on interact
    if dialog_stage == 1:
        return "give_ammo"
    return None

def start_second_line():
    global show_second_text, text_display_2, text_index_2, text_done_2, played_beg_sound, greeter_second_text_start_time
    show_second_text = True
    greeter_second_text_start_time = time.time()
    text_display_2 = ""
    text_index_2 = 0
    text_done_2 = False
    played_beg_sound = False

def damage_greeter(sound_muted):
    global last_oof_played
    choices = [s for s in greeter_oof_sounds if s != last_oof_played]
    if not choices:
        choices = greeter_oof_sounds
    chosen = random.choice(choices)
    if not sound_muted:
        chosen.play()
    last_oof_played = chosen

def play_death_sound(sound_muted):
    if not sound_muted:
        greeter_death_sound.play()

def get_greeter_rect(gx, gy):
    return pygame.Rect(gx, gy, greeter_img.get_width(), greeter_img.get_height())

def update_and_draw(screen, font, gx, gy, greeter_hp, fade_start,
                    picked_gun, gun_placed, bullets_placed,
                    sound_muted, set_ammo_func, inventory_ammo, magazine_size, current_magazine):
    global show_greeter_text, show_second_text, text_display_1, text_display_2
    global text_index_1, text_index_2, text_done_1, text_done_2
    global played_greet_sound, played_beg_sound, greeter_text_start_time, greeter_second_text_start_time
    global dialog_stage, line_delay_started, line_delay_start_time

    greeter_alpha=255
    dead_fade_duration=2
    if greeter_hp<=0 and fade_start is not None:
        elapsed = time.time()-fade_start
        if elapsed<dead_fade_duration:
            greeter_alpha=max(0,255-int((elapsed/dead_fade_duration)*255))
        else:
            greeter_alpha=0

    if greeter_alpha>0 and greeter_hp>0:
        screen.blit(greeter_img, (gx, gy))
    elif greeter_alpha>0 and greeter_hp==0:
        greeter_surf=greeter_img.copy()
        greeter_surf.set_alpha(greeter_alpha)
        screen.blit(greeter_surf,(gx,gy))

    text_speed = 0.05

    if dialog_stage == 0:
        # First line
        if greeter_hp>0 and show_greeter_text and not show_second_text:
            if not played_greet_sound and not sound_muted:
                greeter_greet_sound.play()
                played_greet_sound = True
            if not text_done_1:
                now = time.time()
                expected_index = int((now - greeter_text_start_time)/text_speed)
                while text_index_1 <= expected_index and text_index_1 < len(text_full_1):
                    text_display_1 += text_full_1[text_index_1]
                    text_index_1 += 1
                if text_index_1 == len(text_full_1):
                    text_done_1 = True

            if time.time() - greeter_text_start_time < greeter_show_time:
                if text_display_1:
                    text_surf = font.render(text_display_1, True, (255,255,255))
                    text_rect = text_surf.get_rect(midbottom=(gx+greeter_img.get_width()//2, gy))
                    screen.blit(text_surf, text_rect)
            else:
                # first line show time ended
                show_greeter_text = False
                # Start delay
                if not line_delay_started and text_done_1:
                    line_delay_started = True
                    line_delay_start_time = time.time()

        # After delay, start second line
        if line_delay_started and (time.time() - line_delay_start_time > line_delay_duration) and not show_second_text and text_done_1:
            # start second line
            show_second_text = True
            greeter_second_text_start_time = time.time()
            text_display_2 = ""
            text_index_2 = 0
            text_done_2 = False
            played_beg_sound = False

        # Second line
        if show_second_text:
            if not played_beg_sound and not sound_muted:
                greeter_beg_sound.play()
                played_beg_sound = True
            if not text_done_2:
                now = time.time()
                expected_index = int((now - greeter_second_text_start_time)/text_speed)
                while text_index_2 <= expected_index and text_index_2 < len(text_full_2):
                    text_display_2 += text_full_2[text_index_2]
                    text_index_2 += 1
                if text_index_2 == len(text_full_2):
                    text_done_2 = True

            if time.time() - greeter_second_text_start_time < greeter_show_time:
                if text_display_2:
                    text_surf2 = font.render(text_display_2, True, (255,255,255))
                    text_rect2 = text_surf2.get_rect(midbottom=(gx+greeter_img.get_width()//2, gy - 20))
                    screen.blit(text_surf2, text_rect2)
            else:
                # second line ended
                show_second_text = False
                if not gun_placed:
                    gun_placed = True
                dialog_stage = 1

    # dialog_stage=1 means next time player presses F, we give ammo directly

    return (text_display_1, text_display_2, text_done_1, text_done_2,
            played_greet_sound, played_beg_sound,
            greeter_hp, fade_start, gun_placed)
