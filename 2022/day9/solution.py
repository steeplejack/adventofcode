def move_head(direction, head):
    assert direction in 'UDLR'
    moves = {'U': (0, 1), 'D': (0, -1),
             'L': (-1, 0), 'R': (1, 0)}
    move = moves[direction]
    return apply_move(head, move)

def subtract(head, tail):
    return tuple(head[i] - tail[i] for i in range(2))

def apply_move(rope_end, move):
    return tuple(rope_end[i] + move[i] for i in range(2))

def follow(head, tail):
    """The tail follows the head. If the head is two steps
    away in a straight line, the tail moves one step along
    the straight line to catch up. If the head is two steps
    away in any diagonal, the tail moves diagonally one step"""

    diff = subtract(head, tail)
    if any(abs(item) > 1 for item in diff):
        move = tuple(int(item / (abs(item) if item != 0 else 1))
                     for item in diff)
        return apply_move(tail, move)
    return tail

def parse_line(line):
    direction, times = line.strip().split()
    return (direction, int(times))

if __name__ == '__main__':
    head = (0, 0)
    tail = (0, 0)
    visited = set([tail])

    with open("input.txt") as fl:
        for line in fl:
            direction, times = parse_line(line)
            for _ in range(times):
                head = move_head(direction, head)
                tail = follow(head, tail)
                visited.add(tail)
    # print(sorted(visited, key = lambda x: (x[1], x[0])))
    print(f'Part 1: {len(visited)}')

    rope = [(0, 0) for _ in range(10)]
    visited = set([rope[-1]])

    with open("input.txt") as fl:
        for line in fl:
            direction, times = parse_line(line)
            for _ in range(times):
                rope[0] = move_head(direction, rope[0])
                for i in range(1, len(rope)):
                    rope[i] = follow(rope[i-1], rope[i])
                visited.add(rope[-1])

    # print(sorted(visited, key = lambda x: (x[1], x[0])))
    print(f'Part 2: {len(visited)}')



