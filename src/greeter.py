import pygame, random, time

class Greeter:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hp = 70
        self.triggered = False
        self.interacted = False
        self.dead = False
        self.fading = False
        self.fade_alpha = 255

        self.first_line = "please kill me"
        self.second_line = "use this to kill me"
        self.current_text = ""
        self.text_index = 0
        self.text_done = False
        self.text_timer = 0
        self.text_speed_ms = 50  # time in ms per character
        self.show_time = 3
        self.last_oof = None

        self.greet_sound = pygame.mixer.Sound("assets/audio/creatures/greeter/greeter-greet.ogg")
        self.beg_sound = pygame.mixer.Sound("assets/audio/creatures/greeter/greeter-beg.ogg")
        self.death_sound = pygame.mixer.Sound("assets/audio/creatures/greeter/greeter-death.ogg")
        self.oof_sounds = [
            pygame.mixer.Sound("assets/audio/creatures/greeter/greeter-oof1.ogg"),
            pygame.mixer.Sound("assets/audio/creatures/greeter/greeter-oof2.ogg"),
            pygame.mixer.Sound("assets/audio/creatures/greeter/greeter-oof3.ogg")
        ]

        self.image = pygame.image.load("assets/images/creatures/greeter.png")
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        self.line_start_time = 0

    def trigger(self):
        if not self.triggered and not self.dead:
            self.triggered = True
            self.text_timer = pygame.time.get_ticks()
            self.current_text = ""
            self.text_index = 0
            self.text_done = False
            self.greet_sound.play()
            # Line start time for reference if needed
            self.line_start_time = pygame.time.get_ticks()

    def interact(self):
        # Only interact if first line done, not interacted before, and not dead
        if self.triggered and not self.interacted and self.text_done and not self.dead:
            self.interacted = True
            self.text_timer = pygame.time.get_ticks()
            self.current_text = ""
            self.text_index = 0
            self.text_done = False
            self.beg_sound.play()
            return "drop_gun"
        return None

    def take_damage(self, sound_muted=False):
        if self.dead:
            return
        self.hp -= 10
        if self.hp <= 0:
            self.dead = True
            self.fading = True
            if not sound_muted:
                self.death_sound.play()
        else:
            choices = [s for s in self.oof_sounds if s != self.last_oof]
            if not choices:
                choices = self.oof_sounds
            c = random.choice(choices)
            if not sound_muted:
                c.play()
            self.last_oof = c

    def update(self, sound_muted=False):
        if self.fading:
            self.fade_alpha -= 5
            if self.fade_alpha < 0:
                self.fade_alpha = 0

        if self.triggered and not self.text_done and not self.dead:
            now = pygame.time.get_ticks()
            line = self.second_line if self.interacted else self.first_line
            # Show next char after text_speed_ms
            if now - self.text_timer > self.text_speed_ms:
                self.text_timer = now
                if self.text_index < len(line):
                    self.current_text += line[self.text_index]
                    self.text_index += 1
                    if self.text_index == len(line):
                        self.text_done = True

    def draw(self, screen, font):
        if self.dead and self.fading:
            img = self.image.copy()
            img.set_alpha(self.fade_alpha)
            screen.blit(img, (self.x, self.y))
        elif not self.dead:
            screen.blit(self.image, (self.x, self.y))

        if self.triggered and not self.dead:
            text_surface = font.render(self.current_text, True, (255,255,255))
            screen.blit(text_surface,(self.x, self.y - 20))
