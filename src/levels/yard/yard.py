# "C:\Users\jhriv\OneDrive\Desktop\kleexck\src\levels\yard\yard.py"
import pygame
import os
import sys

if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
    from src.world import IMG_PATH, screen_width, screen_height, font
else:
    try:
        from ...world import IMG_PATH, screen_width, screen_height, font
    except ImportError:
        from src.world import IMG_PATH, screen_width, screen_height, font

class YardLevel:
    def __init__(self):
        self.back_door_rect = pygame.Rect(screen_width-110, 200, 100, 100)
        self.gun_rect = None
        self.bullets_rect = None
        self.bullets_placed = False
        self.gun_placed = False
        self.bullets = []
        
    def handle_event(self, event, player, gun, greeter):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                # Handle back door
                if player.rect.colliderect(self.back_door_rect):
                    return "home"
                    
                # Handle greeter conversation - only if alive
                if self.is_near_greeter(player, greeter) and not greeter.is_dead:
                    if greeter.conversation_stage == 0 and greeter.text_done_1:
                        greeter.conversation_stage = 1
                        greeter.text_display_1 = ""
                        greeter.show_second_text = True
                        greeter.text_display_2 = ""
                        greeter.text_index_2 = 0
                        greeter.text_done_2 = False
                        greeter.played_beg_sound = False
                        greeter.show_text = True
                
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if gun.picked_up:
                mx, my = pygame.mouse.get_pos()
                new_bullet = gun.shoot(mx, my, player)
                if new_bullet:
                    self.bullets.append(new_bullet)
        return None

    def update(self, dt, player=None, gun=None, greeter=None):
        if greeter is None:
            return
            
        # Handle gun dropping when dialogue finishes
        if greeter.text_done_2 and not self.gun_placed and greeter.conversation_stage == 1:
            self.gun_placed = True
            greeter.conversation_stage = 2
            
        # Handle empty gun case and ammo drops - only if greeter is alive
        if (gun.picked_up and gun.current_magazine == 0 and gun.inventory_ammo == 0 and 
            not gun.reloading and not greeter.is_dead and not self.bullets_placed):
            greeter.show_text = True
            greeter.show_ammo_dialogue = True
            if greeter.text_done_3:
                self.bullets_placed = True
                greeter.ammo_drop_sound.play()
                greeter.ammo_drops += 1
        
        # Update bullets and check collisions
        for bullet in self.bullets[:]:
            bullet.update()
            
            if (bullet.rect.x < 0 or bullet.rect.x > screen_width or 
                bullet.rect.y < 0 or bullet.rect.y > screen_height):
                self.bullets.remove(bullet)
                continue
                
            if (bullet.rect.colliderect(pygame.Rect(greeter.x, greeter.y,
                                                  greeter.image.get_width(),
                                                  greeter.image.get_height()))):
                self.bullets.remove(bullet)
                if greeter.hp > 0:
                    greeter.hp -= 10
                    greeter.take_damage()
        
    def is_near_greeter(self, player, greeter):
        dist = ((player.rect.x - greeter.x)**2 + (player.rect.y - greeter.y)**2)**0.5
        return dist < 150
        
    def draw(self, screen, player, gun, greeter):
        # Draw background
        screen.fill((0,200,0))
        pygame.draw.rect(screen, (139,69,19), (100,100,50,100))
        pygame.draw.circle(screen, (34,139,34), (200,200), 50)
        
        # Draw back door
        pygame.draw.rect(screen, (150,75,0), self.back_door_rect)
        
        # Draw the Greeter
        greeter.draw(screen)
        
        # Draw items if placed
        if self.gun_placed and not gun.picked_up:
            screen.blit(gun.image, (greeter.x + 60, greeter.y))
            gun_label = font.render("<gun>", True, (255,255,255))
            screen.blit(gun_label, (greeter.x + 60, greeter.y - 15))
            self.gun_rect = pygame.Rect(
                greeter.x + 60 - 15,
                greeter.y - 15, 
                60,
                60
            )
            
            if player.rect.colliderect(self.gun_rect):
                gun.picked_up = True
                gun.current_magazine = gun.magazine_size
                
        if self.bullets_placed:
            screen.blit(gun.bullets_image, (greeter.x + 100, greeter.y))
            ammo_label = font.render("<pistol ammo>", True, (255,255,255))
            screen.blit(ammo_label, (greeter.x + 100, greeter.y - 15))
            self.bullets_rect = pygame.Rect(
                greeter.x + 100 - 15,
                greeter.y - 15,
                50,
                50
            )
            
            if player.rect.colliderect(self.bullets_rect):
                gun.inventory_ammo += 12
                self.bullets_placed = False

        # Draw back door prompt
        if player.rect.colliderect(self.back_door_rect):
            open_text = font.render("Open [F]", True, (255,255,255))
            screen.blit(open_text, (self.back_door_rect.x + self.back_door_rect.width//2 - 30,
                                  self.back_door_rect.y - 20))
        
        # Draw talk prompt ONLY if greeter is alive
        if self.is_near_greeter(player, greeter) and not greeter.is_dead:
            talk_text = font.render("Talk [F]", True, (255,255,255))
            screen.blit(talk_text, (player.rect.x, player.rect.y - 40))
            
        # Draw bullets
        for bullet in self.bullets:
            bullet.draw(screen)

if __name__ == "__main__":
    from main import run_game
    run_game()