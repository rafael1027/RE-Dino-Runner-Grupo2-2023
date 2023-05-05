import os
import pygame
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.Cloud import Cloud
from dino_runner.components.obstacles.obstacle_manager import ObstaclesManager
from dino_runner.components import text_utils
from dino_runner.components.power_ups.power_up_manager import PowerUpManager
from dino_runner.utils.constants import BG, ICON, RUNNING, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS


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
        self.player = Dinosaur()
        self.obstacle_manager = ObstaclesManager()
        self.power_up_manager = PowerUpManager()
        self.cloud = Cloud()
        self.points = 0
        self.running = True
        self.death_count = 0

    def run(self):
        # Game loop: events - update - draw
        self.obstacle_manager.reset_obstacles()
        self.power_up_manager.reset_power_ups(self.points)
        self.game_speed = 20
        self.points = 0
        self.playing = True
        while self.playing:
            self.events()
            self.update()
            self.draw()
                
    
    def execute(self):
        Music_Game = pygame.mixer.music.load(os.path.join('.dist\Music/fernanflo.mp3'))
        Music_Game= pygame.mixer.music.set_volume(0.5)
        Music_Game = pygame.mixer.music.play(-1)
        while self.running:
            if not self.playing:
                self.show_menu()
                

    def show_menu(self):
        self.running = True
        #Print a white background
        white_color = (255, 255, 255)
        self.screen.fill(white_color)

        #Print menu elements
        self.print_menu_elements()
        pygame.display.update()
        # create a menu event handler
        self.handle_key_events_on_menu()
    
    def print_menu_elements(self):
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2

        if self.death_count == 0:
            text, text_rect = text_utils.get_centered_message('Press any key to Start')
            self.screen.blit(text, text_rect)
        
        #Tarea menu para despues de la muerte
        elif self.death_count > 0:
            text, text_rect = text_utils.get_centered_message('Press any Key to Restart')
            score, score_rect = text_utils.get_centered_message('Your Score: ' + str(self.points),
                                                                height=half_screen_height + 50)
            death, death_rect = text_utils.get_centered_message('Death count: ' + str(self.death_count),
                                                                height=half_screen_height + 100)
            self.screen.blit(score, score_rect)
            self.screen.blit(text, text_rect)
            self.screen.blit(death, death_rect)

        self.screen.blit(RUNNING[0], (half_screen_width - 20, half_screen_height - 140))

    def handle_key_events_on_menu(self):
         for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.playing = False
                    pygame.display.quit()
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    self.run()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                #Si sale del juego el estado re¿¿de running debe ser fals
                self.running = False
        self.screen.fill((255, 255, 255))    

    def update(self):
        user_input = pygame.key.get_pressed()
        self.cloud.update(self.game_speed)
        self.player.update(user_input)
        self.obstacle_manager.update(self)
        self.power_up_manager.update(self.points, self.game_speed, self.player)

    def draw(self):
        self.score()
        self.clock.tick(FPS)
        # Removemos el fill porque lo hacemos en eventos self.screen.fill((255, 255, 255))
        self.draw_background()
        self.cloud.draw(self.screen)
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

    def score(self):
        self.points += 1
        if self.points % 100 == 0:
            self.game_speed += 1
        text, text_rect = text_utils.get_score_element(str(self.points))
        self.player.check_invincibility(self.screen)
        self.screen.blit(text, text_rect)
