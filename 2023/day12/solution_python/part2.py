import argparse
import pathlib

INF = 9223372036854775807

def parse_args():
    parser = argparse.ArgumentParser("AoC 2023 Day 12")
    parser.add_argument('infile', type = pathlib.Path)
    return parser.parse_args()

def parse_line(line):
    problem_string, values = line.strip().split()
    values = [int(v) for v in values.split(',')]
    return problem_string, values

def compatible_positions_from_left(size, constraint):
    """
    Assume the piece being fitted is the first one in the constraint
    This means that if it passes the first '#' in the string, no
    more positions are compatible 
    """
    if size == 0:
        return []
    first_x = INF
    positions = []
    for pos in range(len(constraint) - size + 1):
        if constraint[pos] == '#' and pos < first_x:
            first_x = pos
        if pos > first_x:
            return positions
        if compatible_with(size, constraint, pos):
            positions.append(pos)
    return positions

def number_of_solutions(constraint, blocks, cache=None):
    if cache is None:
        cache = {}

    if (constraint, tuple(blocks)) in cache:
        return cache[(constraint, tuple(blocks))]
    
    if len(blocks) == 1:
        accepted = compatible_positions_from_left(blocks[0], constraint)
        rejected = []
        for pos in accepted:

            if '#' in constraint[pos+blocks[0]:]:
                # a left over '#' hasn't been accounted for,
                # so reject this solution
                rejected.append(pos)
    
        solution = len([x for x in accepted if not x in rejected])
        assert solution == len(accepted) - len(rejected)
        cache[(constraint, tuple(blocks))] = solution
        return solution

    n = 0
    for pos in compatible_positions_from_left(blocks[0], constraint):
        n += number_of_solutions(constraint[pos+blocks[0]+1:], blocks[1:], cache)
    cache[(constraint, tuple(blocks))] = n
    return n

def compatible_with(size, constraint, pos):
    """
    ???????? - len = 8
    .....### x pos=5, size=3, pos+size > len
    """
    constraint_length = len(constraint)
    if size + pos > constraint_length:
        return False
    if pos > 0:
        if constraint[pos - 1] == '#':
            return False
    if size + pos < constraint_length - 1:
        if constraint[size+pos] == '#':
            return False
    for i in range(pos, pos+size):
        if constraint[i] == '.':
            return False
    return True

def part2(infile):
    solutions = 0
    with open(infile) as fl:
        for line in fl:
            s, v = parse_line(line)
            solutions += number_of_solutions('?'.join([s] * 5), v * 5)
    print(f'Answer to part 2 = {solutions}')

def main():
    part2(parse_args().infile)

if __name__ == '__main__':
    main()