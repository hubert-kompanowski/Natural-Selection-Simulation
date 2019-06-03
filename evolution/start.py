import pygame
from creature import Creature
from meal import Meal
import time
import math
from random import randrange
from colors import *
import matplotlib.pyplot as plt


class Evolution:

    def __init__(self):
        pygame.init()
        self.map_size = 800
        self.meal_map_size = (100, 700)
        self.cr_pos = self.map_size / 2
        self.creatures_number = 50
        self.meals_numbers = 50
        self.screen = pygame.display.set_mode((self.map_size, self.map_size))
        self.screen.fill(WHITE)
        pygame.display.update()

        self.meals = []
        self.creatures = []
        self.init_creature_pos()

        self.hist_vel = []
        self.hist_ran = []

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

    def day(self, delay, draw, only_vel=True):
        self.hist_vel = [0]
        self.hist_ran = [0]
        self.meals = [Meal(self.screen, self.meal_map_size, i) for i in range(1, self.meals_numbers + 1)]
        for c in self.creatures:
            self.hist_vel.append(math.floor(c.velocity * 10) / 10)
            self.hist_ran.append(math.floor(c.range * 10) / 10)
            # print(math.floor(c.velocity*10)/10, end=" ")
            c.search(self.meals)
            if draw:
                pygame.draw.circle(self.screen, self.color(c.velocity), c.pos, 10)
        if draw:
            pygame.display.update()
        time.sleep(delay * 3)
        # print()
        while self.loop(delay, draw, only_vel):
            if draw:
                self.screen.fill(WHITE)
            pass

        to_drop = []
        for c in self.creatures:
            if not c.is_alive and c.eaten_meals == 0:
                to_drop.append(c)

        for d in to_drop:
            self.creatures.remove(d)

        to_add = []
        for c in self.creatures:
            if c.eaten_meals == 2:
                pos_0 = 0
                pos_1 = 0
                if c.pos[0] == 10 or c.pos[0] == self.map_size - 10:
                    pos_0 = c.pos[0]
                    pos_1 = c.pos[1] + (randrange(5) - 2) * 30 + 3
                else:
                    pos_0 = c.pos[0] + (randrange(5) - 2) * 30 + 3
                    pos_1 = c.pos[1]

                if pos_0 < 0 or pos_0 > self.map_size:
                    pos_0 = c.pos[0]
                if pos_1 < 0 or pos_1 > self.map_size:
                    pos_1 = c.pos[1]

                x = randrange(10)
                if x == 0:
                    pos_0 = 10
                    pos_1 = math.floor(self.map_size / 2)
                if x == 1:
                    pos_0 = self.map_size - 10
                    pos_1 = math.floor(self.map_size / 2)
                if x == 2:
                    pos_1 = 10
                    pos_0 = math.floor(self.map_size / 2)
                if x == 3:
                    pos_1 = self.map_size - 10
                    pos_0 = math.floor(self.map_size / 2)

                vel = c.velocity
                random_num = randrange(20) - 10
                if random_num > 5:
                    vel = vel + 0.22 * vel
                if random_num < -5:
                    vel = vel - 0.22 * vel
                if not only_vel:
                    ran = c.range
                    random_num = randrange(20) - 10
                    if random_num > 5:
                        ran = ran + 0.1 * ran
                    if random_num < -5:
                        ran = ran - 0.1 * ran

                else:
                    ran = 600

                to_add.append(Creature(pos_0, pos_1, 55, vel, ran))

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

        for a in to_add:
            self.creatures.append(a)

        del self.meals
        self.screen.fill(WHITE)
        time.sleep(delay * 3)

    def loop(self, delay, draw, only_vel):
        for m in self.meals:
            if draw:
                m.draw()

        for c in self.creatures:

            eaten_meal_id = c.move(only_vel)

            if c.is_alive:
                if draw:
                    pygame.draw.circle(self.screen, self.color(c.velocity), c.pos, 10)
            elif c.eaten_meals == 1:
                if draw:
                    pygame.draw.circle(self.screen, self.color(c.velocity), c.pos, 10)
            else:
                if draw:
                    pygame.draw.circle(self.screen, BLACK, c.pos, 10)
            if eaten_meal_id > 0:
                for m in self.meals:
                    if m.id == eaten_meal_id:
                        self.meals.remove(m)
                        break
                for cr in self.creatures:
                    cr.search(self.meals)
                return True

        returning = False
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
        if draw:
            pygame.display.update()
        time.sleep(delay)

        return True

    def color(self, vel):
        red = math.floor((vel - 5) * 255 / 10)
        if red > 254:
            red = 254
        if red < 0:
            red = 0
        return red, 0, 255 - red


