"""
active (2) 0-1: yes no
cell types (3) 00-11 = 0-3:      empty splitter mirror
orientations (2) 0-1:      splitter_vertical splitter_horizontal mirror_forward mirror_back
light directions (4) 0000-1111 = 0-15: up down left right
status (2) 0-1: on off

can store in 9 bits:

0|00|0|0000|0
-|--|-|----|-
       LDRU
a t  o d    s
c y  r i    t
t p  i r    a
i e  e e    t
v    n c    u
e    t t    s
     a i
     t o
     i n
     o
     n 
"""

import argparse
import pathlib
from copy import deepcopy

char_to_cell_mapping = {
    '.':  0b00000000,
    '-':  0b01000000,
    '|':  0b01100000,
    '/':  0b10000000,
    '\\': 0b10100000
}

# bitmasks
LEFT   = 0b1000
RIGHT  = 0b0010
UP     = 0b0001
DOWN   = 0b0100
ACTIVE = 0b100000000

def parse_args():
    parser = argparse.ArgumentParser("AoC 2023 Day 16")
    parser.add_argument("infile", type=pathlib.Path)
    return parser.parse_args()

def parse_grid(infile):
    with open(infile) as fl:
        return [[char_to_cell_mapping[char] for char in list(line.strip())] for line in fl]

def toggle_on(cell):
    return cell ^ 1

def switch_on(cell):
    return cell | 1

def switch_off(cell):
    return (cell | 1) ^ 1

def cell_is_on(cell):
    return cell & 1 == 1

def cell_is_mirror(cell):
    return (cell >> 6) & 0b11 == 0b10

def cell_is_splitter(cell):
    return (cell >> 6) & 0b11 == 0b01

def cell_is_empty(cell):
    return (cell >> 6) & 0b11 == 0b00

def cell_direction(cell):
    return (cell >> 1) & 0b1111

def cell_orientation(cell):
    return cell >> 5 & 1

def make_active(cell):
    return cell | ACTIVE

def make_inactive(cell):
    return make_active(cell) ^ ACTIVE

def cell_is_active(cell):
    return cell & ACTIVE == ACTIVE

def cell_neighbourhood(cell):
    nb = []
    if not cell_is_on(cell):
        return []
    else:
        dirs = cell_direction(cell)
        if dirs & UP == UP:
            nb.append((-1, 0, UP)) # N
        if dirs & RIGHT == RIGHT:
            nb.append((0, 1, RIGHT))  # E
        if dirs & DOWN == DOWN:
            nb.append((1, 0, DOWN))  # S
        if dirs & LEFT == LEFT:
            nb.append((0, -1, LEFT)) # W
    return nb

