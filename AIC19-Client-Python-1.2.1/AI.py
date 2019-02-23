import Model


class AI:

    destination = []
    destination_reached = False
    destinations_reached = []
    hero_to_act_number = 0

    def preprocess(self, world):
        print("preprocess")
        for a in range(4):
            self.destinations_reached.append(False)
        temp = []
        for col in range(world.map.column_num):
            temp.append(False)
        mark = []
        for row in range(world.map.row_num):
            mark.append(temp)
        for a in range(4):
            for objective_cell in world.map.objective_zone:
                if not mark[objective_cell.row][objective_cell.column]:
                    self.destination.append(objective_cell)
                    break
            source = world.map.my_respawn_zone[a]
            for objective_cell in world.map.objective_zone:
                if not mark[objective_cell.row][objective_cell.column]:
                    if(len(world.get_path_move_directions(start_cell=source, end_cell=objective_cell)) < len(world.get_path_move_directions(start_cell=source, end_cell=self.destination[a]))):
                        self.destination[a] = objective_cell
            mark[self.destination[a].row][self.destination[a].column] = True

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
            if self.destination[a] == world.my_heroes[a].current_cell:
                self.destinations_reached[a] = True
            else:
                self.destinations_reached[a] = False
        self.destination_reached = all(self.destinations_reached)
        if not self.destination_reached:
            for a in range(4):
                if not self.destinations_reached[a]:
                    destination = self.destination[a]
                    hero_to_move = world.my_heroes[a]
                    start = hero_to_move.current_cell
                    world.move_hero(hero=hero_to_move, direction=world.get_path_move_directions(start_cell=start, end_cell=destination)[0])

    def action(self, world):
        print("action")
        for a in range(4):
            if self.destination[a] == world.my_heroes[a].current_cell:
                self.destinations_reached[a] = True
            else:
                self.destinations_reached[a] = False
        self.destination_reached = all(self.destinations_reached)
        if not self.destination_reached:
            for a in range(4):
                if not self.destinations_reached[a]:
                    hero_to_act = world.my_heroes[a]
                    world.cast_ability(hero=hero_to_act, ability=hero_to_act.dodge_abilities[0], cell=self.destination[a])
        else:
            pass
