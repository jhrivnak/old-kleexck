import pygame

def draw_character_sheet(screen, font, equipped_main_hand):
    sheet_bg = pygame.Surface((400,300))
    sheet_bg.fill((50,50,50))
    screen.blit(sheet_bg,(200,150))
    sheet_title = font.render("Character Sheet", True, (255,255,255))
    screen.blit(sheet_title,(300,160))
    main_hand_text = font.render(f"Main Hand: {equipped_main_hand if equipped_main_hand else 'None'}", True, (255,255,255))
    screen.blit(main_hand_text,(220,210))
    inv_text = font.render("Backpack (12 slots):", True, (255,255,255))
    screen.blit(inv_text,(220,250))
