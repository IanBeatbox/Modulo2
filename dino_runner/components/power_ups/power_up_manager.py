import os
import random

import pygame

from dino_runner.components.power_ups.shield import Shield


class PowerUpManager():
    def __init__(self):
        self.power_ups = []
        self.when_apprears = 0
        self.duration = random.randint(3, 6)
        self.sound()

    def generate_power_up(self, score):
        if len(self.power_ups) == 0 and self.when_apprears == score:
            self.when_apprears += random.randint(200, 300)
            self.power_ups.append(Shield())

    def update(self, game):
        self.generate_power_up(game.score)
        for power_up in self.power_ups:
            power_up.update(game.game_speed, self.power_ups)
            if game.player.dino_rect.colliderect(power_up.rect):
                self.sound.play()
                power_up.start_time = pygame.time.get_ticks()
                game.player.has_power_up = True
                game.player.type = power_up.type
                game.player.power_time_up = power_up.start_time + \
                    (self.duration * 1000)

                self.power_ups.remove(power_up)

    def sound(self):
        path = os.path.join('dino_runner/assets/Other/t_rex.mp3')
        self.sound = pygame.mixer.Sound(path)

    def draw(self, screen):
        for power_up in self.power_ups:
            power_up.draw(screen)

    def reset_power_ups(self):
        self.power_ups = []
        self.when_apprears = random.randint(200, 300)
