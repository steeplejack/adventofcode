import re
from enum import Enum
from collections import deque

Moves = Enum("Moves", "GEODE OBSIDIAN CLAY ORE WAIT")

class Blueprint():

    def __init__(self, n, ore, clay, obsidian, geode):
        self.n = n
        self.ore = ore
        self.clay = clay
        self.obsidian = obsidian
        self.geode = geode

    def get_blueprint_id(self):
        return self.n

    def get_ore_robot_cost(self):
        return self.ore

    def get_clay_robot_cost(self):
        return self.clay

    def get_obsidian_robot_cost(self):
        return self.obsidian

    def get_geode_robot_cost(self):
        return self.geode

    def max_ore_cost(self):
        return max(self.ore, self.clay, self.obsidian[0], self.geode[0])

    def max_clay_cost(self):
        return self.obsidian[1]

    def max_obsidian_cost(self):
        return self.geode[1]


class Factory():
    def __init__(self, blueprint):
        self.blueprint = blueprint
        self.ore_robots = 1
        self.clay_robots = 0
        self.obsidian_robots = 0
        self.geode_robots = 0
        self.time_step = 0

        self.ore = 0
        self.clay = 0
        self.obsidian = 0
        self.geodes = 0

    def __str__(self):
        resources = f'[ore={self.ore},clay={self.clay},obs={self.obsidian},geo={self.geodes}]'
        robots = f'[ore={self.ore_robots},clay={self.clay_robots},obs={self.obsidian_robots},geo={self.geode_robots}]'
        return f'time={self.time_step} -- resources={resources} / robots={robots}'

    def copy(self):
        new = Factory(self.blueprint)
        new.ore_robots = self.ore_robots
        new.clay_robots = self.clay_robots
        new.obsidian_robots = self.obsidian_robots
        new.geode_robots = self.geode_robots
        new.time_step = self.time_step
        new.ore = self.ore
        new.clay = self.clay
        new.obsidian = self.obsidian
        new.geodes = self.geodes
        return new

    def tick(self):
        self.time_step += 1
        self.ore += self.ore_robots
        self.clay += self.clay_robots
        self.obsidian += self.obsidian_robots
        self.geodes += self.geode_robots

    def build_ore_robot(self):
        ore_cost = self.blueprint.get_ore_robot_cost()
        if self.ore >= ore_cost:
            self.tick()
            self.ore -= ore_cost
            self.ore_robots += 1
            return True
        return False

    def build_clay_robot(self):
        ore_cost = self.blueprint.get_clay_robot_cost()
        if self.ore >= ore_cost:
            self.tick()
            self.ore -= ore_cost
            self.clay_robots += 1
            return True
        return False

    def build_obsidian_robot(self):
        ore_cost, clay_cost = self.blueprint.get_obsidian_robot_cost()
        if self.ore >= ore_cost and self.clay >= clay_cost:
            self.tick()
            self.ore -= ore_cost
            self.clay -= clay_cost
            self.obsidian_robots += 1
            return True
        return False

    def build_geode_robot(self):
        ore_cost, obsidian_cost = self.blueprint.get_geode_robot_cost()
        if self.ore >= ore_cost and self.obsidian >= obsidian_cost:
            self.tick()
            self.ore -= ore_cost
            self.obsidian -= obsidian_cost
            self.geode_robots += 1
            return True
        return False

    def available_moves(self):
        moves = [Moves.WAIT]
        if self.ore >= self.blueprint.get_ore_robot_cost():
            moves.append(Moves.ORE)
        if self.ore >= self.blueprint.get_clay_robot_cost():
            moves.append(Moves.CLAY)
        
        ore_cost, clay_cost = self.blueprint.get_obsidian_robot_cost()
        if self.ore >= ore_cost and self.clay >= clay_cost:
            moves.append(Moves.OBSIDIAN)

        ore_cost, obsidian_cost = self.blueprint.get_geode_robot_cost()
        if self.ore >= ore_cost and self.obsidian >= obsidian_cost:
            moves.append(Moves.GEODE)
        moves = moves[::-1]
        return moves

    def filtered_moves(self):
        moves = self.available_moves()
        if Moves.ORE in moves and self.ore_robots >= self.blueprint.max_ore_cost():
            moves.remove(Moves.ORE)
        if Moves.OBSIDIAN in moves and self.obsidian_robots >= self.blueprint.max_obsidian_cost():
            moves.remove(Moves.OBSIDIAN)
        if Moves.CLAY in moves and self.clay_robots >= self.blueprint.max_clay_cost():
            moves.remove(Moves.CLAY)
        return moves

    def params(self):
        return (self.ore, self.clay, self.obsidian, self.geodes,
                self.ore_robots, self.clay_robots, self.obsidian_robots, self.geode_robots,
                self.time_step)

    def project_best_score(self, max_time):
        remaining_time = max_time - self.time_step
        score = self.geodes
        geode_robots = self.geode_robots
        for _ in range(remaining_time):
            score += geode_robots
            geode_robots += 1
        return score



