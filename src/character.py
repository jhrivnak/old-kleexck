import pygame


class Character:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 3
        self.running = False
        self.direction = "right"
        self.image_index = 0
        self.animation_timer = 0
        self.walk_images = [
            pygame.image.load(f"assets/images/character/cutout_walk-{i}.png")
            for i in range(1, 7)
        ]
        self.run_images = [
            pygame.image.load(f"assets/images/character/cutout_run-{i}.png")
            for i in range(1, 7)
        ]

    def move(self, keys, dt):
        vx, vy = 0, 0
        self.running = keys[pygame.K_LSHIFT]
        if keys[pygame.K_w]:
            vy = -self.speed
        if keys[pygame.K_s]:
            vy = self.speed
        if keys[pygame.K_a]:
            vx = -self.speed
            self.direction = "left"
        if keys[pygame.K_d]:
            vx = self.speed
            self.direction = "right"

        if self.running:
            vx *= 1.5
            vy *= 1.5

        self.x += vx * dt
        self.y += vy * dt
        self.x = max(0, min(self.x, 800 - 32))  # Ensure player stays on screen
        self.y = max(0, min(self.y, 600 - 32))

    def update_animation(self, dt):
        if self.animation_timer > 0.1:  # Change frame every 0.1 seconds
            self.animation_timer = 0
            self.image_index = (self.image_index + 1) % 6
        else:
            self.animation_timer += dt

    def draw(self, screen):
        if self.direction == "right":
            current_image = (
                self.run_images[self.image_index]
                if self.running
                else self.walk_images[self.image_index]
            )
        else:
            current_image = pygame.transform.flip(
                self.run_images[self.image_index]
                if self.running
                else self.walk_images[self.image_index],
                True,
                False,
            )
        screen.blit(current_image, (self.x, self.y))
