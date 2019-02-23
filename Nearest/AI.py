import Model


class AI:

    destination = []
    destination_reached = []
    my_hero_number = 0

    def preprocess(self, world):
        print("preprocess")
        for a in range(4):
            self.destination_reached.append(False)
        mark = []
        for row in range(world.map.row_num):
            temp = []
            for col in range(world.map.column_num):
                temp.append(False)
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
        world.pick_hero(Model.HeroName.BLASTER)

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
                self.destination_reached[a] = True
            else:
                self.destination_reached[a] = False
        for a in range(4):
            hero_to_move = world.my_heroes[a]
            if hero_to_move.current_hp <= 0:
                continue
            if not self.destination_reached[a]:
                destination = self.destination[a]
                start = hero_to_move.current_cell
                world.move_hero(hero=hero_to_move, direction=world.get_path_move_directions(start_cell=start, end_cell=destination)[0])

    def ok(self, world, cell):
        for hero in world.my_heroes:
            if cell == hero.current_cell:
                return False
        return True

    def action(self, world):
        print("action")
        for a in range(4):
            if self.destination[a] == world.my_heroes[a].current_cell:
                self.destination_reached[a] = True
            else:
                self.destination_reached[a] = False
        for a in range(4):
            my_hero = world.my_heroes[a]
            if my_hero.current_hp <= 0:
                continue
            destination = self.destination[a]
            dodge = my_hero.dodge_abilities[0]
            if not self.destination_reached[a] and dodge.is_ready and self.ok(world, world.get_impact_cell(ability=dodge, start_cell=my_hero.current_cell, target_cell=destination)):
                world.cast_ability(hero=my_hero, ability=dodge, cell=destination)
            else:
                if world.opp_heroes[0].current_cell.column == -1 and world.opp_heroes[0].current_cell.row == -1:
                    pass
                else:
                    nearest_opp = world.opp_heroes[0]
                    my_hero_cell = my_hero.current_cell
                    for opp_hero in world.opp_heroes:
                        if opp_hero.current_hp <= 0:
                            continue
                        if world.manhattan_distance(start_cell=my_hero_cell, end_cell=opp_hero.current_cell) < world.manhattan_distance(start_cell=my_hero_cell, end_cell=nearest_opp.current_cell):
                            nearest_opp = opp_hero
                    if nearest_opp.current_hp > 0:
                        offensive_abilities = my_hero.offensive_abilities
                        for b in range(len(offensive_abilities) - 1, -1, -1):
                            attack = offensive_abilities[b]
                            if attack.range < world.manhattan_distance(start_cell=my_hero_cell, end_cell=nearest_opp.current_cell) or not attack.is_ready:
                                continue
                            world.cast_ability(hero=my_hero, ability=attack, cell=nearest_opp.current_cell)