def parse_line(line):
    line = line.strip()
    n = [int(x) for x in re.findall(r'\d+', line)]
    return Blueprint(n[0], n[1], n[2], (n[3], n[4]), (n[5], n[6]))

def apply_move(factory, move):
    if move == Moves.WAIT:
        factory.tick()
    elif move == Moves.ORE:
        assert factory.build_ore_robot()
    elif move == Moves.CLAY:
        assert factory.build_clay_robot()
    elif move == Moves.OBSIDIAN:
        assert factory.build_obsidian_robot()
    else:
        assert factory.build_geode_robot()




def max_score(blueprint, max_time):
    factory = Factory(blueprint)
    q = deque()
    q.append((factory, Moves.WAIT))
    max_score = 0
    seen = set()
    i = 0
    collisions = 0
    branch_and_bounds = 0
    moves_filtered = 0
    time_step = -1
    while len(q) > 0:
        f, move = q.popleft()
        i += 1
        if i % 50000 == 0:
            print(f'BEST={max_score} BBs={branch_and_bounds} MEMO={collisions} FILT={moves_filtered} Q={len(q)} TIME={f.time_step}')
        if f.time_step < max_time:
            apply_move(f, move)
            all_moves = f.available_moves()
            moves = f.filtered_moves()
            moves_filtered += len(all_moves) - len(moves)
            best_possible = f.project_best_score(max_time)
            if best_possible <= max_score:
                branch_and_bounds += 1
            # if Moves.GEODE in moves:
            #     new_moves = [Moves.WAIT, Moves.GEODE]
            #     if Moves.OBSIDIAN in moves:
            #         new_moves.append(Moves.OBSIDIAN)
            #     moves = new_moves
            # elif Moves.OBSIDIAN in moves:
            #     moves = [Moves.WAIT, Moves.OBSIDIAN]
            # elif Moves.CLAY in moves:
            #     moves = [Moves.WAIT, Moves.CLAY]
            for move in moves:
                params = f.params()
                been_seen = (params, move) in seen
                if been_seen:
                    collisions += 1
                if not been_seen and best_possible > max_score:
                    q.append((f.copy(), move))
                    seen.add((params, move))
            score = f.geodes
            if score > max_score:
                max_score = score
        if f.time_step > time_step and f.time_step > 9:
            print(f"Clearing cache at time step {time_step}")
            sz = len(seen)
            time_step = f.time_step
            to_remove = set()
            for (params, move) in seen:
                if params[-1] < time_step:
                    to_remove.add((params, move))
            rm = len(to_remove)
            seen -= to_remove
            assert len(seen) == sz - rm
            assert rm > 0
            print(f"Reduced memo from {sz} to {sz-rm}")
            
    return max_score


