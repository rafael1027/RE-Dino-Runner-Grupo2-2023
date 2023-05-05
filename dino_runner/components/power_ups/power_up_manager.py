import random
import pygame
from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.components.power_ups.hammer import Hammer
from dino_runner.components.power_ups.shield import Shield
from dino_runner.utils.constants import LARGE_CACTUS, SMALL_CACTUS


class PowerUpManager:
    def __init__(self):
        self.power_ups = []
        self.power_list = [0,1]
        self.when_appers = 0
        self.points = 0
    
    def update(self, points, game_speed, player):
        self.generate_power_ups(points)
        for power_up in self.power_ups:
            power_up.update(game_speed, self.power_ups)
            if player.dino_rect.colliderect(power_up.rect):
                power_up.start_time = pygame.time.get_ticks()
                #add this part to Dino
                
                player.Hammer = True
                player.shield = True
                player.show_text = True
                player.type = power_up.type

                time_random = random.randrange (5, 8)
                player.shield_time_up = power_up.start_time + (time_random * 1000)
                self.power_ups.remove(power_up)

    def draw(self, screen):
        for power_up in self.power_ups:
            power_up.draw(screen)
    
    def reset_power_ups(self, points):
        self.power_ups = []
        self.points = points
        self.when_appers = self.points + random.randint(50, 100)

    def generate_power_ups(self, points):
        Opcion = random.choice(self.power_list)
        self.points = points
        if len(self.power_ups) == 0:
            if self.when_appers == self.points:
                print ("generating powerups")
                print(Opcion)
                if Opcion == 0:
                    self.power_ups.append(Shield())
                    self.when_appers = random.randint(self.when_appers+200, self.when_appers+400)
                elif Opcion == 1:
                    self.power_ups.append(Hammer())
                    self.when_appers = random.randint(self.when_appers+200, self.when_appers+400)
        return self.power_ups
    
    print ("Generating powerups")