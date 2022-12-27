from collections import namedtuple
from enum import Enum
from collections import Counter
import copy
import math

Direction = Enum("Direction", "UP DOWN LEFT RIGHT")
Position = namedtuple("Position", "x y")

chars = {Direction.LEFT: '<',
         Direction.RIGHT: '>',
         Direction.UP: '^',
         Direction.DOWN: 'v'}

def bfs_sp(graph, start, end_x, end_y):
    if start[0] == end_x and start[1] == end_y:
        return [start]

    seen = set()
    queue = [[start]]

    while queue:
        path = queue.pop(0)
        node = path[-1]

        if node not in seen:
            neighbours = graph[node]

            for neighbour in neighbours:
                new_path = path[:] # copy
                new_path.append(neighbour)
                queue.append(new_path)

                if neighbour[0] == end_x and neighbour[1] == end_y:
                    return new_path

            seen.add(node)
    return []

class Blizzard():
    def __init__(self, position, direction):
        self.pos = position
        self.dir = direction
        self.char = chars[direction]

    def __repr__(self):
        return f'Blizzard({self.pos}, {self.char})'

    def advance(self, grid):
        x, y = self.pos
        if self.dir == Direction.UP:
            y -= 1
        elif self.dir == Direction.DOWN:
            y += 1
        elif self.dir == Direction.LEFT:
            x -= 1
        elif self.dir == Direction.RIGHT:
            x += 1
        else:
            raise ValueError("Unexpected enum value")

        if x < 1:
            x = len(grid[0]) - 2
        if x > len(grid[0]) - 2:
            x = 1
        if y < 1:
            y = len(grid) - 2
        if y > len(grid) - 2:
            y = 1
        self.pos = Position(x, y)

def update(grid, blizzards):
    new_grid = copy.deepcopy(grid)
    for x in range(1, len(grid[0])-1):
        for y in range(1, len(grid) - 1):
            new_grid[y][x] = '.'

    for blz in blizzards:
        blz.advance(grid)
        x, y = blz.pos
        new_grid[y][x] = blz.char

    c = Counter(blz.pos for blz in blizzards)
    for pos in c:
        x, y = pos
        if c[pos] > 1:
            new_grid[y][x] = str(c[pos])

    return new_grid

def draw(grid):
    print('\n'.join(''.join(row) for row in grid))


def cell_in_grids_is_open(grids, x, y, z):
    if x < 0 or y < 0 or z < 0:
        return False
    if z >= len(grids) or y >= len(grids[0]) or x >= len(grids[0][0]):
        return False
    return grids[z][y][x] == '.'


if __name__ == "__main__":
    filename = "input.txt"

    with open(filename) as fl:
        contents = fl.read().rstrip()

    grid = [list(x) for x in contents.split('\n')]

    blizzards = []
    for x in range(len(grid[0])):
        for y in range(len(grid)):
            char = grid[y][x]
            if char == '<':
                blizzards.append(Blizzard(Position(x, y), Direction.LEFT))
            elif char == '>':
                blizzards.append(Blizzard(Position(x, y), Direction.RIGHT))
            elif char == '^':
                blizzards.append(Blizzard(Position(x, y), Direction.UP))
            elif char == 'v':
                blizzards.append(Blizzard(Position(x, y), Direction.DOWN))
            else:
                continue

    # import os, time
    # for _ in range(240):
    #     grid = update(grid, blizzards)
    #     draw(grid)
    #     time.sleep(.25)
    #     os.system('clear')
    x, y = len(grid[0]) - 2, len(grid) - 2
    grids = []
    init = set(blz.pos for blz in blizzards)
    for _ in range(math.lcm(x, y)):
        grid = update(grid, blizzards)
        grids.append(grid)

    final = set(blz.pos for blz in blizzards)
    assert init == final

    graph = {}
    for z, grid in enumerate(grids):
        for y, row in enumerate(grid):
            for x, cell in enumerate(row):
                if x == 0 or x == len(row) - 1:
                    continue
                if y == 0 and x != 1:
                    continue
                if y == len(grid) - 1 and x != len(row) - 2:
                    continue
                nb = []
                if cell_in_grids_is_open(grids, x, y, z):
                    if cell_in_grids_is_open(grids, x, y, (z + 1) % len(grids)):
                        nb.append((x, y, (z + 1) % len(grids)))
                    if cell_in_grids_is_open(grids, x + 1, y, (z + 1) % len(grids)):
                        nb.append((x + 1, y, (z + 1) % len(grids)))
                    if cell_in_grids_is_open(grids, x - 1, y, (z + 1) % len(grids)):
                        nb.append((x - 1, y, (z + 1) % len(grids)))
                    if cell_in_grids_is_open(grids, x, y + 1, (z + 1) % len(grids)):
                        nb.append((x, y + 1, (z + 1) % len(grids)))
                    if cell_in_grids_is_open(grids, x, y - 1, (z + 1) % len(grids)):
                        nb.append((x, y - 1, (z + 1) % len(grids)))
                assert (x, y, z) not in graph
                graph[(x, y, z)] = nb

    p1 = bfs_sp(graph, (1,0,0), 120, 26)
    print(f'Part 1: {len(p1)}')

    end_p1 = p1[-1]
    x, y, z = end_p1
    p2 = bfs_sp(graph, (x, y, z + 1), 1, 0)

    end_p2 = p2[-1]
    x, y, z = end_p2
    p3 = bfs_sp(graph, (x, y, z + 1), 120, 26)

    print(f'Part 2: {len(p1) + len(p2) + len(p3)}')
