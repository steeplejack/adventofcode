import argparse
import itertools
import pathlib
import queue

def parse_args():
    parser = argparse.ArgumentParser("AoC 2023 Day 12")
    parser.add_argument('infile', type = pathlib.Path)
    return parser.parse_args()

def parse_line(line):
    problem_string, values = line.strip().split()
    values = [int(v) for v in values.split(',')]
    return problem_string, values

def constraints(problem_string, values):
    """
    e.g. vals=[1,2], string_length=6 -> 2 free positions out of 4
        total = string_length - (sum(vals) + len(vals) - 1)
              = 6 - (3 + 2 - 1)
              = 4
        free  = string_length - total
              = (sum(vals) + len(vals) - 1)
    """
    n_constrained_chars = sum(values) + len(values) - 1
    n_free_chars = len(problem_string) - n_constrained_chars
    n_constrained_blocks = constrained = len(values)
    return (n_free_chars, n_free_chars + n_constrained_blocks)

def problem_pieces(values):
    return ['#' * val + '.' for val in values[:-1]] + ['#' * values[-1]]

def findall(string, query='#'):
    assert len(query) == 1
    return [pos for pos, char in enumerate(string) if char == query]

def construct_from_free_positions(pieces, positions):
    l = []
    piece_index = 0
    for i in range(len(pieces) + len(positions)):
        if i in positions:
            l.append('.')
        else:
            try:
                l.append(pieces[piece_index])
            except IndexError as e:
                print(pieces, positions)
                raise e
            piece_index += 1
    return ''.join(l)

def compatible(solution, problem):
    for (s, p) in zip(solution, problem):
        if s == '#' and p == '.':
            return False
        if s == '.' and p == '#':
            return False
    return True

def possibility_generator(problem_string, values):
    n, k = constraints(problem_string, values)
    hash_positions = findall(problem_string, '#')
    dot_positions = findall(problem_string, '.')
    pieces = problem_pieces(values)
    for free_positions in itertools.combinations(range(k), n):
        solution = construct_from_free_positions(pieces, free_positions)
        if compatible(solution, problem_string):
            yield(solution)

def part1(infile):
    solutions = 0
    with open(infile) as fl:
        for line in fl:
            s, v = parse_line(line)
            for _ in possibility_generator(s, v):
                solutions += 1
    print(f'Answer to part 1 = {solutions}')

def main():
    part1(parse_args().infile)

if __name__ == '__main__':
    main()

def quint(s, v):
    nsoln = lambda s, v: len(list(possibility_generator(s, v)))
    single = nsoln(s, v)
    double = nsoln(s + '?' + s, v + v)
    assert double % single == 0
    ratio = int(double) / int(single)
    return single * ratio ** 4

def bitcount(n):
    y = 0
    while n > 0:
        y += n & 1
        n >>= 1
    return y

def firstblockcount(s, char='#'):
    y = 0
    for c in s:
        if c == char:
            y += 1
        else:
            if y > 0:
                return y
    return y

def blockcount(s):
    x = [0]
    i = 0
    for char in s:
        if char == '#':
            x[i] += 1
        else:
            if x[i] > 0:
                i += 1
                x.append(0)
    if x[-1] == 0:
        return x[:-1]
    else:
        return x

def mutate_char(s, pos, char):
    return s[:pos] + char + s[(pos+1):]

def test(s, v):
    q = queue.Queue
    n_unknown = s.count('?')
    unknown_pos = findall(s, '?')
