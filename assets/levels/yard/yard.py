# assets/levels/yard/yard.py
import pygame, random, time
from src.world import screen_width, screen_height, font

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
                    
                # Handle greeter conversation
                if self.is_near_greeter(player, greeter) and greeter.hp > 0:
                    if greeter.conversation_stage == 0 and greeter.text_done_1:
                        greeter.conversation_stage = 1
                        greeter.text_display_1 = ""
                        greeter.show_second_text = True
                        greeter.text_display_2 = ""
                        greeter.text_index_2 = 0
                        greeter.text_done_2 = False
                        greeter.played_beg_sound = False
                        greeter.show_text = True
                        
                    elif greeter.conversation_stage == 1 and greeter.text_done_2:
                        greeter.conversation_stage = 2
                        self.gun_placed = True
                        if not gun.picked_up:
                            gun.drop_sound.play()
                        greeter.show_text = False
                        
                    elif greeter.conversation_stage == 2 and self.gun_placed and not self.bullets_placed:
                        self.bullets_placed = True
                        greeter.conversation_stage = 3
                        
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if gun.picked_up:
                mx, my = pygame.mouse.get_pos()
                new_bullet = gun.shoot(mx, my, player)
                if new_bullet:
                    self.bullets.append(new_bullet)
        return None

    def update(self, dt, player=None, gun=None, greeter=None):
        # Update bullets and check collisions
        if greeter is None:  # Safety check
            return
            
        for bullet in self.bullets[:]:  # Use slice to avoid modifying list while iterating
            bullet.update()
            
            # Remove bullets that go off screen
            if (bullet.rect.x < 0 or bullet.rect.x > screen_width or 
                bullet.rect.y < 0 or bullet.rect.y > screen_height):
                self.bullets.remove(bullet)
                continue
                
            # Check greeter collision
            if (bullet.rect.colliderect(pygame.Rect(greeter.x, greeter.y,
                                                  greeter.image.get_width(),
                                                  greeter.image.get_height()))):
                self.bullets.remove(bullet)
                if greeter.hp > 0:
                    greeter.hp -= 10
                    greeter.take_damage()
        
    def is_near_greeter(self, player, greeter):
        dist = ((player.rect.x - greeter.x)**2 + (player.y - greeter.y)**2)**0.5
        return dist < 100
        
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
        if greeter.conversation_stage >= 2 and self.gun_placed and not gun.picked_up:
            screen.blit(gun.image, (greeter.x + 60, greeter.y))
            gun_label = font.render("<gun>", True, (255,255,255))
            screen.blit(gun_label, (greeter.x + 60, greeter.y - 15))
            self.gun_rect = pygame.Rect(greeter.x + 60, greeter.y, 30, 30)
            
            if player.rect.colliderect(self.gun_rect):
                gun.picked_up = True
                gun.current_magazine = gun.magazine_size
                
        if greeter.conversation_stage >= 3 and self.bullets_placed:
            screen.blit(gun.bullets_image, (greeter.x + 100, greeter.y))
            ammo_label = font.render("<pistol ammo>", True, (255,255,255))
            screen.blit(ammo_label, (greeter.x + 100, greeter.y - 15))
            self.bullets_rect = pygame.Rect(greeter.x + 100, greeter.y, 20, 20)
            
            if player.rect.colliderect(self.bullets_rect):
                gun.inventory_ammo += 12
                self.bullets_placed = False

        # Draw back door prompt
        if player.rect.colliderect(self.back_door_rect):
            open_text = font.render("Open [F]", True, (255,255,255))
            screen.blit(open_text, (self.back_door_rect.x + self.back_door_rect.width//2 - 30,
                                  self.back_door_rect.y - 20))
        
        # Draw talk prompt if near greeter
        if self.is_near_greeter(player, greeter) and greeter.hp > 0:
            talk_text = font.render("Talk [F]", True, (255,255,255))
            screen.blit(talk_text, (player.rect.x, player.rect.y - 40))
            
        # Draw bullets
        for bullet in self.bullets:
            bullet.draw(screen)