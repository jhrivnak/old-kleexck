# src/greeter.py
import pygame, time, random
from .world import IMG_PATH, AUDIO_PATH, font

class Greeter:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hp = 75
        self.text_full_1 = "hello please kill me"
        self.text_full_2 = "please use this to kill me"
        self.text_full_3 = "here's some more ammo to kill me with"
        self.text_full_4 = "SKILL ISSUE DETECTED. here's some more ammo"
        self.text_display_1 = ""
        self.text_display_2 = ""
        self.text_display_3 = ""
        self.text_display_4 = ""
        self.text_index_1 = 0
        self.text_index_2 = 0
        self.text_index_3 = 0
        self.text_index_4 = 0
        self.text_speed = 0.05
        self.text_display_time = 4.0
        self.last_text_update_1 = time.time()
        self.last_text_update_2 = time.time()
        self.last_text_update_3 = time.time()
        self.text_done_1 = False
        self.text_done_2 = False
        self.text_done_3 = False
        self.text_finish_time = None
        self.played_greet_sound = False
        self.played_beg_sound = False
        self.played_skill_sound = False
        self.show_second_text = False
        self.show_ammo_dialogue = False
        self.ammo_dialogue_done = False
        self.fade_start = None
        self.dead_fade_duration = 3
        self.conversation_stage = 0
        self.show_text = False
        self.been_shot = False
        self.is_dead = False
        self.gun_placed = False
        self.blood_start_time = None
        self.blood_alpha = 0
        self.ammo_drops = 0
        self.load_assets()
        
    def load_assets(self):
        self.image = pygame.image.load(f"{IMG_PATH}creatures/greeter.png")
        self.blood_splat = pygame.transform.scale(
            pygame.image.load(f"{IMG_PATH}creatures/blood-splat.png"), 
            (50, 50)) 
    
        self.greet_sound = pygame.mixer.Sound(f"{AUDIO_PATH}creatures/greeter/greeter-greet.ogg")
        self.beg_sound = pygame.mixer.Sound(f"{AUDIO_PATH}creatures/greeter/greeter-beg.ogg")
        self.oof_sounds = [pygame.mixer.Sound(f"{AUDIO_PATH}creatures/greeter/greeter-oof{i}.ogg") 
                          for i in range(1, 4)]
        self.death_sound = pygame.mixer.Sound(f"{AUDIO_PATH}creatures/greeter/greeter-death.ogg")
        self.ammo_drop_sound = pygame.mixer.Sound(f"{AUDIO_PATH}effects/gun/ammoDrop.ogg")
        self.drop_sound = pygame.mixer.Sound(f"{AUDIO_PATH}effects/gun/drop.ogg")
        self.skill_issue_sound = pygame.mixer.Sound(f"{AUDIO_PATH}creatures/greeter/ammoGen.ogg")
        
    def update(self, dt, player):
        # Clear text after delay
        if self.text_finish_time and time.time() - self.text_finish_time > self.text_display_time:
            self.show_text = False
            self.show_second_text = False
            self.show_ammo_dialogue = False
            self.text_finish_time = None
            self.text_display_1 = ""
            self.text_display_2 = ""
            self.text_display_3 = ""
            self.text_done_3 = False
            self.text_index_3 = 0
            self.played_skill_sound = False  # Reset the skill sound flag

        dist_to_player = ((player.x - self.x)**2 + (player.y - self.y)**2)**0.5
        if dist_to_player < 100 and self.hp > 0:
            if self.conversation_stage == 0 and not self.show_text:
                self.show_text = True
                self.text_display_1 = ""
                self.text_index_1 = 0
                self.text_done_1 = False
                self.played_greet_sound = False
                
    def take_damage(self):
        """Called when greeter is hit by a bullet"""
        if self.hp > 0:
            self.been_shot = True
            if self.hp > 10:
                random.choice(self.oof_sounds).play()
            else:
                self.death_sound.play()  # It's here, should play greeter-death.ogg
                self.fade_start = time.time()
                self.is_dead = True
                self.blood_start_time = time.time() + 1
                self.blood_alpha = 0
                
    def draw(self, screen):
        # Draw the greeter sprite first (if alive)
        if not self.is_dead:
            screen.blit(self.image, (self.x, self.y))
            
        # Handle blood splat drawing with fade-in
        if self.is_dead and self.blood_start_time is not None:
            if time.time() > self.blood_start_time:
                # Fade in blood
                self.blood_alpha = min(255, self.blood_alpha + 10)
                blood_surface = self.blood_splat.copy()
                blood_surface.set_alpha(self.blood_alpha)
                # Center blood under where greeter was
                blood_x = self.x + (self.image.get_width() - self.blood_splat.get_width()) // 2
                blood_y = self.y + (self.image.get_height() - self.blood_splat.get_height()) // 2
                screen.blit(blood_surface, (blood_x, blood_y))
                
        # Draw dialogue if needed
        if self.show_text and not self.is_dead:
            self.draw_dialogue(screen)
            
    def draw_dialogue(self, screen):
        if not self.show_second_text and not self.show_ammo_dialogue:
            # First dialogue handling
            if not self.played_greet_sound:
                self.greet_sound.play()
                self.played_greet_sound = True

            if not self.text_done_1:
                if time.time() - self.last_text_update_1 > self.text_speed:
                    self.last_text_update_1 = time.time()
                    if self.text_index_1 < len(self.text_full_1):
                        self.text_display_1 += self.text_full_1[self.text_index_1]
                        self.text_index_1 += 1
                        if self.text_index_1 == len(self.text_full_1):
                            self.text_done_1 = True
                            self.text_finish_time = time.time()
                            
            if self.text_display_1:
                text_surf = font.render(self.text_display_1, True, (255,255,255))
                text_rect = text_surf.get_rect(midbottom=(self.x + self.image.get_width()//2, self.y))
                screen.blit(text_surf, text_rect)
                
        elif self.show_second_text:
            # Gun drop dialogue handling
            if not self.played_beg_sound:
                self.beg_sound.play()
                self.played_beg_sound = True

            if not self.text_done_2:
                if time.time() - self.last_text_update_2 > self.text_speed:
                    self.last_text_update_2 = time.time()
                    if self.text_index_2 < len(self.text_full_2):
                        self.text_display_2 += self.text_full_2[self.text_index_2]
                        self.text_index_2 += 1
                        if self.text_index_2 == len(self.text_full_2):
                            self.text_done_2 = True
                            self.drop_sound.play()
                            self.text_finish_time = time.time()
                            
            if self.text_display_2:
                text_surf2 = font.render(self.text_display_2, True, (255,255,255))
                text_rect2 = text_surf2.get_rect(midbottom=(self.x + self.image.get_width()//2, self.y - 20))
                screen.blit(text_surf2, text_rect2)
                
        elif self.show_ammo_dialogue:
            if not self.text_done_3:
                is_skill_issue = self.ammo_drops > 0
                current_text = self.text_full_4 if is_skill_issue else self.text_full_3
                
                # Play skill issue sound at start of dialogue if it's skill issue case
                if is_skill_issue and not self.played_skill_sound and self.text_display_3 == "":
                    self.skill_issue_sound.play()
                    self.played_skill_sound = True
                
                if time.time() - self.last_text_update_3 > self.text_speed:
                    self.last_text_update_3 = time.time()
                    if self.text_index_3 < len(current_text):
                        self.text_display_3 += current_text[self.text_index_3]
                        self.text_index_3 += 1
                        if self.text_index_3 == len(current_text):
                            self.text_done_3 = True
                            self.text_finish_time = time.time()
                    
            if self.text_display_3:
                text_surf3 = font.render(self.text_display_3, True, (255,255,255))
                text_rect3 = text_surf3.get_rect(midbottom=(self.x + self.image.get_width()//2, self.y - 20))
                screen.blit(text_surf3, text_rect3)