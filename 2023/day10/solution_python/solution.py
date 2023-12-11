import queue
from typing import List, Tuple

def bfs_sp(graph, start, end) -> List[Tuple[int,int]]:
    if start == end:
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

                if neighbour == end:
                    return new_path

            seen.add(node)

    return []

def bfs_all_paths(graph, start):
    paths = {}

    paths[start] = [start]

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

                if not neighbour in seen:
                    paths[neighbour] = new_path

            seen.add(node)

    return paths, seen



class Node:
    def __init__(self, row, col, text):
        self.row = row
        self.col = col
        self.text = text
        self.isstart = text == 'S'
        self.neighbours = self._make_neighbours()

    @property
    def coord(self):
        return (self.row, self.col)

    def __repr__(self):
        return self.text

    def _make_neighbours(self):
        r, c = self.coord
        if self.text == '|':
            neighbours = [(r - 1, c), (r + 1, c)]
        elif self.text == '-':
            neighbours = [(r, c - 1), (r, c + 1)]
        elif self.text == 'F':
            neighbours = [(r + 1, c), (r, c + 1)]
        elif self.text == 'L':
            neighbours = [(r - 1, c), (r, c + 1)]
        elif self.text == 'J':
            neighbours = [(r - 1, c), (r, c - 1)]
        elif self.text == '7':
            neighbours = [(r + 1, c), (r, c - 1)]
        else:
            neighbours = []
        return neighbours

    def filter_neighbours(self, row_length, col_length):
        self.neighbours = [nb for nb in self.neighbours
                           if (0 <= nb[0] < row_length) and (0 <= nb[1] < col_length)]

grid = []
nrows = 0
ncols = 0
startpos = None
startnode = None
with open('../input.txt') as fl:
    for i, line in enumerate(fl):
        nrows += 1
        row = list(line.strip())
        if ncols != 0: assert len(row) == ncols
        ncols = len(row)
        gridrow = []
        for j, char in enumerate(row):
            node = Node(i, j, char)
            if char == 'S':
                assert startpos is None
                startpos = (i, j)
                startnode = node
            gridrow.append(node)
        grid.append(gridrow)

# No wrap-around connections
graph = {}
for row in grid:
    for col in row:
        col.filter_neighbours(nrows, ncols)

# Who connects to 'S'?
for row in grid:
    for col in row:
        if startpos in col.neighbours:
            startnode.neighbours.append(col.coord)

x = []
for nb in startnode.neighbours:
    x.append((nb[0]-startpos[0], nb[1] - startpos[1]))
if (0, 1) in x and (1, 0) in x:
    startnode.text = 'F'
elif (0, 1) in x and (0, -1) in x:
    startnode.text = '-'
elif (0, 1) in x and (-1, 0) in x:
    startnode.text = 'L'
elif (0, -1) in x and (1, 0) in x:
    startnode.text = '7'
elif (0, -1) in x and (-1, 0) in x:
    startnode.text = 'J'
elif (-1, 0) in x and (1, 0) in x:
    startnode.text = '|'
else:
    raise Exception()

# Build the graph dictionary
for row in grid:
    for col in row:
        if col.text != '.':
            graph[col.coord] = col.neighbours

# Shortest paths:
longest_shortest_path = [-1, None]

paths, seen = bfs_all_paths(graph, startpos)

furthest_node = max(paths, key = lambda x: len(paths[x]))
longest_path = paths[furthest_node]
print(f"Furthest distance found at point {furthest_node} at {len(longest_path) - 1} steps")

for row in grid:
    for col in row:
        if not col.coord in seen:
            col.text = '.'


def grid_to_string(grid):
    p = []
    for row in grid:
        s=[]
        for col in row:
            s.append(col.text)
        p.append(''.join(s))
    return '\n'.join(p)

# print(grid_to_string(grid))

js = []
for row in grid:
    io = 0
    s=''.join([n.text for n in row])
    j = []
    for char in s:
        if char in '.':
            j.append('O' if io % 2 == 0 else 'I')
        else:
            j.append('.')
        if char in '7F|':
            io += 1
    js.append(''.join(j))

count = 0
for j in js:
    count += j.count('I')

