import pygame
import settings


class Player(pygame.sprite.Sprite):
    X_SPEED = 5

    def __init__(self, groups: list, obstacle_sprites: pygame.sprite.Group, spawnSpikes):
        super().__init__(groups)
        self.image = pygame.image.load('assets/blue_bird.png').convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 0.12)
        self.rect = self.image.get_rect(
            center=(settings.WIDTH//2, settings.HEIGHT//2))
        self.hitbox = self.rect.inflate(-20, 0)

        self.obstacle_sprites = obstacle_sprites

        self.spawnSpikes = spawnSpikes

        # MOVEMENT
        self.x_vel = self.X_SPEED
        self.GRAVITY = 0.3  # 0.7
        self.y_vel = 0
        self.JUMP_VEL = -7  # -10

        self.trail = []
        self.trail_time = 0.35
        self.trail_timer = 0
        self.trail_delay = 0.05
        self.trail_step_timer = self.trail_delay

        self.started = False

        self.jumped = False

        self.score = 0
        self.dead = False

    def reset(self) -> bool:
        """resets the player when space pressed"""
        if self.x_vel < 0:
            self.image = pygame.transform.flip(self.image, True, False)
        self.x_vel = self.y_vel = 0

        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and self.jumped:
            return False
        if not keys[pygame.K_SPACE] and self.jumped:
            self.jumped = False
            return False
        if not keys[pygame.K_SPACE]:
            return False

        self.x_vel = self.X_SPEED
        self.y_vel = 0
        self.started = False
        self.jumped = True
        self.score = 0
        self.dead = False

        self.hitbox.center = (settings.WIDTH//2, settings.HEIGHT//2)
        self.rect.center = self.hitbox.center

        return True

    def update(self) -> None:
        "called once per frame"
        self.input()

        self.timers()

        if self.started:
            self.applyGravity()
            self.move()

        for i, trail_point in sorted(enumerate(self.trail), reverse=True):
            if trail_point.duration <= 0:
                self.trail.pop(i)

    def input(self) -> None:
        """player input logic"""
        if self.dead:
            return

        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and not self.jumped and not self.started:
            self.started = True
            return

        if keys[pygame.K_SPACE] and not self.jumped:
            self.y_vel = self.JUMP_VEL
            self.jumped = True
            self.trail_timer = self.trail_time
            self.trail_step_timer = self.trail_delay
        if not keys[pygame.K_SPACE]:
            self.jumped = False

    def move(self) -> None:
        """moves the player"""
        self.wallBounce()

        self.hitbox.x += self.x_vel
        self.hitbox.y += self.y_vel
        self.collisions()

        self.rect.center = self.hitbox.center

    def wallBounce(self) -> None:
        """bounce off wall"""
        if (self.rect.right >= settings.WIDTH and self.x_vel > 0) or (self.rect.left <= 0 and self.x_vel < 0):
            self.score += 1
            self.x_vel = -self.x_vel
            self.image = pygame.transform.flip(self.image, True, False)

            if self.score > 0:
                self.spawnSpikes(False if self.score % 2 == 0 else True)
                self.x_vel += 0.05 if self.x_vel > 0 else -0.05

    def applyGravity(self) -> None:
        self.y_vel += self.GRAVITY

    def collisions(self) -> None:
        """checks collisions with obstacles"""
        for sprite in self.obstacle_sprites:
            for point in sprite.points:
                if self.hitbox.collidepoint(point[0], point[1]):
                    self.dead = True

    def timers(self) -> None:
        """counts down all timers being used and does logic based off them"""
        if self.trail_timer > 0:
            self.trail_timer -= 1/settings.FPS
        if self.trail_step_timer > 0:
            self.trail_step_timer -= 1/settings.FPS

        if self.trail_step_timer <= 0 and self.trail_timer > 0:
            self.trail.append(TrailPoint(self.rect.center))

            if self.trail_timer > 0:
                self.trail_step_timer = self.trail_delay


class TrailPoint:
    def __init__(self, pos):
        self.pos = pos

        self.duration = 0.25

    def update(self):
        self.duration -= 1/settings.FPS
