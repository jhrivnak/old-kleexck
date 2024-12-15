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
        self.text_display_1 = ""
        self.text_display_2 = ""
        self.text_index_1 = 0
        self.text_index_2 = 0
        self.text_speed = 0.05
        self.last_text_update_1 = time.time()
        self.last_text_update_2 = time.time()
        self.text_done_1 = False
        self.text_done_2 = False
        self.played_greet_sound = False
        self.played_beg_sound = False
        self.show_second_text = False
        self.fade_start = None
        self.dead_fade_duration = 3
        self.conversation_stage = 0
        self.show_text = False
        self.load_assets()
        
    def load_assets(self):
        self.image = pygame.image.load(f"{IMG_PATH}creatures/greeter.png")
        self.greet_sound = pygame.mixer.Sound(f"{AUDIO_PATH}creatures/greeter/greeter-greet.ogg")
        self.beg_sound = pygame.mixer.Sound(f"{AUDIO_PATH}creatures/greeter/greeter-beg.ogg")
        self.oof_sounds = [pygame.mixer.Sound(f"{AUDIO_PATH}creatures/greeter/greeter-oof{i}.ogg") 
                          for i in range(1, 4)]
        self.death_sound = pygame.mixer.Sound(f"{AUDIO_PATH}creatures/greeter/greeter-death.ogg")
        
    def update(self, dt, player):
        dist_to_player = ((player.x - self.x)**2 + (player.y - self.y)**2)**0.5
        if dist_to_player < 100 and self.hp > 0:
            if self.conversation_stage == 0 and not self.show_text:
                self.show_text = True
                self.text_display_1 = ""
                self.text_index_1 = 0
                self.text_done_1 = False
                self.played_greet_sound = False
                
    def draw(self, screen):
        if self.hp > 0 or (self.fade_start and time.time() - self.fade_start < self.dead_fade_duration):
            alpha = 255
            if self.fade_start:
                elapsed = time.time() - self.fade_start
                alpha = max(0, 255 - int((elapsed/self.dead_fade_duration)*255))
            
            temp_surface = self.image.copy()
            temp_surface.set_alpha(alpha)
            screen.blit(temp_surface, (self.x, self.y))
            
            if self.show_text:
                self.draw_dialogue(screen)
                
    def draw_dialogue(self, screen):
        if not self.show_second_text:
            # Play greet sound when starting first dialogue
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
                            
            if self.text_display_1:
                text_surf = font.render(self.text_display_1, True, (255,255,255))
                text_rect = text_surf.get_rect(midbottom=(self.x + self.image.get_width()//2, self.y))
                screen.blit(text_surf, text_rect)
                
        elif self.show_second_text:
            # Play beg sound when starting second dialogue
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
                            
            if self.text_display_2:
                text_surf2 = font.render(self.text_display_2, True, (255,255,255))
                text_rect2 = text_surf2.get_rect(midbottom=(self.x + self.image.get_width()//2, self.y - 20))
                screen.blit(text_surf2, text_rect2)

    def take_damage(self):
        """Called when greeter is hit by a bullet"""
        if self.hp > 0:
            if self.hp > 10:
                random.choice(self.oof_sounds).play()
            else:
                self.death_sound.play()
                self.fade_start = time.time()