import Model


class AI:

    far = []
    destination = []
    has_attacked = []
    near = []
    wait = []
    waiting_time = []

    def longest_cooldown(self, hero):
        ret = 0
        for ability in hero.abilities:
            if ability.cooldown > ret:
                ret = ability.cooldown
        return ret

    def preprocess(self, world):
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
                new_len = len(world.get_path_move_directions(start_cell=source, end_cell=objective_cell))
                far_len = len(world.get_path_move_directions(start_cell=source, end_cell=self.far[a]))
                near_len = len(world.get_path_move_directions(start_cell=source, end_cell=self.near[a]))
                if new_len > far_len:
                    if not mark_far[objective_cell.row][objective_cell.column]:
                        self.far[a] = objective_cell
                elif new_len < near_len:
                    if not mark_near[objective_cell.row][objective_cell.column]:
                        self.near[a] = objective_cell
            mark_far[self.far[a].row][self.far[a].column] = True
            mark_near[self.near[a].row][self.near[a].column] = True
            self.destination.append(self.far[a])

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
                if self.destination[a] == self.far[a]:
                    self.destination[a] = self.near[a]
                else:
                    self.destination[a] = self.far[a]
        for a in range(4):
            hero_to_move = world.my_heroes[a]
            destination = self.destination[a]
            if hero_to_move.current_hp <= 0 or world.ap < hero_to_move.move_ap_cost or destination == hero_to_move.current_cell:
                continue
            start = hero_to_move.current_cell
            world.move_hero(hero=hero_to_move, direction=world.get_path_move_directions(start_cell=start, end_cell=destination)[0])

    def ok(self, world, cell):
        for hero in world.my_heroes:
            if cell == hero.current_cell:
                return False
        return True

    def can_hit(self, world, hero):
        first_opp_hero_cell = world.opp_heroes[0].current_cell
        if first_opp_hero_cell.column == -1 and first_opp_hero_cell.row == -1:
            return False
        for offensive_ability in hero.offensive_abilities:
            if not offensive_ability.is_ready or not world.ap >= offensive_ability.ap_cost:
                continue
            hero_cell = hero.current_cell
            for opp_hero in world.opp_heroes:
                if world.manhattan_distance(start_cell=world.get_impact_cell(ability=offensive_ability, start_cell=hero_cell, target_cell=opp_hero.current_cell), end_cell=hero_cell) <= (offensive_ability.range + offensive_ability.area_of_effect):
                    return True
        return False

    def action(self, world):
        print("action")
        for a in range(4):
            if self.destination[a] == world.my_heroes[a].current_cell:
                if self.destination[a] == self.far[a]:
                    self.destination[a] = self.near[a]
                else:
                    self.destination[a] = self.far[a]
        for a in range(4):
            my_hero = world.my_heroes[a]
            if my_hero.current_hp <= 0:
                continue
            destination = self.destination[a]
            dodge = my_hero.dodge_abilities[0]
            if my_hero.current_cell != destination and dodge.is_ready and self.ok(world, world.get_impact_cell(ability=dodge, start_cell=my_hero.current_cell, target_cell=destination)) and world.ap >= dodge.ap_cost:
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
                        if world.manhattan_distance(start_cell=my_hero_cell, end_cell=opp_hero.current_cell) < world.manhattan_distance(start_cell=my_hero_cell, end_cell=nearest_opp.current_cell):
                            nearest_opp = opp_hero
                    if nearest_opp.current_hp > 0:
                        offensive_abilities = my_hero.offensive_abilities
                        for b in range(len(offensive_abilities) - 1, -1, -1):
                            attack = offensive_abilities[b]
                            if attack.range < world.manhattan_distance(start_cell=my_hero_cell, end_cell=nearest_opp.current_cell) or not attack.is_ready or world.ap < attack.ap_cost:
                                continue
                            world.cast_ability(hero=my_hero, ability=attack, cell=nearest_opp.current_cell)
                            world.ap -= attack.ap_cost
