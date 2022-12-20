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

    def nn_inputs(self):
        p = list(self.params())
        b = [self.blueprint.get_ore_robot_cost(),
             self.blueprint.get_clay_robot_cost(),
             self.blueprint.get_obsidian_robot_cost()[0],
             self.blueprint.get_obsidian_robot_cost()[1],
             self.blueprint.get_geode_robot_cost()[0],
             self.blueprint.get_geode_robot_cost()[1]]
        return np.array(p + b, dtype=float)[:, np.newaxis]


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


import numpy as np
from scipy.special import softmax

def relu(arr):
    return np.clip(arr, 0, np.inf)

class NeuralNet():
    def __init__(self):
        self.w1 = np.random.random((5, 15))
        self.b1 = np.random.random((5, 1)) * 2 + 1

    def crossover(self, other):
        w = np.zeros_like(self.w1)
        b = np.zeros_like(self.b1)
        pw = np.random.random(w.shape)
        pb = np.random.random(b.shape)

        for i in range(w.shape[0]):
            for j in range(w.shape[1]):
                if pw[i, j] > 0.5:
                    w[i, j] = other.w1[i, j]
                else:
                    w[i, j] = self.w1[i, j]

        for i in range(b.shape[0]):
            if pb[i, 0] > 0.5:
                b[i, 0] = other.b1[i, 0]
            else:
                b[i, 0] = self.b1[i, 0]

        nn = NeuralNet()
        nn.w1 = w
        nn.b1 = b
        return nn

    def mutate(self):
        pw = np.random.random(self.w1.shape)
        pb = np.random.random(self.b1.shape)
        
        for i in range(pw.shape[0]):
            for j in range(pw.shape[1]):
                if pw[i, j] < 0.1:
                    self.w1[i, j] += np.random.normal(0, 0.1)

        for i in range(pb.shape[0]):
            if pb[i, 0] < 0.1:
                self.b1[i, 0] += np.random.normal(0, 0.1)

    def forward(self, inputs):
        return softmax(self.w1 @ inputs + self.b1)[:, 0]

    def move(self, factory):
        m = np.zeros(5)
        moves = factory.available_moves()
        inputs = factory.nn_inputs()
        if Moves.WAIT in moves:
            m[0] = 1
        if Moves.ORE in moves:
            m[1] = 1
        if Moves.CLAY in moves:
            m[2] = 1
        if Moves.OBSIDIAN in moves:
            m[3] = 1
        if Moves.GEODE in moves:
            m[4] = 1
        p = self.forward(inputs) * m
        p /= sum(p)
        return np.random.choice(
                [Moves.WAIT, Moves.ORE, Moves.CLAY, Moves.OBSIDIAN, Moves.GEODE],
                p = p)
        

class Agent():
    def __init__(self, network, factory):
        self.network = network
        self.factory = factory

    def evolve(self, steps):
        for _ in range(steps):
            move = self.network.move(self.factory)
            apply_move(self.factory, move)

    def score(self):
        return self.factory.geodes


def new_generation(agents):
    new_agents = []
    for _ in range(10):
        net = agents[0].network
        new_agents.append(Agent(net, Factory(blueprints[0])))
        net.mutate()
        new_agents.append(Agent(net, Factory(blueprints[0])))

    for i in range(10):
        for _ in range(2):
            net = agents[i].network
            new_agents.append(Agent(net, Factory(blueprints[0])))
            net.mutate()
            new_agents.append(Agent(net, Factory(blueprints[0])))

    for i in range(50):
        net = agents[i].network
        new_agents.append(Agent(net, Factory(blueprints[0])))
        net.mutate()
        new_agents.append(Agent(net, Factory(blueprints[0])))

    for i in range(9):
        for j in range(i+1, 10):
            net = agents[i].network.crossover(agents[j].network)
            new_agents.append(Agent(net, Factory(blueprints[0])))
            net.mutate()
            new_agents.append(Agent(net, Factory(blueprints[0])))

    for i in range(19):
        for j in range(i+1, 20):
            net = agents[i].network.crossover(agents[j].network)
            new_agents.append(Agent(net, Factory(blueprints[0])))
            net.mutate()
            new_agents.append(Agent(net, Factory(blueprints[0])))

    for _ in range(1000 - len(new_agents)):
        new_agents.append(Agent(NeuralNet(), Factory(blueprints[0])))
    agents = new_agents
    for agent in agents:
        agent.evolve(32)

    agents.sort(key = lambda x: x.score(), reverse = True)
    return agents

if __name__ == "__main__":
    filename = 'input.txt'
    with open(filename) as fl:
        blueprints = [parse_line(line) for line in fl]

    blueprints = blueprints[2:]

    agents = []
    for _ in range(1000):
        agent = Agent(NeuralNet(), factory = Factory(blueprints[0]))
        agent.evolve(32)
        agents.append(agent)

    agents.sort(key = lambda x: x.score(), reverse = True)
    print('Gen1=', agents[0].score())

    # Generation 2
    agents = new_generation(agents)
    print('Gen2=', agents[0].score())

    # Generation 3
    agents = new_generation(agents)
    print('Gen3=', agents[0].score())

    # Generation 4
    agents = new_generation(agents)
    print('Gen4=', agents[0].score())
    
    # Generation 5
    agents = new_generation(agents)
    print('Gen5=', agents[0].score())

    best = 0
    for i in range(6, 501):
        agents = new_generation(agents)
        score = agents[0].score()
        if score > best:
            best = score
        print(f'Gen{i}={score} (best={best})')
