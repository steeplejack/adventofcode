import queue
from typing import List, Tuple

# Hello, code from 2022, day 12
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

# So, I was busy writing a presentation, and
# I made no effort to tidy up this code.
# Cue plain scripting and repeatedly
# looping over the data.
grid = []
nrows = 0
ncols = 0
startpos = None
startnode = None
with open('../input.txt') as fl:
    array = [line.strip() for line in fl.readlines()]

# Modify the input: double the resolution of the graph
# by interspersing blank rows and columns. Original
# graph entries can be identified later because they'll
# have odd row and col indices.
# Interspersing adds blank rows at the start and end of
# the data, which I can rely on to be "outside" the graph
new_array = []
dummy_row = ' ' * len(array[0])
for line in array:
    new_array.append(dummy_row)
    assert len(dummy_row) == len(line)
    new_array.append(line)
new_array.append(dummy_row)

def intersperse(row):
    r = [' ']
    for char in row:
        r.append(char)
        r.append(' ')
    return r

array = [intersperse(row) for row in new_array]

# these modifications are to reconnect pipes
# that have been interrupted by the new blank
# rows and columns
for i in range(len(array)):
    for j in range(len(array[0])):
        if array[i][j] == ' ':
            changes = 0
            if i > 0:
                if array[i-1][j] in '|F7':
                    array[i][j] = '|'
                    changes += 1
            if i + 1 < len(array):
                if array[i+1][j] in '|JL':
                    array[i][j] = '|'
                    changes += 1
            if j > 0:
                if array[i][j-1] in '-LF':
                    array[i][j] = '-'
                    changes += 1
            if j + 1 < len(array[i]):
                if array[i][j+1] in '-J7':
                    array[i][j] = '-'
                    changes += 1
            assert changes <= 2

# Build graph from modified input
grid = []
startpos = None
startnode = None
for i in range(len(array)):
    gridrow = []
    for j in range(len(array[0])):
        char = array[i][j]
        node = Node(i, j, char)
        if char == '-': assert len(node.neighbours) > 0
        if char == 'S':
            assert startpos is None
            startpos = (i, j)
            startnode = node
        gridrow.append(node)
    grid.append(gridrow)


# print('\n'.join(''.join(row) for row in array))
    
# No wrap-around connections
graph = {}
nrows = len(grid)
ncols = len(grid[0])
for row in grid:
    for col in row:
        col.filter_neighbours(nrows, ncols)

# Who connects to 'S'?
for row in grid:
    for col in row:
        if startpos in col.neighbours:
            startnode.neighbours.append(col.coord)


# Build the graph dictionary
for row in grid:
    for col in row:
        graph[col.coord] = col.neighbours

paths, seen = bfs_all_paths(graph, startpos)

# Delete any pipes that are not in the main circuit
# by changing them to a blank character
for i in range(nrows):
    for j in range(ncols):
        if not (i, j) in seen:
            if grid[i][j].text not in '. ':
                if i % 2 == 1 and j % 2 == 1:
                    grid[i][j] = Node(i, j, '.')
                else:
                    grid[i][j] = Node(i, j, ' ')

def grid_to_string(grid):
    p = []
    for row in grid:
        s=[]
        for col in row:
            s.append(col.text)
        p.append(''.join(s))
    return '\n'.join(p)

# print(grid_to_string(grid))

# Connect empty ('.' | ' ') cells together so
# I can do a flood-fill of all "outside" cells
for i in range(nrows):
    for j in range(ncols):
        if grid[i][j].text in '. ':
            for ii in (i-1,i,i+1):
                if ii < 0 or ii >= nrows:
                    continue
                for jj in (j-1,j,j+1):
                    if jj < 0 or jj >= ncols:
                        continue
                    if i == ii and j == jj:
                        continue
                    if grid[ii][jj].text in '. ':
                        if i == ii or j == jj:
                            graph[(i, j)].append((ii, jj))

# Flood-fill
_, outside = bfs_all_paths(graph, (0, 0))

# Anything that is not part of the "outside" or 
# main circuit connected components must be "inside"
# Count only the original cells (odd-indices)
count = 0
for i in range(nrows):
    for j in range(ncols):
        if i % 2 == 1 and j % 2 == 1:
            if (i, j) not in outside and (i, j) not in seen:
                count += 1
# This is the answer!
print(count)
