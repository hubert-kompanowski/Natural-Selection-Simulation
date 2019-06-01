import math


class Creature:
    def __init__(self, x_, y_, index_, velocity_=3.0, range_=600):
        self.index = index_
        self.pos = (x_, y_)
        self.start_pos = (x_, y_)
        self.velocity = velocity_
        self.actual_step = 0
        self.move_plan = []
        self.actual_step_to_home = 0
        self.move_home_plan = []

        self.range = range_
        self.max_energy = 90.0*300/self.range
        self.actual_energy = self.max_energy
        self.eaten_meals = 0

        self.is_alive = True
        self.is_eaten = False
        self.returning = False
        self.returned = False
        self.found_meal = False
        self.meal_id = -1

    def move(self):
        #
        # print(str(self.index), end=" is ")
        # if not self.is_alive:
        #     print("dead ", end=", ")
        # else:
        #     print("alive", end=", ")
        # if self.returned:
        #     print("    returned", end=", ")
        # else:
        #     print("not returned", end=", ")
        # if self.returning:
        #     print("    returning", end=", ")
        # else:
        #     print("not returning", end=", ")
        # print("eat " + str(self.eaten_meals) + " meals")

        if self.returned:
            self.returning = False
            return -1

        if self.returning:
            self.move_home()
            return -1

        if self.actual_energy <= 0 and self.eaten_meals == 0:
            self.is_alive = False
            return -1

        if (self.actual_energy <= 0 and self.eaten_meals == 1) and not self.returning:
            self.returning = True
            self.is_alive = False
            self.find_path_to_home()

        if self.actual_step + 1 == len(self.move_plan):
            self.eaten_meals += 1
            if self.eaten_meals == 2:
                self.is_eaten = True
            return self.meal_id

        if self.actual_step + 1 < len(self.move_plan):
            self.actual_step += 1
            self.pos = self.move_plan[self.actual_step]

        if not self.is_eaten:
            self.actual_energy -= 1 * self.velocity * self.velocity / 25
            if self.actual_energy < 0:
                self.actual_energy = 0.0

        return -1

    def move_home(self):
        if self.pos[0] == self.start_pos[0] and self.pos[1] == self.start_pos[1]:
            self.returned = True
            self.returning = False

        else:
            self.actual_step_to_home += 1
            if self.actual_step_to_home < len(self.move_home_plan):
                self.pos = self.move_home_plan[self.actual_step_to_home]
            else:
                self.pos = self.start_pos


    def move_rand(self):
        pass

    def search(self, meals):
        # print("search")

        if len(meals) == 0 and self.eaten_meals == 0:
            self.is_alive = False
            self.actual_energy = 0.0
            self.returning = False
            return None

        if (self.is_eaten and self.is_alive) or (self.actual_energy <= 0 and self.eaten_meals == 1) or (
                len(meals) == 0 and self.eaten_meals > 0):
            self.find_path_to_home()

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

            for i in range(1, step_to_achieve + 1):
                x_next_step = self.pos[0] + math.floor((dest_x - self.pos[0]) / step_to_achieve * i)
                y_next_step = self.pos[1] + math.floor((dest_y - self.pos[1]) / step_to_achieve * i)
                self.move_plan.append((x_next_step, y_next_step))

            self.move_plan.append((dest_x, dest_y))

        # else:

    def find_path_to_home(self):
        self.actual_step_to_home = 0
        self.move_home_plan.clear()

        step_to_achieve = 20 - math.floor(self.velocity)
        dest_x = self.start_pos[0]
        dest_y = self.start_pos[1]
        self.meal_id = -1
        self.is_eaten = True
        self.returning = True

        for i in range(1, step_to_achieve + 1):
            x_next_step = self.pos[0] + math.floor((dest_x - self.pos[0]) / step_to_achieve * i)
            y_next_step = self.pos[1] + math.floor((dest_y - self.pos[1]) / step_to_achieve * i)
            self.move_home_plan.append((x_next_step, y_next_step))

        self.move_home_plan.append((dest_x, dest_y))
