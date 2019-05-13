import pygame
import math


class Creature:
    def __init__(self, _x, _y, _screen, _index):
        self.index = _index
        self.velocity = 10
        self.energy = 0
        (self.x, self.y) = (_x, _y)
        self.screen = _screen
        self.eaten_meals = 0
        self.exist = True

        self.update(self.x, self.y, (0, 0, 255))

    def remove(self):
        self.energy = 0
        pygame.draw.circle(self.screen, (255, 255, 255), (self.x, self.y), 10)

    def done(self):
        self.update((255, 0, 255), self.x, self.y)
        self.energy = 0

    def update(self, color, _x=None, _y=None):
        if self.energy > 0:
            if not (_x is None and _y is None):
                (self.x, self.y) = (_x, _y)
            pygame.draw.circle(self.screen, color, (self.x, self.y), 10)

    def move(self, x_, y_):

        self.update((255, 255, 255))

        x_dest = x_ - self.x
        y_dest = y_ - self.y

        sum_move = abs(x_dest) + abs(y_dest)

        if sum_move < 15:
            self.update((0, 0, 255), x_, y_)
            return True
        elif self.energy > 0:
            x_move = math.ceil(x_dest * self.velocity / sum_move)
            y_move = math.floor(y_dest * self.velocity / sum_move)
            self.update((0, 0, 255), self.x + x_move, self.y + y_move)
            self.energy -= self.velocity ** 2
            return False

    def search(self, meals):
        if len(meals) == 0:
            return None
        (index, min_dist) = (0, math.inf)
        i = 0
        flag = True
        for m in meals:
            actual = math.sqrt((m.x - self.x) ** 2 + (m.y - self.y) ** 2)
            if actual < min_dist and m.exist:
                min_dist = actual
                index = i
                flag = False
            i += 1

        if flag:
            return None
        return meals[index]
