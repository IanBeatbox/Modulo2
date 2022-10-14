import os
import random

import pygame

from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.components.obstacles.pterodactyl import Pterodactyl
from dino_runner.utils.constants import BIRD, SHIELD_TYPE


class ObstacleManager():
    def __init__(self):
        self.obstacles = []
        self.sound()

    def update(self, game):
        if len(self.obstacles) == 0:
            if random.randint(0, 2) == 0:
                cactus_type = 'SMALL' if random.randint(0, 1) == 0 else 'LARGE'
                cactus = Cactus(cactus_type)
                self.obstacles.append(cactus)
            else:
                pterodactyl = Pterodactyl(BIRD)
                self.obstacles.append(pterodactyl)

        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacle.rect):
                if game.player.type != SHIELD_TYPE:
                    pygame.time.delay(1000)
                    self.sound.play()
                    game.death_count += 1
                    game.playing = False
                    break
                else:
                    self.obstacles.remove(obstacle)

    def sound(self):
        path = os.path.join('dino_runner/assets/Other/die.wav')
        self.sound = pygame.mixer.Sound(path)

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)

    def reset_obstacles(self):
        self.obstacles = []
