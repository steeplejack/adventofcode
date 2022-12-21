import re
from enum import Enum
from collections import deque
from collections import namedtuple

Params = namedtuple("Params", "time ore clay obsidian geode ore_robot clay_robot obsidian_robot geode_robot")
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

def new():
    return Params(0, 0, 0, 0, 0, 1, 0, 0, 0)

def wait(params):
    return Params(params.time + 1,
                  params.ore + params.ore_robot,
                  params.clay + params.clay_robot,
                  params.obsidian + params.obsidian_robot,
                  params.geode + params.geode_robot,
                  params.ore_robot,
                  params.clay_robot,
                  params.obsidian_robot,
                  params.geode_robot)

def build_ore_robot(blueprint, params):
    cost = blueprint.get_ore_robot_cost()
    return Params(params.time + 1,
                  params.ore + params.ore_robot - cost,
                  params.clay + params.clay_robot,
                  params.obsidian + params.obsidian_robot,
                  params.geode + params.geode_robot,
                  params.ore_robot + 1,
                  params.clay_robot,
                  params.obsidian_robot,
                  params.geode_robot)

def build_clay_robot(blueprint, params):
    cost = blueprint.get_clay_robot_cost()
    return Params(params.time + 1,
                  params.ore + params.ore_robot - cost,
                  params.clay + params.clay_robot,
                  params.obsidian + params.obsidian_robot,
                  params.geode + params.geode_robot,
                  params.ore_robot,
                  params.clay_robot + 1,
                  params.obsidian_robot,
                  params.geode_robot)

def build_obsidian_robot(blueprint, params):
    cost_ore, cost_clay = blueprint.get_obsidian_robot_cost()
    return Params(params.time + 1,
                  params.ore + params.ore_robot - cost_ore,
                  params.clay + params.clay_robot - cost_clay,
                  params.obsidian + params.obsidian_robot,
                  params.geode + params.geode_robot,
                  params.ore_robot,
                  params.clay_robot,
                  params.obsidian_robot + 1,
                  params.geode_robot)

def build_geode_robot(blueprint, params):
    cost_ore, cost_obsidian = blueprint.get_geode_robot_cost()
    return Params(params.time + 1,
                  params.ore + params.ore_robot - cost_ore,
                  params.clay + params.clay_robot,
                  params.obsidian + params.obsidian_robot - cost_obsidian,
                  params.geode + params.geode_robot,
                  params.ore_robot,
                  params.clay_robot,
                  params.obsidian_robot,
                  params.geode_robot + 1)

def available_moves(blueprint, params):
    moves = []
    if params.ore >= blueprint.get_geode_robot_cost()[0] and params.obsidian >= blueprint.get_geode_robot_cost()[1]:
        moves.append(Moves.GEODE)
    if params.ore >= blueprint.get_obsidian_robot_cost()[0] and params.clay >= blueprint.get_obsidian_robot_cost()[1] and params.obsidian_robot < blueprint.max_obsidian_cost():
        moves.append(Moves.OBSIDIAN)
    if params.ore >= blueprint.get_ore_robot_cost() and params.ore_robot < blueprint.max_ore_cost():
        moves.append(Moves.ORE)
    if params.ore >= blueprint.get_clay_robot_cost() and params.clay_robot < blueprint.max_clay_cost():
        moves.append(Moves.CLAY)
    moves.append(Moves.WAIT)
    return moves

def apply_move(blueprint, params, move):
    if move == Moves.WAIT:
        return wait(params)
    elif move == Moves.ORE:
        return build_ore_robot(blueprint, params)
    elif move == Moves.CLAY:
        return build_clay_robot(blueprint, params)
    elif move == Moves.OBSIDIAN:
        return build_obsidian_robot(blueprint, params)
    else:
        return build_geode_robot(blueprint, params)

def parse_line(line):
    line = line.strip()
    n = [int(x) for x in re.findall(r'\d+', line)]
    return Blueprint(n[0], n[1], n[2], (n[3], n[4]), (n[5], n[6]))

def trnum(x):
    return (x * (x + 1)) // 2

