import queue
import sys

def char_to_height(char):
    if char == 'S':
        return 0
    elif char == 'E':
        return 25
    else:
        return ord(char) - ord('a')

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

    nrow = len(grid)
    ncol = len(grid[0])

    # Nodes is a mapping from grid position to height,
    # graph is a mapping from grid position to neighbours
    #   reachable from this position
    # reverse_graph is a mapping from grid position to
    #   neighbours from which the current pos is reachable
    #   (used when searching backwards from an end point to
    #    a start point)
    nodes = {}
    graph = {}
    reverse_graph = {}

    start = None
    end = None
    for i in range(nrow):
        for j in range(ncol):
            val = grid[i][j]
            height = char_to_height(val)
            if val == 'S':
                start = (i, j)
            if val == 'E':
                end = (i, j)
            nodes[(i, j)] = height
            graph[(i, j)] = []
            reverse_graph[(i, j)] = []

    # Make connections
    for i, j in nodes:
        height = nodes[(i, j)]

        left = (i, j-1)
        right = (i, j+1)
        up = (i-1, j)
        down = (i+1, j)

        for n in (left, right, up, down):
            if n in nodes:
                h = nodes[n]
                if h - height <= 1:
                    graph[(i, j)].append(n)
                if height - h <= 1:
                    reverse_graph[(i, j)].append(n)

    distances, backtracks = dijkstra(graph, start, end)
    shortest_path = distances[end]
    print(f'Part 1: {shortest_path}')

    distances, backtracks = dijkstra(reverse_graph, end)
    distances = {k: v for k, v in distances.items() if v < sys.maxsize}
    sorted_paths = sorted(distances, key = lambda x: distances[x])
    a_list = []
    shortest_path = sys.maxsize
    for p in sorted_paths:
        i, j = p
        if grid[i][j] == 'a':
            a_list.append(p)
            if distances[p] < shortest_path:
                shortest_path = distances[p]
    print(f'Part 2: {shortest_path}')

