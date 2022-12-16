import sys
from collections import namedtuple
from enum import Enum

Point = namedtuple("Point", "x y")
Pair = namedtuple("Pair", "start end")
Bounds = namedtuple("Bounds", "xmin xmax ymin ymax")
SandStatus = Enum("SandStatus", ["Settled", "Blocked", "FellForever", "NotStarted"])

class Board():
    def __init__(self, bounds: Bounds):
        self.source = None
        self.bounds = bounds
        width = bounds.xmax - bounds.xmin + 1
        height = bounds.ymax - bounds.ymin + 1
        # empty board
        self.board = [['.'] * width for _ in range(height)]

    def index(self, point: Point):
        """
        Convert user space coordinate to internal coordinate
        """
        return Point(point.x - self.bounds.xmin,
                     point.y - self.bounds.ymin)

    def add_source(self, source: Point):
        i = self.index(source)
        self.source = i
        self.set(i, '+')

    def draw_rocks(self, pairs: list[Pair]):
        for pair in pairs:
            if pair.start.y == pair.end.y:
                y = pair.start.y
                for x in range(pair.start.x, pair.end.x + 1):
                    i = self.index(Point(x, y))
                    self.set(i, '#')
            else:
                x = pair.start.x
                for y in range(pair.start.y, pair.end.y + 1):
                    i = self.index(Point(x, y))
                    self.set(i, '#')

    def get(self, point: Point):
        """
        Gets the grid square at point 'point'
        'point' must be in the internal coordinate system
        """
        return self.board[point.y][point.x]

    def set(self, point: Point, val: str):
        self.board[point.y][point.x] = val

    def add_sand(self):
        assert self.source
        entry_point = self.source
        if self.get(entry_point) == 'o':
            return SandStatus.Blocked
        if self.get(entry_point) == '#':
            raise ValueError("Source is blocked by rock")

        s = entry_point
        while True:
            next = Point(s.x, s.y+1)
            if next.y > self.bounds.ymax:
                return SandStatus.FellForever
            if self.get(next) in '#o':
                diag = Point(next.x-1, next.y)
                if self.get(diag) == '.':
                    s = diag
                    continue
                else:
                    diag = Point(next.x+1, next.y)
                    if self.get(diag) == '.':
                        s = diag
                        continue
                    else:
                        self.set(s, 'o')
                        return SandStatus.Settled
            else:
                s = next


    def render(self):
        import numpy as np
        rows = self.bounds.ymax - self.bounds.ymin + 1
        columns = self.bounds.xmax - self.bounds.xmin + 1
        colours = 3
        frame = np.zeros((colours, rows, columns))
        for row in range(rows):
            for col in range(columns):
                val = self.get(Point(col, row))
                if val == 'o':
                    frame[0, row, col] = 200
                    frame[1, row, col] = 200
                elif val == '#':
                    frame[0, row, col] = 100
                    frame[1, row, col] = 60
                    frame[2, row, col] = 160
                elif val == '+':
                    frame[0, row, col] = 128
                    frame[1, row, col] = 128
                    frame[2, row, col] = 128
        return frame


    def __str__(self):
        return '\n'.join(''.join(row) for row in self.board)

def check_pair(pair):
    return pair.start.x == pair.end.x or pair.start.y == pair.end.y

def sort_pair(pair):
    if pair.start.x > pair.end.x or pair.start.y > pair.end.y:
        return Pair(pair.end, pair.start)
    return pair

def parse_input(filename):
    """
    Extracts a sequence of start->end coordinate pairs
    from an input file
    """
    seq = []
    with open(filename) as fl:
        for line in fl:
            coords = line.strip().split(' -> ')
            for start, end in zip(coords, coords[1::]):
                start = Point(*(int(val) for val in start.split(',')))
                end = Point(*(int(val) for val in end.split(',')))
                pair = Pair(start, end)
                assert check_pair(pair)
                seq.append(sort_pair(pair))
    return seq

def pairs_to_points(pairs):
    points = []
    for pair in pairs:
        points.append(pair.start)
        points.append(pair.end)
    return points

def get_bounds(points):
    xs = []
    ys = []
    for point in points:
        xs.append(point.x)
        ys.append(point.y)
    return Bounds(min(xs), max(xs), min(ys), max(ys))

def construct_board(pairs, source):
    points = pairs_to_points(pairs) + [source]
    bounds = get_bounds(points)
    width = bounds.xmax - bounds.xmin + 1
    height = bounds.ymax - bounds.ymin + 1

    # initial board
    board = Board(bounds)
    board.add_source(source)
    board.draw_rocks(pairs)
    return board

def part1():
    source = Point(500, 0)
    pairs = parse_input("input.txt")
    points = pairs_to_points(pairs)
    bounds = get_bounds(points)
    board = construct_board(pairs, source)
    sand_status = SandStatus.NotStarted
    n = 0
    while sand_status not in [SandStatus.FellForever, SandStatus.Blocked]:
        sand_status = board.add_sand()
        if sand_status == SandStatus.Settled:
            n += 1
        print(f'{board}\n')
    print(f'Part 1: {n}')


def part2():
    source = Point(500, 0)
    pairs = parse_input("input.txt")
    points = pairs_to_points(pairs)
    bounds = get_bounds(points)
    
    # Add a floor
    pairs.append(Pair(
        Point(bounds.xmin - 125, bounds.ymax + 2),
        Point(bounds.xmax + 150, bounds.ymax + 2)
    ))

    board = construct_board(pairs, source)
    sand_status = SandStatus.NotStarted
    n = 0
    while sand_status not in [SandStatus.FellForever, SandStatus.Blocked]:
        sand_status = board.add_sand()
        if sand_status == SandStatus.Settled:
            n += 1
        #print(f'{board}\n')
    if sand_status == SandStatus.FellForever:
        raise ValueError("not wide enough!")
    if n < 24943:
        raise ValueError("not wide enough!2")
    print(f'Part 2: {n}')

if __name__ == '__main__':

    #part1()
    #part2()

    import array2gif
    pairs = parse_input("input.txt")
    points = pairs_to_points(pairs)
    bounds = get_bounds(points)
    pairs.append(Pair(
        Point(bounds.xmin - 125, bounds.ymax + 2),
        Point(bounds.xmax + 150, bounds.ymax + 2)
    ))
    source = Point(500, 0)
    board = construct_board(pairs, source)
    frames = []
    for f in range(24960):
        if (f+1) % 25 == 0:
            print(f+1)
        board.add_sand()
        frames.append(board.render())
    from PIL import Image
    imgs = [Image.fromarray(frame.transpose(1,2,0).astype(np.uint8))
            for frame in frames]
    imgs[0].save("array.gif", save_all=True, append_images=imgs[1:], duration=10, loop=0)
    # array2gif.write_gif(frames, "input.gif", fps = 60)