def project_score(params, max_time):
    s = max_time - params[0]
    return trnum(s + params.geode_robot - 1) - trnum(params.geode_robot - 1) + params.geode

import random

def greedy_search(blueprint, generations):
    factory = new()
    for _ in range(generations):
        moves = available_moves(blueprint, factory)
        if Moves.GEODE in moves:
            factory = build_geode_robot(blueprint, factory)
        elif Moves.OBSIDIAN in moves:
            factory = build_obsidian_robot(blueprint, factory)
        else:
            move = random.choice(moves)
            factory = apply_move(blueprint, factory, move)
    return factory

def greedy_lower_bound(blueprint, generations):
    s = 0
    for _ in range(100):
        f = greedy_search(blueprint, generations)
        if f.geode > s:
            s = f.geode
    return s



def max_score(blueprint, max_time, lower_bound = 0, heuristic = False):
    factory = new()
    apply_move(blueprint, factory, Moves.WAIT)
    q = deque()
    q.append(factory)
    max_score = 0
    seen = set()
    i = 0
    collisions = 0
    branch_and_bounds = 0
    time_step = -1
    while len(q) > 0:
        f = q.popleft()
        i += 1

        score = f[4]
        if score > max_score:
            max_score = score
        
        if i % 50000 == 0:
            print(f'LB={lower_bound} BEST={max_score} BBs={branch_and_bounds} MEMO={collisions} Q={len(q)} TIME={f.time}')
        
        if f.time < max_time:
            moves = available_moves(blueprint, f)
            if heuristic:
                if Moves.GEODE in moves:
                    moves = [Moves.GEODE]
                elif Moves.OBSIDIAN in moves:
                    moves = [Moves.OBSIDIAN]
            for move in moves:
                new_f = apply_move(blueprint, f, move)
                
                best_possible = project_score(new_f, max_time)
                if best_possible <= max_score or best_possible < lower_bound:
                    branch_and_bounds += 1
                
                been_seen = new_f in seen
                if been_seen:
                    collisions += 1
                
                if not been_seen and best_possible > max_score and best_possible >= lower_bound:
                    q.append(new_f)
                    seen.add(new_f)
        
        if f.time > time_step and f.time > 9:
            time_step = f.time
            sz = len(seen)
            to_remove = set()
            for params in seen:
                if params.time < time_step:
                    to_remove.add(params)
            rm = len(to_remove)
            seen -= to_remove
            assert len(seen) == sz - rm
            assert rm > 0
            
    return max_score


