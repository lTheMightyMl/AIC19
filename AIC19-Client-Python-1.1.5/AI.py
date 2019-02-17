
import Model


class AI:

    destination_reached = False
    destinations_reached = []
    hero_to_act_number = 0

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
            for a in range(4):
                if not self.destinations_reached[a]:
                    destination = world.map.objective_zone[a]
                    hero_to_move = world.my_heroes[a]
                    start = hero_to_move.current_cell
                    world.move_hero(hero=hero_to_move, direction=world.get_path_move_directions(start_cell=start, end_cell=destination)[0])

    def action(self, world):
        print("action")
        for a in range(4):
            if world.map.objective_zone[a] == world.my_heroes[a].current_cell:
                self.destinations_reached[a] = True
        self.destination_reached = all(self.destinations_reached)
        if not self.destination_reached:
            for a in range(4):
                if not self.destinations_reached[a]:
                    hero_to_act = world.my_heroes[a]
                    world.cast_ability(hero=hero_to_act, ability=hero_to_act.dodge_abilities[0], cell=world.map.objective_zone[a])
