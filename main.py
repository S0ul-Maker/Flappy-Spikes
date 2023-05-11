import pygame
import sys
import settings

from level import Level


class Game():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (settings.WIDTH, settings.HEIGHT))
        pygame.display.set_caption("flappy spikes")
        self.clock = pygame.time.Clock()

        self.level = Level()

    def run(self) -> None:
        while True:
            self.update()
            self.clock.tick(settings.FPS)

    def update(self) -> None:
        """called once per frame"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                self.level.diffculty = min(
                    self.level.diffculty+1, settings.MAX_DIIFICULTY)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                self.level.diffculty = max(
                    self.level.diffculty-1, settings.MIN_DIIFICULTY)

        self.screen.fill('grey')
        print(self.level.diffculty)

        self.level.update()

        pygame.display.update()

        if not self.level.dead_prev and self.level.player.dead:
            self.level.dead_prev = True
            pygame.time.wait(250)


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