def illuminate(cell, incoming_direction):
    """
    incoming direction is the direction the incoming beam is travelling
    With a blank cell, the emitted light travels in the same direction
      as incoming,
    With a splitter the light will emit as follows:
      '|' + LEFT   -> UP and DOWN      1000 -> 0101  =  8 -> 5
      '|' + RIGHT  -> UP and DOWN      0010 -> 0101  =  2 -> 5
      '|' + UP     -> UP               0001 -> 0001  =  1 -> 1
      '|' + DOWN   -> DOWN             0100 -> 0100  =  4 -> 4
      '-' + UP     -> LEFT and RIGHT   0001 -> 1010  =  1 -> 10
      '-' + UP     -> LEFT and RIGHT   0100 -> 1010  =  4 -> 10
      '-' + LEFT   -> LEFT             1000 -> 1000  =  8 -> 8
      '-' + RIGHT  -> RIGHT            0010 -> 0010  =  2 -> 2
    With a mirror the light emits as follows:
      '/'  + LEFT   ->  DOWN      1000 -> 0100  =  8 -> 4
      '/'  + RIGHT  ->  UP        0010 -> 0001  =  2 -> 1
      '/'  + UP     ->  RIGHT     0001 -> 0010  =  1 -> 2
      '/'  + DOWN   ->  LEFT      0100 -> 1000  =  4 -> 8
      '\\' + LEFT   ->  UP        1000 -> 0001  =  8 -> 1
      '\\' + RIGHT  ->  DOWN      0010 -> 0100  =  2 -> 4
      '\\' + UP     ->  LEFT      0001 -> 1000  =  4 -> 2
      '\\' + DOWN   ->  RIGHT     0100 -> 0010  =  1 -> 8
    """
    # print(f'Illuminating cell with value {cell} ( {b9(cell)} )')
    # print(f'Incoming direction = {b4(incoming_direction)}')
    lit_cell = make_active(switch_on(cell))
    # print(f'Cell is lit: {cell} ( {b9(cell)} )')

    if cell_is_empty(cell):
        # print(" EMPTY CELL")
        return lit_cell | (incoming_direction << 1)
    elif cell_is_mirror(cell):
        # print(" MIRROR CELL")
        if cell_orientation(cell) == 0: # '/'
            # print("  ORIENTATION 0 = '/'")
            if incoming_direction == LEFT:
                return lit_cell | (DOWN << 1)
            if incoming_direction == RIGHT:
                return lit_cell | (UP << 1)
            if incoming_direction == UP:
                return lit_cell | (RIGHT << 1)
            if incoming_direction == DOWN:
                return lit_cell | (LEFT << 1)
        if cell_orientation(cell) == 1: # '\\'
            # print("  ORIENTATION 1 = '\\'")
            if incoming_direction == LEFT:
                return lit_cell | (UP << 1)
            if incoming_direction == RIGHT:
                return lit_cell | (DOWN << 1)
            if incoming_direction == UP:
                return lit_cell | (LEFT << 1)
            if incoming_direction == DOWN:
                return lit_cell | (RIGHT << 1)
    elif cell_is_splitter(cell):
        # print(" SPLITTER CELL")
        if cell_orientation(cell) == 0: # '-'
            # print("  ORIENTATION 0 = '-'")
            if incoming_direction == LEFT or incoming_direction == RIGHT:
                return lit_cell | (incoming_direction << 1)
            if incoming_direction == UP or incoming_direction == DOWN:
                return lit_cell | ((LEFT|RIGHT) << 1)
        if cell_orientation(cell) == 1: # '|'
            # print("  ORIENTATION 1 = '|'")
            if incoming_direction == UP or incoming_direction == DOWN:
                return lit_cell | (incoming_direction << 1)
            if incoming_direction == LEFT or incoming_direction == RIGHT:
                return lit_cell | ((UP|DOWN) << 1)
    else:
        print(" UNKNOWN CELL")
        raise ValueError("Unknown cell type")

def b4(i):
    if i < 0 or i > 15: raise ValueError("Not a 4bit uint")
    return f'{i:04b}'

def b8(i):
    if i < 0 or i > 255: raise ValueError("Not an 8bit uint")
    return f'{i:08b}'

def b9(i):
    if i < 0 or i > 511: raise ValueError("Not a 9bit uint")
    return f'{i:09b}'

def initialise_grid(grid, i=0, j=0, direction=RIGHT):
    new_grid = deepcopy(grid)
    new_grid[i][j] = illuminate(new_grid[i][j], direction)
    return new_grid

def in_bounds(i, j, max_i, max_j):
    return i >= 0 and i < max_i and j >= 0 and j < max_j

def update_grid(grid):
    new_grid = deepcopy(grid)
    max_i = len(grid)
    max_j = len(grid[0])
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            cell = grid[i][j]
            if cell_is_active(cell):
                neighbourhood = cell_neighbourhood(cell)
                # print(f'**The cell at {i},{j} (={cell}, {b9(cell)}) is on and its neighbourhood is {neighbourhood}')
                for ni, nj, direction in neighbourhood:
                    if in_bounds(i+ni, j+nj, max_i, max_j):
                        # print(f'**Illuminating cell at {i+ni},{j+nj} in direction {direction}')
                        new_grid[i+ni][j+nj] = illuminate(new_grid[i+ni][j+nj], direction)
                new_grid[i][j] = make_inactive(cell)
    return new_grid, (changed := not (new_grid == grid))

