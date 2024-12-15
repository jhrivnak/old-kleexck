import pygame


class HUD:
    def __init__(self):
        self.heart_full = pygame.image.load("assets/images/character/heartFull.png")
        self.heart_half = pygame.image.load("assets/images/character/heartHalf.png")
        self.mana_full = pygame.image.load("assets/images/character/mana.png")
        self.mana_half = pygame.image.load("assets/images/character/manaHalf.png")

    def draw(self, screen, health, mana, equipped_gun, ammo, inventory_ammo):
        x, y = 10, 10
        # Draw health
        for i in range(health // 2):
            screen.blit(self.heart_full, (x, y))
            x += 32
        if health % 2 == 1:
            screen.blit(self.heart_half, (x, y))
            x += 32

        # Draw mana
        x, y = 10, 50
        for i in range(mana // 2):
            screen.blit(self.mana_full, (x, y))
            x += 32
        if mana % 2 == 1:
            screen.blit(self.mana_half, (x, y))

        # Draw ammo if gun is equipped
        if equipped_gun:
            x, y = 10, 90
            gun_icon = pygame.image.load("assets/images/items/gun.png")
            gun_icon = pygame.transform.scale(gun_icon, (32, 32))
            screen.blit(gun_icon, (x, y))
            ammo_text = f"{ammo}:{inventory_ammo}"
            font = pygame.font.SysFont(None, 24)
            text_surface = font.render(ammo_text, True, (255, 255, 255))
            screen.blit(text_surface, (x + 40, y + 8))
