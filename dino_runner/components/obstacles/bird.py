
import random
from dino_runner.components.obstacles.obstacle import Obstacle
from dino_runner.utils.constants import BIRD

class Bird(Obstacle):
    def __init__ (self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = random.randint (200, 300)
        self.index = 0
        
        
    def draw(self, SCREEN):
        if self.index >= 9:
            self.index =0
        SCREEN.blit(self.image[self.index//5], self.rect)
        self.index += 1
            
        