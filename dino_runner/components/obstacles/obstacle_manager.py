
import random
import pygame
from dino_runner.components.obstacles.bird import Bird
from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.utils.constants import BIRD, LARGE_CACTUS, SMALL_CACTUS 


class ObstaclesManager:
    def __init__(self):
        self.obstacles = []
        self.cactus_list = [0,1,2]
        
    def update(self,game):
        if len(self.obstacles) == 0:
            opcion = random.choice(self.cactus_list)
            if opcion == 0:
                self.obstacles.append(Cactus(SMALL_CACTUS))
            elif opcion == 1:
                self.obstacles.append(Cactus(LARGE_CACTUS))
            elif opcion == 2:
                self.obstacles.append(Bird(BIRD))

    
        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacle.rect):
                if not game.player.shield:
                    pygame.time.delay(1000)
                    game.playing = False
                    game.death_count +=1
                    break
                else:
                    self.obstacles.remove(obstacle)
            
    def draw(self,screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)
            
    def reset_obstacles(self):
        self.obstacles = []