if __name__ == '__main__':
    evolution = Evolution()
    only_vel = True

    if not only_vel:
        delay = 1 / 60
        for i in range(10):
            evolution.day(delay, draw=True, only_vel=only_vel)
            print("Average of velocity = " + str(math.fsum(evolution.hist_vel) / len(evolution.hist_vel)))
            print("Average of range = " + str(math.fsum(evolution.hist_ran) / len(evolution.hist_ran)))
            fig2 = plt.figure()
            plt.hist2d(evolution.hist_vel, evolution.hist_ran, bins=10, range=[[0, 20], [0, 1000]])
            plt.xlabel('velocity')
            plt.ylabel('range')
            cbar = plt.colorbar()
            cbar.ax.set_ylabel('Counts')
            plt.show()
        delay = 0
        for i in range(100):
            evolution.day(delay, draw=True, only_vel=only_vel)
            print("Average of velocity = " + str(math.fsum(evolution.hist_vel) / len(evolution.hist_vel)))
            print("Average of range = " + str(math.fsum(evolution.hist_ran) / len(evolution.hist_ran)))
            if i % 25 == 0:
                fig2 = plt.figure()
                plt.hist2d(evolution.hist_vel, evolution.hist_ran, bins=10, range=[[0, 20], [0, 1000]])
                plt.xlabel('velocity')
                plt.ylabel('range')
                cbar = plt.colorbar()
                cbar.ax.set_ylabel('Counts')
                plt.show()

        delay = 0
        for i in range(700):
            evolution.day(delay, draw=False, only_vel=only_vel)
            print("Average of velocity = " + str(math.fsum(evolution.hist_vel) / len(evolution.hist_vel)))
            print("Average of range = " + str(math.fsum(evolution.hist_ran) / len(evolution.hist_ran)))
            if i % 25 == 0:
                fig2 = plt.figure()
                plt.hist2d(evolution.hist_vel, evolution.hist_ran, bins=10, range=[[0, 20], [0, 1000]])
                plt.xlabel('velocity')
                plt.ylabel('range')
                cbar = plt.colorbar()
                cbar.ax.set_ylabel('Counts')
                plt.show()
        delay = 1 / 60
        for i in range(10):
            evolution.day(delay, draw=True, only_vel=only_vel)
            print("Average of velocity = " + str(math.fsum(evolution.hist_vel) / len(evolution.hist_vel)))
            print("Average of range = " + str(math.fsum(evolution.hist_ran) / len(evolution.hist_ran)))
            if i % 25 == 0:
                fig2 = plt.figure()
                plt.hist2d(evolution.hist_vel, evolution.hist_ran, bins=10, range=[[0, 20], [0, 1000]])
                plt.xlabel('velocity')
                plt.ylabel('range')
                cbar = plt.colorbar()
                cbar.ax.set_ylabel('Counts')
                plt.show()

        pass
    else:

        delay = 1 / 60
        for i in range(10):
            evolution.day(delay, draw=True, only_vel=only_vel)
            print("Average of velocity = " + str(math.fsum(evolution.hist_vel) / len(evolution.hist_vel)))
            n, bins, patches = plt.hist(evolution.hist_vel, range=(0, 20), bins=15)
            x = 0
            for p in patches:
                col = x / 20
                p.set_facecolor((col, 0.0, 1.0 - col, 1.0))
                x += 1
            plt.show()

        delay = 0
        for i in range(100):
            evolution.day(delay, draw=True, only_vel=only_vel)
            if i % 10 == 0:
                print("Average of velocity = " + str(math.fsum(evolution.hist_vel) / len(evolution.hist_vel)))
                n, bins, patches = plt.hist(evolution.hist_vel, range=(0, 20), bins=15)
                x = 0
                for p in patches:
                    col = x / 20
                    p.set_facecolor((col, 0.0, 1.0 - col, 1.0))
                    x += 1
                plt.show()

        delay = 0
        for i in range(700):
            evolution.day(delay, draw=False, only_vel=only_vel)
            if i % 10 == 0:
                print("Average of velocity = " + str(math.fsum(evolution.hist_vel) / len(evolution.hist_vel)))
                n, bins, patches = plt.hist(evolution.hist_vel, range=(0, 20), bins=15)
                x = 0
                for p in patches:
                    col = x / 20
                    p.set_facecolor((col, 0.0, 1.0 - col, 1.0))
                    x += 1
                plt.show()

        delay = 1 / 60
        for i in range(10):
            evolution.day(delay, draw=True, only_vel=only_vel)
            print("Average of velocity = " + str(math.fsum(evolution.hist_vel) / len(evolution.hist_vel)))
            n, bins, patches = plt.hist(evolution.hist_vel, range=(0, 20), bins=15)
            x = 0
            for p in patches:
                col = x / 20
                p.set_facecolor((col, 0.0, 1.0 - col, 1.0))
                x += 1
            plt.show()
