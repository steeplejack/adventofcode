from collections import namedtuple
from queue import Queue

Point = namedtuple("Point", "x y z")

def bfs(graph, node: Point):
    explored = set([node])
    q = Queue()
    q.put(node)
    while not q.empty():
        v = q.get()
        for w in graph[v]:
            if not w in explored:
                explored.add(w)
                q.put(w)
    return explored

def bfs2(graph, node: Point, full_cubes: set):
    n = 0
    explored = set([node])
    q = Queue()
    q.put(node)
    while not q.empty():
        v = q.get()
        for w in graph[v]:
            if w in full_cubes:
                n += 1
                continue
            if not w in explored:
                explored.add(w)
                q.put(w)
    return explored, n

def get_neighbours(point: Point) -> set:
    s = set()
    s.add(Point(point.x-1, point.y, point.z))
    s.add(Point(point.x+1, point.y, point.z))
    s.add(Point(point.x, point.y-1, point.z))
    s.add(Point(point.x, point.y+1, point.z))
    s.add(Point(point.x, point.y, point.z-1))
    s.add(Point(point.x, point.y, point.z+1))
    return s


def construct_graph(full_cubes):
    min_x = min(cube.x for cube in full_cubes)
    min_y = min(cube.y for cube in full_cubes)
    min_z = min(cube.z for cube in full_cubes)

    max_x = max(cube.x for cube in full_cubes)
    max_y = max(cube.y for cube in full_cubes)
    max_z = max(cube.z for cube in full_cubes)

    graph = dict()
    for x in range(min_x-1, max_x+2):
        for y in range(min_y-1, max_y+2):
            for z in range(min_z-1, max_z+2):
                cube = Point(x,y,z)
                graph[cube] = []

    for cube in graph:
        neighbours = get_neighbours(cube)
        for neighbour in neighbours:
            if neighbour in graph:
                if cube in full_cubes and neighbour in full_cubes:
                    graph[cube].append(neighbour)
                elif cube not in full_cubes and neighbour not in full_cubes:
                    graph[cube].append(neighbour)
    return graph, Point(min_x, min_y, min_z)


def construct_graph2(full_cubes):
    min_x = min(cube.x for cube in full_cubes)
    min_y = min(cube.y for cube in full_cubes)
    min_z = min(cube.z for cube in full_cubes)

    max_x = max(cube.x for cube in full_cubes)
    max_y = max(cube.y for cube in full_cubes)
    max_z = max(cube.z for cube in full_cubes)

    graph = dict()
    for x in range(min_x-1, max_x+2):
        for y in range(min_y-1, max_y+2):
            for z in range(min_z-1, max_z+2):
                cube = Point(x,y,z)
                graph[cube] = []

    for cube in graph:
        neighbours = get_neighbours(cube)
        for neighbour in neighbours:
            if neighbour in graph:
                graph[cube].append(neighbour)
    return graph, Point(min_x, min_y, min_z)


import time

def make_graph_version1(filename):

    full_cubes = set()
    with open(filename) as fl:
        for line in fl:
            x, y, z = [int(v) for v in line.strip().split(',')]
            cube = Point(x, y, z)
            full_cubes.add(cube)

    graph, init = construct_graph(full_cubes)
    return graph, init, full_cubes

def make_graph_version2(filename):

    full_cubes = set()
    with open(filename) as fl:
        for line in fl:
            x, y, z = [int(v) for v in line.strip().split(',')]
            cube = Point(x, y, z)
            full_cubes.add(cube)

    graph, init = construct_graph2(full_cubes)
    return graph, init, full_cubes

def part2_version1(graph, init, full_cubes):
    start = time.monotonic_ns()

    # Find all connected components:
    seen = set()
    components = []
    for node in graph:
        if node in seen:
            continue
        component = bfs(graph, node)
        components.append(component)
        seen.update(component)

    to_add = set()
    for component in components:
        cmp_is_full = all(cube in full_cubes for cube in component)
        cmp_is_exterior = init in component
        if not cmp_is_full and not cmp_is_exterior:
            # component is air bubble
            to_add.update(component)

    new_full_cubes = set()
    new_full_cubes.update(full_cubes)
    new_full_cubes.update(to_add)

    n = 0
    for cube in new_full_cubes:
        for neighbour in get_neighbours(cube):
            if neighbour not in new_full_cubes:
                n += 1
    print(f'Part 2: {n}')

    end = time.monotonic_ns()
    print(f'{(end-start) / 1000000} ms')


def part2_version2(graph, init, full_cubes):
    start = time.monotonic_ns()

    cc, n = bfs2(graph, init, full_cubes)

    print(f'Part 2: {n}')

    end = time.monotonic_ns()
    print(f'{(end-start) / 1000000} ms')


if __name__ == "__main__":
    filename = "input.txt"
    full_cubes = set()
    with open(filename) as fl:
        for line in fl:
            x, y, z = [int(v) for v in line.strip().split(',')]
            cube = Point(x, y, z)
            full_cubes.add(cube)

    n = 0
    for cube in full_cubes:
        for neighbour in get_neighbours(cube):
            if neighbour not in full_cubes:
                n += 1
    print(f'Part 1: {n}')

    # Build a graph of the filled-in cubes and the surrounding air.
    # Connect air cubes together and filled in cubes together.
    # All exterior air cubes will form one connected component.
    # Filled in cubes will form one or more connected components.
    # Any remaining components are interior air bubbles - can treat these
    # as filled-in cubes.

    # Build the graph:
    graph, init = construct_graph(full_cubes)

    # Find all connected components:
    seen = set()
    components = []
    for node in graph:
        if node in seen:
            continue
        component = bfs(graph, node)
        components.append(component)
        seen.update(component)

    to_add = set()
    for component in components:
        cmp_is_full = all(cube in full_cubes for cube in component)
        cmp_is_exterior = init in component
        if not cmp_is_full and not cmp_is_exterior:
            # component is air bubble
            to_add.update(component)

    new_full_cubes = set()
    new_full_cubes.update(full_cubes)
    new_full_cubes.update(to_add)

    n = 0
    for cube in new_full_cubes:
        for neighbour in get_neighbours(cube):
            if neighbour not in new_full_cubes:
                n += 1
    print(f'Part 2: {n}')

    
    # To solve part 2 it's enough to fully connect the graph,
    # and when finding the exterior connected component, when
    # hitting a filled-in neighbour, not adding it to the search,
    # instead incrementing a counter. In the end this counter
    # will give the number of exposed faces.
    graph, init = construct_graph2(full_cubes)
    cc, n = bfs2(graph, init, full_cubes)

    # Ignoring set up costs, version 2 is about twice as fast
    version_1_inputs = make_graph_version1("input.txt")
    version_2_inputs = make_graph_version2("input.txt")
    part2_version1(*version_1_inputs) # ~ 60ms
    part2_version2(*version_2_inputs) # ~ 30ms

