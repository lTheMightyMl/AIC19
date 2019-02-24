import Model


class AI:

    far = []
    destination = []
    near = []

    def preprocess(self, world):
        print("preprocess")
        print("preprocess")
        mark_far = []
        mark_near = []
        for row in range(world.map.row_num):
            temp_far = []
            temp_near = []
            for col in range(world.map.column_num):
                temp_far.append(False)
                temp_near.append(False)
            mark_far.append(temp_far)
            mark_near.append(temp_near)
        for a in range(4):
            for objective_cell in world.map.objective_zone:
                if len(self.far) == a and not mark_far[objective_cell.row][objective_cell.column]:
                    self.far.append(objective_cell)
                if len(self.near) == a and not mark_near[objective_cell.row][objective_cell.column]:
                    self.near.append(objective_cell)
                if len(self.near) > a and len(self.far) > a:
                    break
            source = world.map.my_respawn_zone[a]
            for objective_cell in world.map.objective_zone:
                new_len = len(world.get_path_move_directions(
                    start_cell=source, end_cell=objective_cell))
                far_len = len(world.get_path_move_directions(
                    start_cell=source, end_cell=self.far[a]))
                near_len = len(world.get_path_move_directions(
                    start_cell=source, end_cell=self.near[a]))
                if new_len > far_len:
                    if not mark_far[objective_cell.row][objective_cell.column]:
                        self.far[a] = objective_cell
                elif new_len < near_len:
                    if not mark_near[objective_cell.row][objective_cell.column]:
                        self.near[a] = objective_cell
            mark_far[self.far[a].row][self.far[a].column] = True
            mark_near[self.near[a].row][self.near[a].column] = True
            if a % 2 == 0:
                self.destination.append(self.far[a])
            else:
                self.destination.append(self.near[a])

    def pick(self, world):
        print("pick")
        world.pick_hero(Model.HeroName.BLASTER)

    def move(self, world):
        print("move")
        for a in range(4):
            hero_to_move = world.my_heroes[a]
            if hero_to_move.current_hp <= 0:
                continue
            if not self.destination[a] == hero_to_move.current_cell:
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
            my_hero = world.my_heroes[a]
            if my_hero.current_hp <= 0:
                continue
            destination = self.destination[a]
            dodge = my_hero.dodge_abilities[0]
            if not self.destination[a] == my_hero.current_cell and dodge.is_ready and self.ok(world, world.get_impact_cell(ability=dodge, start_cell=my_hero.current_cell, target_cell=destination)) and world.ap >= dodge.ap_cost:
                world.cast_ability(hero=my_hero, ability=dodge, cell=destination)
                world.ap -= dodge.ap_cost
            else:
                if world.opp_heroes[0].current_cell.column == -1 and world.opp_heroes[0].current_cell.row == -1:
                    pass
                else:
                    nearest_opp = world.opp_heroes[0]
                    my_hero_cell = my_hero.current_cell
                    for opp_hero in world.opp_heroes:
                        if opp_hero.current_hp <= 0:
                            continue
                        cur_dist = world.manhattan_distance(start_cell=my_hero_cell, end_cell=nearest_opp.current_cell)
                        new_dist = world.manhattan_distance(start_cell=my_hero_cell, end_cell=opp_hero.current_cell)
                        if new_dist < cur_dist:
                            nearest_opp = opp_hero
                        elif new_dist == cur_dist and opp_hero.current_hp < nearest_opp.current_hp:
                            nearest_opp = opp_hero
                    if nearest_opp.current_hp > 0:
                        offensive_abilities = my_hero.offensive_abilities
                        for b in range(len(offensive_abilities) - 1, -1, -1):
                            attack = offensive_abilities[b]
                            nearest_opp_cell = nearest_opp.current_cell
                            if attack.area_of_effect < world.manhattan_distance(start_cell=world.get_impact_cell(start_cell=my_hero_cell, target_cell=nearest_opp_cell, ability=attack), end_cell=nearest_opp_cell) or not attack.is_ready or world.ap < attack.ap_cost:
                                continue
                            world.cast_ability(hero=my_hero, ability=attack, cell=nearest_opp_cell)
                            world.ap -= attack.ap_cost
