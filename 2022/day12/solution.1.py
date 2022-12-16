import queue
import sys

class Node():
    def __init__(self, char, row, col):
        self.l = None
        self.r = None
        self.u = None
        self.d = None
        self.z = char_to_height(char)
        self.i = row
        self.j = col

def char_to_height(char):
    if char == 'S':
        return 0
    elif char == 'E':
        return 25
    else:
        return ord(char) - ord('a')

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


def dijkstra(graph, source, sink = None):
    dist = {source: 0}
    prev = {}
    q = queue.PriorityQueue()
    q.put((dist[source], source))

    for node in graph:
        if node != source:
            dist[node] = sys.maxsize
            prev[node] = None

    while not q.empty():
        _, u = q.get()
        if sink and sink == u:
            return dist, prev
        for v in graph[u]:
            d = dist[u] + 1 # All distances are 1 in the graphs we are considering
            if d < dist[v]:
                dist[v] = d
                prev[v] = u
                q.put((dist[v], v))

    return dist, prev

if __name__ == "__main__":
    infile = "input.txt"

    with open(infile) as fl:
        grid = [list(x) for x in fl.read().strip().split()]

    nodes = {}
    graph = {}
    reverse_graph = {}

    nrow = len(grid)
    ncol = len(grid[0])
    for i in range(nrow):
        assert len(grid[i]) == ncol

    start = None
    end = None
    potential_starts = []
    for i in range(nrow):
        for j in range(ncol):
            val = grid[i][j]
            if val == 'S':
                start = (i, j)
                potential_starts.append((i, j))
            if val == 'E':
                end = (i, j)
            if val == 'a':
                potential_starts.append((i, j))
            node = Node(val, i, j)
            nodes[(i, j)] = node
            graph[(i, j)] = []
            reverse_graph[(i, j)] = []

    # Make connections
    for i, j in nodes:
        node = nodes[(i, j)]
        assert (i, j) == (node.i, node.j)
        left = (i, j-1)
        right = (i, j+1)
        up = (i-1, j)
        down = (i+1, j)

        if left[1] >= 0:
            left_node = nodes.get(left)
            if left_node and (left_node.z - node.z) <= 1:
                node.l = left_node
                graph[(i, j)].append(left)
            if left_node and (node.z - left_node.z) <= 1:
                reverse_graph[(i, j)].append(left)

        if right[1] < ncol:
            right_node = nodes.get(right)
            if right_node and (right_node.z - node.z) <= 1:
                node.r = right_node
                graph[(i, j)].append(right)
            if right_node and (node.z - right_node.z) <= 1:
                reverse_graph[(i, j)].append(right)
            
        if up[0] >= 0:
            up_node = nodes.get(up)
            if up_node and (up_node.z - node.z) <= 1:
                node.u = up_node
                graph[(i, j)].append(up)
            if up_node and (node.z - up_node.z) <= 1:
                reverse_graph[(i, j)].append(up)

        if down[0] < nrow:
            down_node = nodes.get(down)
            if down_node and (down_node.z - node.z) <= 1:
                node.d = down_node
                graph[(i, j)].append(down)
            if down_node and (node.z - down_node.z) <= 1:
                reverse_graph[(i, j)].append(down)

    shortest_path = bfs_sp(graph, start, end)
    shortest_path.remove(start)
    print(f'Part 1: {len(shortest_path)}')

    paths = {}
    print(f"Checking {len(potential_starts)} potential starts")

    # potential_starts = set(potential_starts)
    while potential_starts:
        start = potential_starts.pop()
        sp = bfs_sp(graph, start, end)
        if sp:
            sp.remove(start)
            paths[start] = len(sp)
            # print(f"  {start}->{len(sp)}")
            # Prune the list
            a_nodes = []
            for node in sp:
                i, j = node
                if grid[i][j] == 'a':
                    a_nodes.append(node)
            if len(a_nodes) > 0:
                a_nodes.pop()
                for node in a_nodes:
                    if node in potential_starts:
                        potential_starts.remove(node)

        # else:
        #     print(f"  {start} X")

    shortest = sorted(paths, key = lambda x: paths[x])[0]
    print(f'Part 2: {paths[shortest]}')

