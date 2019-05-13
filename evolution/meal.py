from random import randrange
import pygame


class Meal:
    def __init__(self, _screen, i):
        self.exist = True
        (self.x, self.y) = (randrange(i), randrange(i))
        self.screen = _screen
        pygame.draw.circle(self.screen, (255, 0, 0), (self.x, self.y), 5)

    def __del__(self):
        pygame.draw.circle(self.screen, (255, 255, 255), (self.x, self.y), 10)



