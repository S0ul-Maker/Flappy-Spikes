import pygame
import settings
import random
import os

from player import Player
from spike import Spike


class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()

        self.player = Player([self.visible_sprites],
                             self.obstacle_sprites, self.spawnSpikes)

        self.y_border_offset = 20
        self.startSpikes()

        self.score_font = pygame.font.Font(
            os.path.join('fonts', 'Roboto-Light.ttf'), 100)
        self.reset_font = pygame.font.Font(
            os.path.join('fonts', 'Roboto-Medium.ttf'), 50)

        self.spikes = []
        self.min_spikes = 2
        self.max_spikes = 3

        self.dead_prev = False

        self.diffculty = 4

    def reset(self):
        reset = self.player.reset()

        if not reset:
            return

        self.dead_prev = False

        for spike in self.spikes:
            spike.kill()
        self.spikes = []
        self.min_spikes = 2
        self.max_spikes = 3

    def startSpikes(self) -> None:
        """creates the starting border spikes"""
        for i in range(8):
            Spike([self.visible_sprites, self.obstacle_sprites],
                  (40+(i*60), self.y_border_offset))
            Spike([self.visible_sprites, self.obstacle_sprites],
                  (40+(i*60), settings.HEIGHT - self.y_border_offset))

    # TODO 可能要改这里 这里是生成Spike的地方
    def spawnSpikes(self, left: bool) -> None:
        """spawns spikes on specified side"""
        for spike in self.spikes:
            spike.kill()
        self.spikes = []

        for _ in range(random.randint(int(self.min_spikes), int(self.max_spikes))):
            attempts = 0
            while True:
                if left:
                    add_spike = Spike([self.visible_sprites, self.obstacle_sprites], (-20, random.uniform(
                        self.y_border_offset+40, settings.HEIGHT - self.y_border_offset-40)), left=True)
                else:
                    add_spike = Spike([self.visible_sprites, self.obstacle_sprites], (settings.WIDTH+20, random.uniform(
                        self.y_border_offset+40, settings.HEIGHT - self.y_border_offset-40)), left=False)

                free = True
                for spike in self.visible_sprites:
                    if spike == add_spike:
                        continue
                    if add_spike.rect.colliderect(spike.rect):
                        add_spike.kill()
                        free = False
                        break
                if free or attempts >= 10:
                    break
                else:
                    attempts += 1
            self.spikes.append(add_spike)

        if self.player.score % 2 == 0:
            self.max_spikes += 0.2
        if self.player.score & 5 == 0:
            self.min_spikes += 0.1

    def update(self) -> None:
        "called once per frame"
        self.drawScore()
        for trail_point in self.player.trail:
            pygame.draw.circle(self.display_surface, (0, 155, 246),
                               trail_point.pos, trail_point.duration*50)
            trail_point.update()
        self.visible_sprites.draw(self.display_surface)
        self.drawBorders()

        self.player.update()
        for spike in self.spikes:
            spike.update()

        if self.player.dead:
            self.reset()

            self.drawResetPrompt()

    def drawResetPrompt(self):
        hue_surf = pygame.Surface((settings.WIDTH, settings.HEIGHT))
        hue_surf.set_alpha(75)
        hue_surf.fill((200, 200, 200))
        self.display_surface.blit(hue_surf, (0, 0))

        reset_text = self.reset_font.render(
            "press SPACE to reset", True, (0, 155, 246))
        reset_text_rect = reset_text.get_rect(
            center=(settings.WIDTH//2, settings.HEIGHT//2))
        self.display_surface.blit(reset_text, reset_text_rect)

    def drawScore(self):
        pygame.draw.circle(self.display_surface, (240, 240, 240),
                           (settings.WIDTH//2, settings.HEIGHT//2), 75)

        score = self.score_font.render(
            str(self.player.score), True, (75, 75, 75))
        score_rect = score.get_rect(
            center=(settings.WIDTH//2, settings.HEIGHT//2))
        self.display_surface.blit(score, score_rect)

    def drawBorders(self):
        pygame.draw.rect(self.display_surface, (39, 39, 39), pygame.Rect(
            0, 0, settings.WIDTH, self.y_border_offset))
        pygame.draw.rect(self.display_surface, (39, 39, 39), pygame.Rect(
            0, settings.HEIGHT-self.y_border_offset, settings.WIDTH, self.y_border_offset))
