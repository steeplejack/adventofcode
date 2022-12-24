import enum
from collections import namedtuple, Counter
Move = enum.Enum("Move", "NW N NE E SE S SW W NONE")
Position = namedtuple("Position", "x y")

class Elf():
    def __init__(self, name, position):
        self.name = name
        self.position = position
        self.pending = position

    def __repr__(self):
        return f'Elf({self.name}, {self.position})'

    def __str__(self):
        return f'Elf({self.name}, {self.position}, {self.pending})'

    def add_pending(self, move: Move):
        x, y = self.position
        if move == Move.NW:
            self.pending = Position(x-1, y-1)
        elif move == Move.N:
            self.pending = Position(x, y-1)
        elif move == Move.NE:
            self.pending = Position(x+1, y-1)
        elif move == Move.E:
            self.pending = Position(x+1, y)
        elif move == Move.SE:
            self.pending = Position(x+1, y+1)
        elif move == Move.S:
            self.pending = Position(x, y+1)
        elif move == Move.SW:
            self.pending = Position(x-1, y+1)
        elif move == Move.W:
            self.pending = Position(x-1, y)
        else:
            self.pending = self.position

    def clear_pending(self):
        self.pending = self.position

    def update(self):
        if self.pending and self.position != self.pending:
            self.position = self.pending
            return 1
        return 0


def check_neighbours(elf, elves):
    x, y = elf.position
    neighbours = {}
    positions = set(elf.position for elf in elves)
    neighbours['NW'] = (x-1, y-1) in positions
    neighbours['N'] = (x, y-1) in positions
    neighbours['NE'] = (x+1, y-1) in positions
    neighbours['W'] = (x-1, y) in positions
    neighbours['E'] = (x+1, y) in positions
    neighbours['SW'] = (x-1, y+1) in positions
    neighbours['S'] = (x, y+1) in positions
    neighbours['SE'] = (x+1, y+1) in positions
    return neighbours

def propose_move(elf, neighbours, round_number):
    if not any(neighbours.values()):
        elf.clear_pending()
        return 

    def rule1():
        if not (neighbours['NW'] or neighbours['N'] or neighbours['NE']):
            return Move.N
        return Move.NONE

    def rule2():
        if not (neighbours['SW'] or neighbours['S'] or neighbours['SE']):
            return Move.S
        return Move.NONE

    def rule3():
        if not (neighbours['SW'] or neighbours['W'] or neighbours['NW']):
            return Move.W
        return Move.NONE

    def rule4():
        if not (neighbours['SE'] or neighbours['E'] or neighbours['NE']):
            return Move.E
        return Move.NONE
    rules = [rule1, rule2, rule3, rule4]

    for i in range(round_number, round_number + len(rules)):
        i %= len(rules)
        move = rules[i]()
        if move != Move.NONE:
            elf.add_pending(move)
            return

def apply_pending(elves):
    counter = Counter(elf.pending for elf in elves)
    n_moved = 0
    for elf in elves:
        if counter[elf.pending] == 1:
            n_moved += elf.update()
        else:
            elf.clear_pending()
    return n_moved

def get_bounds(elves):
    return (
            min(elf.position.x for elf in elves),
            max(elf.position.x for elf in elves),
            min(elf.position.y for elf in elves),
            max(elf.position.y for elf in elves)
            )

def draw_elves(elves):
    x0, x1, y0, y1 = get_bounds(elves)
    w = x1 - x0 + 1
    h = y1 - y0 + 1
    grid = [['.'] * w for row in range(h)]
    for elf in elves:
        x, y = elf.position
        grid[y - y0][x - x0] = '#'
    return '\n'.join(''.join(row) for row in grid)

    

if __name__ == "__main__":
    filename = 'input.txt'


    elves = list()
    name = 0
    with open(filename) as fl:
        for y, line in enumerate(fl):
            line = line.strip()
            for x, char in enumerate(line):
                if char == '#':
                    elf = Elf(name, Position(x, y))
                    elves.append(elf)
                    name += 1

    print (f"{len(elves)} ELVES!")
    round = 0
    while True:
        for elf in elves:
            nb = check_neighbours(elf, elves)
            propose_move(elf, nb, round)
        
        n_moved = apply_pending(elves)
        print(f'    Round = {round}, #Moved = {n_moved}')
        # print(str(round) + '\n' + draw_elves(elves) + '\n\n')
        
        if round == 9:
            x0, x1, y0, y1 = get_bounds(elves)
            h = x1 - x0 + 1
            w = y1 - y0 + 1
            score = h * w - len(elves)
            print(f'Part 1: {score}')

        if n_moved == 0:
            print(f'Part 2: {round + 1}')
            break

        round += 1

