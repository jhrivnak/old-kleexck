import pygame

heart_full = pygame.image.load("assets/images/character/heartFull.png")
heart_full = pygame.transform.scale(heart_full,(10,10))
heart_half = pygame.image.load("assets/images/character/heartHalf.png")
heart_half = pygame.transform.scale(heart_half,(10,10))
mana_full = pygame.image.load("assets/images/character/mana.png")
mana_full = pygame.transform.scale(mana_full,(10,10))
mana_half = pygame.image.load("assets/images/character/manaHalf.png")
mana_half = pygame.transform.scale(mana_half,(10,10))

gun_img = pygame.image.load("assets/images/items/gun.png")
gun_img = pygame.transform.scale(gun_img,(50,50))

bullet_img = pygame.image.load("assets/images/items/bullet.png")
bullet_img = pygame.transform.scale(bullet_img,(10,10))

bullets_img = pygame.image.load("assets/images/items/bullets.png")
bullets_img = pygame.transform.scale(bullets_img,(30,30))

def draw_hud(screen, font, health, mana, picked_gun, current_magazine, inventory_ammo, screen_width, screen_height):
    hearts_to_draw = health // 2
    half_heart = (health % 2) != 0
    x_offset = 10
    y_offset = screen_height - 60
    for i in range(hearts_to_draw):
        screen.blit(heart_full, (x_offset + i*12, y_offset))
    if half_heart:
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
        y_offset_gun = y_offset - 40
        screen.blit(gun_img, (x_offset_gun, y_offset_gun))
        ammo_text = f"{current_magazine}:{inventory_ammo}"
        at_surf = font.render(ammo_text, True, (255,255,255))
        screen.blit(at_surf, (x_offset_gun+60, y_offset_gun+10))

def draw_item_label(screen, font, label, x, y):
    lbl = font.render(label, True, (255,255,255))
    screen.blit(lbl,(x, y-20))

def draw_bullets_img(screen, x, y):
    screen.blit(bullets_img,(x,y))

def draw_bullet_img(screen, x, y):
    screen.blit(bullet_img, (x,y))
