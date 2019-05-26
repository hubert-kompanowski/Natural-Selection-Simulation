from random import randrange
import pygame
from colors import *


class Meal:
    def __init__(self, _screen, map, id_):
        self.exist = True
        (self.x, self.y) = (randrange(map[0], map[1]), randrange(map[0], map[1]))
        self.screen = _screen
        self.draw()
        self.id = id_

    def draw(self):
        if self.exist:
            pygame.draw.circle(self.screen, GREEN, (self.x, self.y), 5)