def cell_to_str(cell):
    if cell_is_active(cell):
        return '*'
    if cell_is_mirror(cell):
        return '/' if cell_orientation(cell) == 0 else '\\'
    if cell_is_splitter(cell):
        return '-' if cell_orientation(cell) == 0 else '|'
    if cell_is_empty(cell):
        n_beams = len(cell_neighbourhood(cell))
        if n_beams == 0:
            return '.'
        if n_beams == 1:
            if cell_direction(cell) == LEFT: return '<'
            elif cell_direction(cell) == RIGHT: return '>'
            elif cell_direction(cell) == UP: return '^'
            else: return 'v'
        else:
            return(str(n_beams))

def grid_to_str(grid):
    rows = []
    for row in grid:
        rowchars = [cell_to_str(cell) for cell in row]
        rows.append(''.join(rowchars))
    return '\n'.join(rows)

def grid_to_tuple(grid):
    return tuple(tuple(row) for row in grid)

def count_lit_cells(grid):
    return sum(x & 1 for row in grid for x in row)

grid = parse_grid('/Users/kg8/code/aoc/2023/day16/input.txt')
grid = initialise_grid(grid)
changed = True
niter = 0
seen_states = Counter()
seen_states.update([grid_to_str(grid)])
while True:
    grid, changed = update_grid(grid)
    #print(f'{niter}\n{grid_to_str(grid)}\n{count_lit_cells(grid)}\n')
    niter += 1
    print(count_lit_cells(grid))
    seen_states.update([grid_to_str(grid)])
    if seen_states[grid_to_str(grid)] > 10:
        break
print(count_lit_cells(grid))


def energized(grid, memo = None):
    """
    Memoizing like this isn't much help - it early-exited 5 times out of 440
    """
    if memo == None:
        memo = {}
    changed = True
    niter = 0
    seen_states = Counter()
    seen_states.update([grid_to_tuple(grid)])
    while True:
        key = grid_to_tuple(grid)
        if key in memo:
            print('early exit!')
            score = memo[key]
            break
        grid, changed = update_grid(grid)
        key = grid_to_tuple(grid)
        niter += 1
        seen_states.update([key])
        if seen_states[key] > 10:
            break

    score = count_lit_cells(grid)
    for state in seen_states:
        memo[state] = score
    return score, memo

# Part 1
init_grid = parse_grid('/Users/kg8/code/aoc/2023/day16/input.txt')
grid = initialise_grid(deepcopy(init_grid), 0, 0, RIGHT)
score, memo_ = energized(grid)
print(f'Answer to part 1 = {score}')

# Part 2
init_grid = parse_grid('/Users/kg8/code/aoc/2023/day16/input.txt')
nrow = len(init_grid)
ncol = len(init_grid[0])
scores = {(0, 0, 0): 0}
memo_ = {}
for i in range(nrow):
    print(f'i={i}: max score so far={scores[max(scores,key=lambda x: scores[x])]}')
    grid = initialise_grid(deepcopy(init_grid), i, 0, RIGHT)
    score, memo_ = energized(grid, memo_)
    scores[(i, 0, RIGHT)] = score
    grid = initialise_grid(deepcopy(init_grid), i, ncol-1, LEFT)
    score, memo_ = energized(grid, memo_)
    scores[(i, ncol-1, LEFT)] = score

for j in range(ncol):
    print(f'j={j}: max score so far={scores[max(scores,key=lambda x: scores[x])]}')
    grid = initialise_grid(deepcopy(init_grid), 0, j, DOWN)
    score, memo_ = energized(grid, memo_)
    scores[(0, j, DOWN)] = score
    grid = initialise_grid(deepcopy(init_grid), nrow-i, j, UP)
    score, memo_ = energized(grid, memo_)
    scores[(nrow-i, j, UP)] = score

