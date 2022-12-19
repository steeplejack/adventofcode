import itertools
import math
import re
from collections import defaultdict
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


class Graph():
    def __init__(self):
        self.nodes = {}
        self.edges = {}
        self.nodes_in_order = []

    def __len__(self):
        return len(self.nodes)

    def add_node(self, node, flow):
        self.nodes[node] = flow
        self.nodes_in_order.append(node)
        self.nodes_in_order.sort()

    def add_edges(self, node, exits):
        self.edges[node] = exits

    def open_node(self, node):
        flow, open = self.nodes[node]
        if open:
            raise ValueError("Node is already open")
        self.nodes[node] = (flow, True)

    def get_flow(self, node):
        return self.nodes[node]

    def get_node_at_index(self, index):
        return self.nodes_in_order[index]

    def get_index_of_node(self, node):
        return self.nodes_in_order.index(node)

def parse_line(line):
    pattern = r"Valve ([A-Z]{2}) has flow rate=(\d+); tunnel[s]? lead[s]? to valve[s]? ([A-Z, ]+)"
    rgx = re.compile(pattern)
    search = rgx.search(line.strip())
    if search:
        valve = search.group(1)
        rate = int(search.group(2))
        exits = search.group(3).split(', ')
        return valve, rate, exits

def add_to_graph(graph: Graph, valve, rate, exits):
    graph.add_node(valve, rate)
    graph.add_edges(valve, exits)

def get_score(g: Graph, location, time, max_time):
    score = (max_time - time) * g.get_flow(location)
    return score

def reachable_from(g: Graph, curr, prev):
    return curr in g.edges[prev]

def path_length(path, dists):
    tot = 0
    for a, b in zip(path, path[1:]):
        tot += dists[a][b]
    return tot

def permsize(n, k):
    return math.gamma(n+1) / math.gamma(n - k + 1)

def score_path(path, dists, flows, max_time):
    t = 0
    s = 0
    i = 0
    for i, (a, b) in enumerate(zip(path, path[1:])):
        t += (dists[a][b] + 1)
        if t >= max_time:
            return s, path[:i+2]
        s += (max_time - t) * flows[b]
    return s, path[:i+2]

def brute_force_search(nodes, dists, flows, max_time, path_length):
    best = 0
    best_path = []
    max_iter = permsize(len(nodes), path_length)
    for i, p in enumerate(itertools.permutations(nodes, path_length), start=1):
        path = ['AA'] + list(p)
        score, path = score_path(path, dists, flows, max_time)
        if score > best:
            best = score
            best_path = path
        #if i % 1000000 == 0:
            #print(f'{i} ({100 * i/max_iter})% {best} {len(best_path)}')
    #print(f'{i} ({100 * i/max_iter})% {best} {len(best_path)}')
    return best, best_path

if __name__ == "__main__":
    filename = "input.txt" # 1809 is too low! 1937 is too low!

    with open(filename) as fl:
        g = Graph()
        for line in fl:
            valve, rate, exits = parse_line(line)
            add_to_graph(g, valve, rate, exits)

    dists = {}
    nodes = list(filter(lambda x: g.nodes[x] > 0, g.nodes))
    if not 'AA' in nodes:
        nodes.append('AA')

    nodes.sort()

    for node in nodes:
        dists[node] = {}

    for i in range(len(nodes)-1):
        for j in range(i+1, len(nodes)):
            d = len(bfs_sp(g.edges, nodes[i], nodes[j])) - 1
            dists[nodes[i]][nodes[j]] = d
            dists[nodes[j]][nodes[i]] = d

    nodes.remove('AA')

    part2 = True

    if not part2:
        max_time = 30
        result = brute_force_search(nodes, dists, g.nodes, max_time, min(7, len(nodes)))
        print(f'Part 1: {result[0]}')
    else:
        max_time = 26
    
        # Brute force all the 8-paths. Store the highest scoring
        # result for the path nodes in any order.
        # Then brute force all paths among the remaining nodes.
        # Result is the highest combination of scores from the
        # two enumerations.
        import os, pickle
        if os.path.exists('part2_dict.pickle'):
            with open('part2_dict.pickle', 'rb') as fl:
                d = pickle.load(fl)
        else:
            d = defaultdict(int)
            max_iter = permsize(len(nodes), 8)
            for i, p in enumerate(
                    itertools.permutations(nodes, 8),
                    start = 1):
                path = ['AA'] + list(p)
                score, path = score_path(path, dists, g.nodes, max_time)
                key = frozenset(path)
                if score > d[key]:
                    d[key] = score
                if i % 1000000 == 0:
                    print(f'{i} ({100 * i/max_iter})%')
            print(f'{i} ({100 * i/max_iter})%')

        best2 = 0 # 2762 is too low!
        for i, (k, score1) in enumerate(d.items(), start=1):
            print(f"=={i}/{len(d)}== BEST = {best2}")
            nodes2 = list(set(nodes) - k)
            score2, _ = brute_force_search(nodes2, dists,
                                           g.nodes, max_time,
                                           min(8, len(nodes2)))
            total = score1 + score2
            if total > best2:
                best2 = total
                with open('best.txt', 'w') as fl:
                    fl.write(','.join(sorted(k))+'\n')
                    fl.write(','.join(sorted(nodes2))+'\n')
                    fl.write(f'{total}\n')
        print(f'Part 2: {best2}')

        # Best paths found for part 2:
        # ['AA', 'XC', 'HH', 'FL', 'DW', 'UK', 'OL', 'WV', 'VM'] = 1262
        # ['AA', 'RP', 'SU', 'XD', 'TE', 'YP', 'FQ', 'CS'] = 1513
        # or
        # ['AA', 'XC', 'HH', 'FL', 'DW', 'UK', 'OL', 'WV', 'CS'] = 1262
        # ['AA', 'RP', 'SU', 'XD', 'TE', 'YP', 'FQ', 'VM'] = 1513

