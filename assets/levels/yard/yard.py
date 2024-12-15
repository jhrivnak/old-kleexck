import pygame

def draw_yard(screen, font, player_rect, back_door_rect, greeter_hp, greeter_x, greeter_y, fade_start, dead_fade_duration, greeter_img, gun_img, bullet_img, bullets_img, picked_gun, gun_rect, bullets_rect, bullets_placed, gun_visible):
    # Draw the yard level
    screen.fill((0,200,0))
    pygame.draw.rect(screen, (139,69,19), (100,100,50,100)) # Just a random object (a tree trunk?)
    pygame.draw.circle(screen, (34,139,34), (200,200), 50)  # a bush or tree top
    pygame.draw.rect(screen, (150,75,0), back_door_rect)
    if player_rect.colliderect(back_door_rect):
        open_text = font.render("Open [F]", True, (255,255,255))
        screen.blit(open_text, (back_door_rect.x+back_door_rect.width//2-30, back_door_rect.y - 20))

    if greeter_hp>0 and greeter_img:
        greeter_alpha=255
        if fade_start is not None:
            elapsed = pygame.time.get_ticks()/1000.0 - fade_start
            if elapsed<0:
                elapsed=0
            if elapsed<dead_fade_duration:
                greeter_alpha=max(0,255-int((elapsed/dead_fade_duration)*255))
            else:
                greeter_alpha=0
        greeter_surf=greeter_img.copy()
        greeter_surf.set_alpha(greeter_alpha)
        screen.blit(greeter_surf,(greeter_x,greeter_y))

    # Only show gun if we decided to make it visible after talking to greeter
    if gun_visible and not picked_gun:
        gt = font.render("<gun>", True, (255,255,255))
        screen.blit(gt,(gun_rect.x, gun_rect.y-20))
        screen.blit(gun_img,(gun_rect.x, gun_rect.y))

    if bullets_placed:
        bt = font.render("<pistol ammo>", True, (255,255,255))
        screen.blit(bt,(bullets_rect.x, bullets_rect.y-20))
        screen.blit(bullets_img,(bullets_rect.x, bullets_rect.y))

def yard_interact(px, py, gx, gy, show_greeter_text_once, show_greeter_text, show_second_text, text_done_1, text_done_2, bullets_placed, fade_start, greeter_hp, gun_visible, add_chat):
    # Currently no direct interactions coded here. Could be used to handle yard-specific interactions if needed.
    pass
