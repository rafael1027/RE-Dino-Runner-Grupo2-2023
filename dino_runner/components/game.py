
import pygame
from dino_runner.components.dinosaur import Dinosaur

from dino_runner.components import text_utils
from dino_runner.components.obstacles.obstacles_manager import ObstaclesManager

from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.player = Dinosaur()
        self.obstacles_manager = ObstaclesManager()
        self.points = 0
        self.running = True
        self.death_count = 0

    def run(self):
        # Game loop: events - update - draw
        self.obstacles_manager.reset_obstacles()
        self.playing = True
        while self.playing:
            self.events()
            self.update()
            self.draw()
        pygame.quit()
        
    def execute(self):
        while self.running:
            if not self.playing:
                self.show_menu()
            
    def show_menu(self):
        self.running = True
        # print a white background
        white_color = (255, 255, 255)
        self.screen.fill(white_color)
        
        #print menu elements
        self.print_menu_elements()
        pygame.display.update()
        # create a menu event handler
        
    def print_menu_elements(self):
        half_screen_height = SCREEN_HEIGHT //2
        half_screen_width = SCREEN_WIDTH //2
        
        if self.death_count == 0:
            text , text_rect =text_utils.get_centered_message('press any key to start ')
            self.screen.blit(text, text_rect)
            
    def handle_key_events_on_menu(self):
         for event in pygame.event.get():
            if event.type == pygame.QUIT:
                 self.running = False
                 self.playing = False
                 pygame.display.quit()
                 pygame.quit()
                 exit()
            if event.type == pygame.KEYDOWN :
                self.run()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacles_manager.update(self)

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacles_manager.draw(self.screen)
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
        print(self.x_pos_bg)