if __name__ == "__main__":
    import sys
    filename = sys.argv[1]
    # filename = 'example.txt'
    with open(filename) as fl:
        blueprints = [parse_line(line) for line in fl]

    # Test
    blueprint = blueprints[0]
    if filename == 'example.txt':
        factory = new()
        # Minute 1
        factory = wait(factory)
        # Minute 2
        factory = wait(factory)
        # Minute 3
        factory = build_clay_robot(blueprint, factory)
        # Minute 4
        factory = wait(factory)
        # Minute 5
        factory = build_clay_robot(blueprint, factory)
        # Minute 6
        factory = wait(factory)
        # Minute 7
        factory = build_clay_robot(blueprint, factory)
        # Minute 8
        factory = wait(factory)
        # Minute 9
        factory = wait(factory)
        # Minute 10
        factory = wait(factory)
        # Minute 11
        factory = build_obsidian_robot(blueprint, factory)
        # Minute 12
        factory = build_clay_robot(blueprint, factory)
        # Minute 13
        factory = wait(factory)
        # Minute 14
        factory = wait(factory)
        # Minute 15
        factory = build_obsidian_robot(blueprint, factory)
        # Minute 16
        factory = wait(factory)
        # Minute 17
        factory = wait(factory)
        # Minute 18
        factory = build_geode_robot(blueprint, factory)
        # Minute 19
        factory = wait(factory)
        # Minute 20
        factory = wait(factory)
        # Minute 21
        factory = build_geode_robot(blueprint, factory)
        # Minute 22
        factory = wait(factory)
        # Minute 23
        factory = wait(factory)
        # Minute 24
        factory = wait(factory)
        assert factory.geode == 9

        factory = new()
        factory = apply_move(blueprint, factory, Moves.WAIT) # 1
        factory = apply_move(blueprint, factory, Moves.WAIT)
        factory = apply_move(blueprint, factory, Moves.WAIT)
        factory = apply_move(blueprint, factory, Moves.WAIT)
        factory = apply_move(blueprint, factory, Moves.ORE)  # 5
        factory = apply_move(blueprint, factory, Moves.WAIT)
        factory = apply_move(blueprint, factory, Moves.CLAY)
        factory = apply_move(blueprint, factory, Moves.CLAY)
        factory = apply_move(blueprint, factory, Moves.CLAY)
        factory = apply_move(blueprint, factory, Moves.CLAY) # 10
        factory = apply_move(blueprint, factory, Moves.CLAY)
        factory = apply_move(blueprint, factory, Moves.CLAY)
        factory = apply_move(blueprint, factory, Moves.CLAY)
        factory = apply_move(blueprint, factory, Moves.OBSIDIAN)
        factory = apply_move(blueprint, factory, Moves.WAIT) # 15
        factory = apply_move(blueprint, factory, Moves.OBSIDIAN)
        factory = apply_move(blueprint, factory, Moves.OBSIDIAN)
        factory = apply_move(blueprint, factory, Moves.WAIT)
        factory = apply_move(blueprint, factory, Moves.OBSIDIAN)
        factory = apply_move(blueprint, factory, Moves.GEODE) # 20
        factory = apply_move(blueprint, factory, Moves.OBSIDIAN)
        factory = apply_move(blueprint, factory, Moves.GEODE)
        factory = apply_move(blueprint, factory, Moves.GEODE)
        factory = apply_move(blueprint, factory, Moves.GEODE)
        factory = apply_move(blueprint, factory, Moves.WAIT) #25
        factory = apply_move(blueprint, factory, Moves.GEODE)
        factory = apply_move(blueprint, factory, Moves.GEODE)
        factory = apply_move(blueprint, factory, Moves.WAIT)
        factory = apply_move(blueprint, factory, Moves.GEODE)
        factory = apply_move(blueprint, factory, Moves.GEODE) # 30
        factory = apply_move(blueprint, factory, Moves.GEODE)
        factory = apply_move(blueprint, factory, Moves.WAIT)
        assert factory.geode == 56
    
    part2 = True

    if part2: # 49 18
        # I was stuck on this and checked the solutions thread on reddit for ideas. One thing I added from there
        # is to never build more robots producing a resource than I can spend of that resource in one turn - 
        # don't have 5 obsidian robots if the maximum obsidian cost is 4. This helps, but was still not enough
        # to make the problem solvable.
        # The best idea I had (the only thing that made the problem tractable without blowing all my memory)
        # is to set an expectation of the lower bound of the score before doing the tree search, and prune any
        # branches that can't achieve this score. I use a greedy semi-randomised initial search to get a rough
        # lower bound, followed by a tree search with a heuristic to heavily prune the tree (always build a geode
        # robot if available; always build an obsidian robot if it's the best available). With a decently high
        # lower bound the exact search is easy, even without using the rule I got from reddit.
        if len(blueprints) > 3:
            blueprints = blueprints[:3]
        scores = []
        for blueprint in blueprints:
            lower_bound = greedy_lower_bound(blueprint, 32)
            lower_bound = max_score(blueprint, 32, lower_bound, heuristic = True)
            score = max_score(blueprint, 32, lower_bound, heuristic = False)
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
            lower_bound = greedy_lower_bound(blueprint, 24)
            lower_bound = max_score(blueprint, 24, lower_bound, heuristic = True)
            score = max_score(blueprint, 24, lower_bound, heuristic = False)
            scores.append(score)
            print(score)
            print(scores)
        print(scores)

        ids = [bp.get_blueprint_id() for bp in blueprints]
        result = sum(score*id for (score, id) in zip(scores, ids))
        print(f'Part 1: {result}')
