
import Model
from random import randint


class AI:

    dirs = []
    dodge_finished = False
    dodges_finished = []
    hero_to_act_number = 0
    hero_to_move_number = 0
    p = 0

    def preprocess(self, world):
        print("preprocess")
        for a in range(4):
            self.dirs.append(world.get_path_move_directions(start_cell=world.map.my_respawn_zone[a], end_cell=world.map.objective_zone[a]))
            self.dodges_finished.append(False)

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

    def action(self, world):
        print("action")
        if not self.dodge_finished:
            while self.dodges_finished[self.hero_to_act_number]:
                self.hero_to_act_number += 1
                self.hero_to_act_number %= 4
            hero_to_act = world.my_heroes[self.hero_to_act_number]
            destination = world.map.objective_zone[self.hero_to_act_number]
            world.cast_ability(hero=hero_to_act, ability=hero_to_act.dodge_abilities[0], cell=destination)
            if destination == hero_to_act.current_cell:
                self.dodges_finished[self.hero_to_act_number] = True
            self.dodge_finished = all(self.dodges_finished)
            self.hero_to_act_number += 1
            self.hero_to_act_number %= 4