if __name__ == "__main__":
    filename = 'example.txt'
    with open(filename) as fl:
        blueprints = [parse_line(line) for line in fl]

    # Test
    if filename == 'example.txt':
        factory = Factory(blueprints[0])
        # Minute 1
        factory.tick()
        # Minute 2
        factory.tick()
        # Minute 3
        assert factory.build_clay_robot()
        # Minute 4
        factory.tick()
        # Minute 5
        assert factory.build_clay_robot()
        # Minute 6
        factory.tick()
        # Minute 7
        assert factory.build_clay_robot()
        # Minute 8
        factory.tick()
        # Minute 9
        factory.tick()
        # Minute 10
        factory.tick()
        # Minute 11
        assert factory.build_obsidian_robot()
        # Minute 12
        factory.build_clay_robot()
        # Minute 13
        factory.tick()
        # Minute 14
        factory.tick()
        # Minute 15
        assert factory.build_obsidian_robot()
        # Minute 16
        factory.tick()
        # Minute 17
        factory.tick()
        # Minute 18
        assert factory.build_geode_robot()
        # Minute 19
        factory.tick()
        # Minute 20
        factory.tick()
        # Minute 21
        assert factory.build_geode_robot()
        # Minute 22
        factory.tick()
        # Minute 23
        factory.tick()
        # Minute 24
        factory.tick()
        assert factory.geodes == 9

        factory = Factory(blueprints[0])
        print(Moves.WAIT, factory.filtered_moves())
        apply_move(factory, Moves.WAIT) # 1
        print(Moves.WAIT, factory.filtered_moves())
        apply_move(factory, Moves.WAIT)
        print(Moves.WAIT, factory.filtered_moves())
        apply_move(factory, Moves.WAIT)
        print(Moves.WAIT, factory.filtered_moves())
        apply_move(factory, Moves.WAIT)
        print(Moves.ORE, factory.filtered_moves())
        apply_move(factory, Moves.ORE)  # 5
        print(Moves.WAIT, factory.filtered_moves())
        apply_move(factory, Moves.WAIT)
        print(Moves.CLAY, factory.filtered_moves())
        apply_move(factory, Moves.CLAY)
        print(Moves.CLAY, factory.filtered_moves())
        apply_move(factory, Moves.CLAY)
        print(Moves.CLAY, factory.filtered_moves())
        apply_move(factory, Moves.CLAY)
        print(Moves.CLAY, factory.filtered_moves())
        apply_move(factory, Moves.CLAY) # 10
        print(Moves.CLAY, factory.filtered_moves())
        apply_move(factory, Moves.CLAY)
        print(Moves.CLAY, factory.filtered_moves())
        apply_move(factory, Moves.CLAY)
        print(Moves.CLAY, factory.filtered_moves())
        apply_move(factory, Moves.CLAY)
        print(Moves.OBSIDIAN, factory.filtered_moves())
        apply_move(factory, Moves.OBSIDIAN)
        print(Moves.WAIT, factory.filtered_moves())
        apply_move(factory, Moves.WAIT) # 15
        print(Moves.OBSIDIAN, factory.filtered_moves())
        apply_move(factory, Moves.OBSIDIAN)
        print(Moves.OBSIDIAN, factory.filtered_moves())
        apply_move(factory, Moves.OBSIDIAN)
        print(Moves.WAIT, factory.filtered_moves())
        apply_move(factory, Moves.WAIT)
        print(Moves.OBSIDIAN, factory.filtered_moves())
        apply_move(factory, Moves.OBSIDIAN)
        print(Moves.GEODE, factory.filtered_moves())
        apply_move(factory, Moves.GEODE) # 20
        print(Moves.OBSIDIAN, factory.filtered_moves())
        apply_move(factory, Moves.OBSIDIAN)
        print(Moves.GEODE, factory.filtered_moves())
        apply_move(factory, Moves.GEODE)
        print(Moves.GEODE, factory.filtered_moves())
        apply_move(factory, Moves.GEODE)
        print(Moves.GEODE, factory.filtered_moves())
        apply_move(factory, Moves.GEODE)
        print(Moves.WAIT, factory.filtered_moves())
        apply_move(factory, Moves.WAIT) #25
        print(Moves.GEODE, factory.filtered_moves())
        apply_move(factory, Moves.GEODE)
        print(Moves.GEODE, factory.filtered_moves())
        apply_move(factory, Moves.GEODE)
        print(Moves.WAIT, factory.filtered_moves())
        apply_move(factory, Moves.WAIT)
        print(Moves.GEODE, factory.filtered_moves())
        apply_move(factory, Moves.GEODE)
        print(Moves.GEODE, factory.filtered_moves())
        apply_move(factory, Moves.GEODE) # 30
        print(Moves.GEODE, factory.filtered_moves())
        apply_move(factory, Moves.GEODE)
        print(Moves.WAIT, factory.filtered_moves())
        apply_move(factory, Moves.WAIT)
        assert factory.geodes == 56
    
    part2 = True

    if part2:
        if len(blueprints) > 3:
            blueprints = blueprints[:3]
        scores = []
        for blueprint in blueprints:
            score = max_score(blueprint, 32)
            scores.append(score)
            print(score)
            print(scores)
        print(scores)

        result = 1
        for score in scores:
            result *= score
        print(f'Part 2: {result}') # 11592, 13248 are too small

    else:
        scores = []
        for blueprint in blueprints:
            score = max_score(blueprint, 24)
            scores.append(score)
            print(score)
            print(scores)
        print(scores)

        ids = [bp.get_blueprint_id() for bp in blueprints]
        result = sum(score*id for (score, id) in zip(scores, ids))
        print(f'Part 1: {result}')
