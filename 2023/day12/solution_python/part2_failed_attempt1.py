import argparse
import itertools
import pathlib
import queue
from collections import deque
from copy import copy

INF = 9223372036854775807

def parse_args():
    parser = argparse.ArgumentParser("AoC 2023 Day 12")
    parser.add_argument('infile', type = pathlib.Path)
    return parser.parse_args()

def parse_line(line):
    problem_string, values = line.strip().split()
    values = [int(v) for v in values.split(',')]
    return problem_string, values

def allowed_positions(size, constraint):
    max_index = len(constraint) - 1
    if len(constraint) < size: return []
    result = []
    for i in range(len(constraint) - size + 1):
        if i > 0 and constraint[i-1] == '#':
            continue
        if all(char in '?#' for char in constraint[i:(i+size)]):
            if i + size > max_index:
                result.append((i, i + size + 1))
            else:
                if constraint[i + size] != '#':
                    result.append((i, i + size + 1))
        if constraint[i] == '#':
            break
    return result

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

def create_lookup_table(constraint, blocks):
    table = []
    for block in blocks:
        table.append([0] * len(constraint))
    return table

def first_last_available_positions(constraint_length, blocks, block_index):
    """
    first index: sum(precpieces) + len(precpieces)
    disallowed at end: sum(nextpieces) + len(nextpieces) + currentpiece - 1
    last index: len(constraint) - disallowed at end
    """
    current_piece = blocks[block_index]
    precpieces = blocks[:block_index]
    nextpieces = blocks[block_index+1:]
    startpos = sum(precpieces) + len(precpieces)
    disallowed_at_end = sum(nextpieces) + len(nextpieces) + current_piece - 1
    endpos = constraint_length - disallowed_at_end
    return (startpos, endpos)

def reverse_range(start, end=None):
    if end is not None:
        return range(end - 1, start - 1, -1)
    else:
        return range(start-1, -1, -1)

def fill_lookup_table(constraint, blocks, table = None):
    if table is None:
        table = create_lookup_table(constraint, blocks)
    
    lc = len(constraint)
    lb = len(blocks)
    # Build the table back to front, top to bottom
    # Start with the first block and the first row
    block_size = blocks[-1]
    row = table[0]
    start, end = first_last_available_positions(lc, blocks, lb - 1)
    count = 0
    for j in reverse_range(start, end):
        if compatible_with(block_size, constraint, j):
            count += 1
            table[0][j] = count

    for block_index in reverse_range(lb - 1):
        row = lb - block_index - 1
        block_size = blocks[block_index]
        start, end = first_last_available_positions(lc, blocks, block_index)
        prev_j_value = 0
        for j in reverse_range(start, end):
            if compatible_with(block_size, constraint, j):
                k = j + block_size + 1
                table[row][j] = table[row-1][k] + prev_j_value
                prev_j_value = table[row][j]

    return table



    # for b in reverse_range(len(blocks)):
    #     table_row = len(blocks) - b - 1
    #     block_size = blocks[b]
    #     count = 0
    #     start, end = first_last_available_positions(len(constraint), blocks, b)
    #     for rpos in range(end - 1, -1, -1):
    #         cmp = compatible_with(block_size, constraint, rpos)
    #         print(f'compatible_with({block_size}, {constraint}, {rpos}) = {cmp}')
    #         if compatible_with(block_size, constraint, rpos) and rpos >= start:
    #             count += 1
    #         if table_row > 0:
    #             if rpos + block_size + 1 < len(constraint):
    #                 if table[table_row-1][rpos + block_size + 1] > 0:
    #                     table[table_row][rpos] = count + table[table_row-1][rpos + block_size + 1]
    #             else:
    #                 table[table_row][rpos] = count
    #         else:
    #             table[table_row][rpos] = count
    # return table

class Problem:
    def __init__(self, constraint, blocks):
        self.constraint = constraint
        self.blocks = blocks

    def current(self, item):
        size = self.blocks[item.block_index]
        remaining_blocks = self.blocks[(item.block_index+1):]
        endoffset = len(self.constraint) - sum(remaining_blocks) + len(remaining_blocks) - 1
        constraint = self.constraint[item.offset:(1+endoffset)]
        return size, constraint


class Item:
    """
    You can have a solution list stored in the item,
    and append to it as the solution is built up,
    but it's not needed for the problem, so I got rid of it
    """
    def __init__(self, offset, block_index):
        self.offset = offset
        self.block_index = block_index

    def __repr__(self):
        return f'Item({self.offset}, {self.block_index})'

def solve(constraint, blocks, repetitions = 1):
    rconstraint = '?'.join([constraint] * repetitions)
    rblocks = blocks * repetitions
    queue = deque()

    nsolutions = 0

    problem = Problem(rconstraint, rblocks)
    item = Item(0, 0)
    queue.append(item)

    it = 0

    while len(queue) > 0:
        it += 1
        if it % 100000 == 0:
            print(f'Iteration:  {it}')
            print(f'Queue size: {len(queue)}', flush=True)
        curr_item = queue.popleft()
        sz, constr = problem.current(curr_item)

        for pos, constr_start in allowed_positions(sz, constr):
            new_offset = curr_item.offset + constr_start
            new_solution = [] # curr_item.solution + [pos + curr_item.offset]
            if curr_item.block_index == len(problem.blocks) - 1:
                # solutions.append(new_solution)
                nsolutions += 1
            else:
                new_item = Item(new_offset, curr_item.block_index + 1)
                queue.append(new_item)

    return nsolutions

def part2(infile):
    s = 0
    with open(infile) as fl:
        for line in fl:
            print(line.strip())
            constraint, blocks = parse_line(line)
            s += solve(constraint, blocks, 5)
    return s

def main():
    args = parse_args()
    answer = part2(args.infile)
    print(f'Answer to part 2 = {answer}')

if __name__ == '__main__':
    main()

