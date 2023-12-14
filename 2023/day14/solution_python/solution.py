from copy import deepcopy
from collections import defaultdict

def tilt_north(orig_grid):
    grid = deepcopy(orig_grid)
    nswaps = 1
    while nswaps > 0:
        nswaps = 0
        for i in range(1, len(grid)):
            row = grid[i]
            for j in range(len(row)):
                if grid[i][j] == 'O' and grid[i-1][j] == '.':
                    grid[i-1][j], grid[i][j] = grid[i][j], grid[i-1][j]
                    nswaps += 1
    return grid

def tilt_south(orig_grid):
    grid = deepcopy(orig_grid)
    nswaps = 1
    while nswaps > 0:
        nswaps = 0
        for i in reversed(range(len(grid) - 1)):
            row = grid[i]
            for j in range(len(row)):
                if grid[i][j] == 'O' and grid[i+1][j] == '.':
                    grid[i+1][j], grid[i][j] = grid[i][j], grid[i+1][j]
                    nswaps += 1
    return grid

def tilt_west(orig_grid):
    grid = deepcopy(orig_grid)
    nswaps = 1
    while nswaps > 0:
        nswaps = 0
        for i in range(len(grid)):
            row = grid[i]
            for j in range(1, len(row)):
                if grid[i][j] == 'O' and grid[i][j-1] == '.':
                    grid[i][j], grid[i][j-1] = grid[i][j-1], grid[i][j]
                    nswaps += 1
    return grid

def tilt_east(orig_grid):
    grid = deepcopy(orig_grid)
    nswaps = 1
    while nswaps > 0:
        nswaps = 0
        for i in range(len(grid)):
            row = grid[i]
            for j in reversed(range(len(row) - 1)):
                if grid[i][j] == 'O' and grid[i][j+1] == '.':
                    grid[i][j], grid[i][j+1] = grid[i][j+1], grid[i][j]
                    nswaps += 1
    return grid

def score_grid(grid):
     total = 0
     max_weight = len(grid)
     for i, row in enumerate(grid):
          n_rocks = row.count('O')
          weight = max_weight - i
          total += n_rocks * weight
     return total

def cycle(orig_grid):
    grid = tilt_north(orig_grid)
    grid = tilt_west(grid)
    grid = tilt_south(grid)
    return tilt_east(grid)

def cycle_n(orig_grid, n):
    grid = deepcopy(orig_grid)
    for _ in range(n):
        grid = cycle(grid)
    return grid

def grid_to_string(grid):
    return '\n'.join(''.join(row) for row in grid)

def grid_from_string(s):
    return [list(x) for x in s.split('\n')]

def part1(infile):
    with open(infile) as fl:
        grid = [list(line.strip()) for line in fl]

    tilted = tilt_north(grid)
    score = score_grid(tilted)
    return score

def run_until_cycles_detected(orig_grid):
    grid = deepcopy(orig_grid)
    d = defaultdict(list)
    i = 1
    while True:
        grid = cycle(grid)
        s = grid_to_string(grid)
        d[s].append(i)
        if len(d[s]) == 5:
            return d
        i += 1

def diff(l):
    return [l[i] - l[i-1] for i in range(1, len(l))]

def part2(infile):
    with open(infile) as fl:
        grid = [list(line.strip()) for line in fl]
    d = run_until_cycles_detected(grid)
    cycle_size = diff(d[max(d, key=lambda x: len(d[x]))])
    assert len(set(cycle_size)) == 1 and len(cycle_size) > 1

    target = 1000000000
    n = target % cycle_size[0]
    
    for k, val in d.items():
        if len(val) > 1 and val[0] % cycle_size[0] == n:
            return score_grid(grid_from_string(k))




def main():
     print(f'Answer to part 1 = {part1("../input.txt")}')
     print(f'Answer to part 2 = {part2("../input.txt")}')

if __name__ == '__main__':
     main()