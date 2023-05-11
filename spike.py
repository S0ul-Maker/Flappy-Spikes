import pygame
import settings
import math


class Spike(pygame.sprite.Sprite):
    def __init__(self, groups: list, center_pos: tuple, left: bool = None):
        super().__init__(groups)
        self.image = pygame.image.load('assets/spike.png').convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 45, 0.75)
        self.rect = self.image.get_rect(center=center_pos)

        self.left = left
        self.appear_speed = 1.5

        self.points = [self.rect.midtop, self.rect.midleft,
                       self.rect.midbottom, self.rect.midright]
        self.points.extend([self.midpoint(self.rect.midtop, self.rect.midright),
                            self.midpoint(self.rect.midtop, self.rect.midleft),
                            self.midpoint(self.rect.midbottom,
                                          self.rect.midright),
                            self.midpoint(self.rect.midbottom, self.rect.midleft)])

    def midpoint(self, point1, point2) -> tuple:
        """gets the midpoint of 2 points"""
        x = (point1[0]+point2[0])/2
        y = (point1[1]+point2[1])/2
        return (x, y)

    def update(self) -> None:
        moved = False
        if self.left and self.rect.centerx < 0:
            self.rect.centerx += self.appear_speed
            moved = True
        elif self.left and self.rect.centerx > 0:
            self.rect.centerx = 0
            moved = True

        if not self.left and self.rect.centerx > settings.WIDTH:
            self.rect.centerx -= self.appear_speed
            moved = True
        elif not self.left and self.rect.centerx < settings.WIDTH:
            self.rect.centerx = settings.WIDTH
            moved = True

        if moved:
            self.points = [self.rect.midtop, self.rect.midleft,
                           self.rect.midbottom, self.rect.midright]
            self.points.extend([self.midpoint(self.rect.midtop, self.rect.midright),
                                self.midpoint(self.rect.midtop,
                                              self.rect.midleft),
                                self.midpoint(self.rect.midbottom,
                                              self.rect.midright),
                                self.midpoint(self.rect.midbottom, self.rect.midleft)])
