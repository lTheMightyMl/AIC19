
import Model
from random import randint


class AI:

    destination_reached = False
    destinations_reached = []
    hero_to_act_number = 0
    hero_to_move_number = 0

    def preprocess(self, world):
        print("preprocess")
        for a in range(4):
            self.destinations_reached.append(False)

    def pick(self, world):
        print("pick")
        world.pick_hero(Model.HeroName.HEALER)

    def next_cell(self, cur_cell, dir):
        if dir == Model.Direction.UP:
            cur_cell.row += 1
        elif dir == Model.Direction.DOWN:
            cur_cell.row -= 1
        elif dir == Model.Direction.LEFT:
            cur_cell.column -= 1
        else:
            cur_cell.column += 1

    def move(self, world):
        print("move")
        for a in range(4):
            if world.map.objective_zone[a] == world.my_heroes[a].current_cell:
                self.destinations_reached[a] = True
        self.destination_reached = all(self.destinations_reached)
        if not self.destination_reached:
            while self.destinations_reached[self.hero_to_move_number]:
                self.hero_to_move_number += 1
                self.hero_to_move_number %= 4
            hero_to_move = world.my_heroes[self.hero_to_move_number]
            destination = world.map.objective_zone[self.hero_to_move_number]
            world.move_hero(hero=hero_to_move, direction=world.get_path_move_directions(start_cell=hero_to_move.current_cell, end_cell=destination)[0])
            self.hero_to_move_number += 1
            self.hero_to_move_number %= 4

    def action(self, world):
        print("action")
        for a in range(4):
            if world.map.objective_zone[a] == world.my_heroes[a].current_cell:
                self.destinations_reached[a] = True
        self.destination_reached = all(self.destinations_reached)
        if not self.destination_reached:
            while self.destinations_reached[self.hero_to_act_number]:
                self.hero_to_act_number += 1
                self.hero_to_act_number %= 4
            hero_to_act = world.my_heroes[self.hero_to_act_number]
            world.cast_ability(hero=hero_to_act, ability=hero_to_act.dodge_abilities[0], cell=world.map.objective_zone[self.hero_to_act_number])
            self.hero_to_act_number += 1
            self.hero_to_act_number %= 4
