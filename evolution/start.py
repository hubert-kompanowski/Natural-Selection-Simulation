import pygame
from creature import Creature
from meal import Meal
import time
from random import randrange


class Ecolution:

    def __init__(self):
        pygame.init()
        self.map_size = 500
        self.creatures_number = 3
        self.meals_numbers = 3
        self.screen = pygame.display.set_mode((self.map_size, self.map_size))
        self.screen.fill((255, 255, 255))
        pygame.display.update()

        self.meals = [Meal(self.screen, self.map_size) for _ in range(self.meals_numbers)]
        self.creatures = [Creature(randrange(self.map_size), randrange(self.map_size), self.screen, str(i)) for i in
                          range(self.creatures_number)]

    def loop(self):
        flag = False
        is_energy = False
        for c in self.creatures:

            if c.energy > 0:
                is_energy = True
            # elif c.eaten_meals < 2:
            #     print("mniej niż zerooooo")

            if c.eaten_meals < 2:
                flag = True
                my_meal = c.search(self.meals)
                if my_meal is None:
                    return False
                if c.move(my_meal.x, my_meal.y):
                    my_meal.exist = False
                    c.eaten_meals += 1
            elif c.eaten_meals == 2:
                c.done()
            pygame.display.update()
        is_meal = False

        if not is_energy:
            return False

        for m in self.meals:
            if m.exist:
                is_meal = True
        if not is_meal:
            return False

        return flag
        # false -> przeywa

    def day(self):
        for c in self.creatures:
            c.eaten_meals = 0
            c.energy = 8000
            c.update((255, 255, 255))

        while self.loop():
            time.sleep(1.0 / 30)  #############################33333
            pass

        # for c in evol.creatures:
        #     print(c.index, "- vel=", c.velocity, "  meal=", c.eaten_meals, " en=", c.energy)
        # print()

        new_cre = []
        for c in self.creatures:
            if c.eaten_meals == 0:
                c.remove()
                c.exist = False
            elif c.eaten_meals == 1:
                continue
            elif c.eaten_meals == 2:
                cr = Creature(5, 5, self.screen, "@")
                cr.update((255, 255, 255))
                cr.velocity = c.velocity + (randrange(3) - 1) / 3
                new_cre.append(cr)

        while True:
            flag = True
            for c in self.creatures:
                if not c.exist:
                    self.creatures.remove(c)
                    flag = False
            if flag:
                break

        for c in new_cre:
            self.creatures.append(c)

        self.screen.fill((255, 255, 255))

        del self.meals

        self.meals = [Meal(self.screen, self.map_size) for _ in range(self.meals_numbers)]
        for c in self.creatures:
            c.update((255, 255, 255), c.x, c.y)
            c.x = randrange(self.map_size)
            c.y = randrange(self.map_size)
        #     print(c.index, "- vel=", int(c.velocity), "  meal=", c.eaten_meals)
        # print()


if __name__ == '__main__':
    evol = Ecolution()
    for _ in range(10):
        evol.day()
        # print(_)
    #
    # for c in evol.creatures:
    #     print("vel=", c.velocity, "  meal=", c.eaten_meals, " en=", c.energy)
    # print()
