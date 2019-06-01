import pygame
from creature import Creature
from meal import Meal
import time
import math
from random import randrange
from colors import *


class Evolution:

    def __init__(self):
        pygame.init()
        self.map_size = 800
        self.meal_map_size = (200, 600)
        self.cr_pos = self.map_size / 2
        self.creatures_number = 20
        self.meals_numbers = 15
        self.screen = pygame.display.set_mode((self.map_size, self.map_size))
        self.screen.fill(WHITE)
        pygame.display.update()

        self.meals = []
        self.creatures = []
        self.init_creature_pos()

    def init_creature_pos(self):
        for i in range(self.creatures_number):
            if i % 4 == 0:
                y_pos = self.map_size / 2 - self.cr_pos / 2
                self.creatures.append(
                    Creature(10, math.floor(y_pos + i // 4 * self.cr_pos / (self.creatures_number / 4)), i))
            if i % 4 == 1:
                y_pos = self.map_size / 2 - self.cr_pos / 2
                self.creatures.append(
                    Creature(self.map_size - 10,
                             math.floor(y_pos + i // 4 * self.cr_pos / (self.creatures_number / 4)), i))
            if i % 4 == 2:
                x_pos = self.map_size / 2 - self.cr_pos / 2
                self.creatures.append(
                    Creature(math.floor(x_pos + i // 4 * self.cr_pos / (self.creatures_number / 4)), 10, i))
            if i % 4 == 3:
                x_pos = self.map_size / 2 - self.cr_pos / 2
                self.creatures.append(
                    Creature(math.floor(x_pos + i // 4 * self.cr_pos / (self.creatures_number / 4)),
                             self.map_size - 10, i))

    def day(self):
        self.meals = [Meal(self.screen, self.meal_map_size, i) for i in range(1, self.meals_numbers + 1)]
        for c in self.creatures:
            c.search(self.meals)
            pygame.draw.circle(self.screen, BLUE, c.pos, 10)

        pygame.display.update()
        time.sleep(0.5)

        while self.loop():
            self.screen.fill(WHITE)

        to_drop = []
        for c in self.creatures:
            if not c.is_alive and c.eaten_meals == 0:
                to_drop.append(c)

            c.actual_energy = c.max_energy
            c.is_eaten = False
            c.returned = False
            c.returning = False
            c.is_alive = True
            c.eaten_meals = 0
            c.actual_step = 0
            c.actual_step_to_home = 0
            c.move_plan = []
            c.move_home_plan = []

        for d in to_drop:
            self.creatures.remove(d)

        del self.meals
        self.screen.fill(WHITE)
        time.sleep(1)

    def loop(self):
        for m in self.meals:
            m.draw()

        for c in self.creatures:

            eaten_meal_id = c.move()

            if c.is_alive:
                pygame.draw.circle(self.screen, BLUE, c.pos, 10)
            elif c.eaten_meals == 1:
                pygame.draw.circle(self.screen, BLUE, c.pos, 10)
            else:
                pygame.draw.circle(self.screen, BLACK, c.pos, 10)
            if eaten_meal_id > 0:
                for m in self.meals:
                    if m.id == eaten_meal_id:
                        self.meals.remove(m)
                        break
                for cr in self.creatures:
                    cr.search(self.meals)
                return True
        print()
        returning = False
        all_returned = True
        all_dead_or_returned = True
        for c in self.creatures:
            if c.returning:
                returning = True
            if not c.returned and c.is_alive:
                all_dead_or_returned = False




        if len(self.meals) == 0 and not returning:
            return False

        if all_dead_or_returned and not returning:
            return False
        pygame.display.update()
        time.sleep(1 / 30)

        return True


if __name__ == '__main__':
    evolution = Evolution()
    for _ in range(10):
        evolution.day()
