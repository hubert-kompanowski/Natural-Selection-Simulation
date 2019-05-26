import pygame
import math
from colors import *
from pygame.math import Vector2
import time


class Creature:
    def __init__(self, x_, y_):
        self.pos = (x_, y_)
        self.start_pos = (x_, y_)
        self.velocity = 5.0
        self.actual_step = 0
        self.move_plan = []

        self.range = 600
        self.max_energy = 100.0
        self.actual_energy = self.max_energy
        self.eaten_meals = 0

        self.is_alive = True
        self.is_eaten = False
        self.returning = False
        self.returned = False
        self.found_meal = False
        self.meal_id = -1

    def move(self):
        if self.returned:
            return -1

        if self.actual_energy <= 0:
            self.is_alive = False
            return -1



        # if len(self.move_plan) == 1:
        #     self.pos = self.move_plan[0]

        if self.actual_step + 1 == len(self.move_plan):
            self.eaten_meals += 1
            if self.eaten_meals == 2:
                self.is_eaten = True
            if self.returning:
                self.returned = True
                self.returning = False
            return self.meal_id

        if self.returning:
            self.actual_step += 1
            self.pos = self.move_plan[self.actual_step]
            return -1

        if self.actual_step + 1 < len(self.move_plan):
            self.actual_step += 1
            self.pos = self.move_plan[self.actual_step]

        if not self.is_eaten:
            self.actual_energy -= 1

        return -1

    def move_rand(self):
        pass

    def search(self, meals):

        if (self.is_eaten and self.is_alive) or (not self.is_alive and self.eaten_meals == 1) or (
                len(meals) == 0 and self.eaten_meals > 0):
            step_to_achieve = 15
            dest_x = self.start_pos[0]
            dest_y = self.start_pos[1]
            self.meal_id = -1
            self.is_eaten = True
            self.returning = True

        elif self.eaten_meals < 2 and self.is_alive:
            self.move_plan.clear()
            self.actual_step = 0
            if len(meals) == 0:
                return None
            (index, min_dist) = (0, math.inf)
            i = 0
            flag = True
            for m in meals:
                actual = math.sqrt((m.x - self.pos[0]) ** 2 + (m.y - self.pos[1]) ** 2)
                if actual < min_dist and m.exist and actual ** 2 <= self.range ** 2:
                    min_dist = actual
                    index = i
                    flag = False
                i += 1

            if flag:
                self.meal_id = -1
                return None

            step_to_achieve = math.floor(min_dist / self.velocity)

            dest_x = meals[index].x
            dest_y = meals[index].y

            self.meal_id = meals[index].id
        else:
            return None

        for i in range(1, step_to_achieve + 1):
            x_next_step = self.pos[0] + math.floor((dest_x - self.pos[0]) / step_to_achieve * i)
            y_next_step = self.pos[1] + math.floor((dest_y - self.pos[1]) / step_to_achieve * i)
            self.move_plan.append((x_next_step, y_next_step))

        self.move_plan.append((dest_x, dest_y))
