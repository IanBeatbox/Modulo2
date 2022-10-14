

import pygame

from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.components.power_ups.power_up_manager import PowerUpManager
from dino_runner.utils.constants import (BG, DEFAULT_TYPE, DINO_DEAD,
                                         FONT_STYLE, FPS, GAME_OVER, ICON,
                                         SCREEN_HEIGHT, SCREEN_WIDTH, TITLE,
                                         Cloud)


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.x_pos_cloud = 0
        self.y_pos_cloud = 100
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.power_up_manager = PowerUpManager()
        self.running = False
        self.score = 0
        self.death_count = 0
        self.menssage = ""
        self.position_x = 0
        self.position_y = 0

    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()
        pygame.display.quit()
        pygame.quit()

    def reset_game(self):
        self.obstacle_manager.reset_obstacles()
        self.playing = True
        self.game_speed = 20
        self.power_up_manager.reset_power_ups()

    def run(self):
        # Game loop: events - update - draw
        self.reset_game()
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False

    def update(self):
        self.update_score()
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self)
        self.power_up_manager.update(self)

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.draw_cloud()
        self.draw_score()
        self.draw_power_up_time()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.power_up_manager.draw(self.screen)
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))

        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def draw_cloud(self):
        image_width = Cloud.get_width()
        self.screen.blit(Cloud, (self.x_pos_cloud, self.y_pos_cloud))
        self.screen.blit(
            Cloud, (image_width + self.x_pos_cloud, self.y_pos_cloud))

        if self.x_pos_cloud <= -image_width:
            self.screen.blit(
                Cloud, (image_width + self.x_pos_cloud, self.y_pos_cloud))
            self.x_pos_cloud = 0
        self.x_pos_cloud -= self.game_speed

    def show_message(self, menssage, position_x, position_y):
        font = pygame.font.Font(FONT_STYLE, 30)
        text = font.render(menssage, True, (0, 0, 0))
        text_rec = text.get_rect()
        text_rec.center = (position_x, position_y)
        self.screen.blit(text, text_rec)

    def draw_score(self):
        self.menssage = f'Score: {self.score}'
        self.position_x = 1000
        self.position_y = 50
        self.show_message(self.menssage, self.position_x, self.position_y)

    def draw_power_up_time(self):
        if self.player.has_power_up:
            time_to_show = round(
                (self.player.power_time_up - pygame.time.get_ticks()) / 1000, 2)
            if time_to_show >= 0:
                self.menssage = f'{self.player.type.capitalize()} enabled for {time_to_show} seconds'
                font = pygame.font.Font(FONT_STYLE, 30)
                text = font.render(self.menssage, True, (0, 0, 0))
                text_rec = text.get_rect()
                text_rec.center = (500, 50)
                self.screen.blit(text, text_rec)
            else:
                self.has_power_up = False
                self.player.type = DEFAULT_TYPE

    def update_score(self):
        self.score += 1

        if self.score % 100 == 0 and self.game_speed < 700:
            self.game_speed += 5

    

    def handle_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.playing = False
            elif event.type == pygame.KEYDOWN:
                self.score = 0
                self.run()

    def show_menu(self):
        self.screen.fill((44, 168, 135))
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2

        if self.death_count == 0:
            self.screen.blit(ICON, (half_screen_width -
                             20, half_screen_height - 140))

            menssage = "Press any key to start"
            self.show_message(
                menssage, half_screen_width, half_screen_height)
        else:
            self.screen.fill((230, 15, 51))
            self.screen.blit(DINO_DEAD, (half_screen_width -
                             20, half_screen_height - 140))
            menssage = f'Deaths: {self.death_count}'
            self.show_message(
                menssage, half_screen_width - 460, half_screen_height - 250)

            self.screen.blit(GAME_OVER, (half_screen_width -
                             180, half_screen_height - 250))

            menssage = f'Score: {self.score}'
            self.show_message(
                menssage, half_screen_width, half_screen_height+80)
            message = 'Try again'
            self.show_message(message,
                              half_screen_width, half_screen_height)
            menssage = "Press any key to Continue"
            self.show_message(
                menssage, half_screen_width, half_screen_height + 250)
        pygame.display.update()
        self.handle_events_on_menu()
