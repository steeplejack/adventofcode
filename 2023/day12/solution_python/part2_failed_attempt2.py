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
        count = 0
        for j in reverse_range(start, end):
            if compatible_with(block_size, constraint, j):
                lookup_pos = j + block_size + 1
                lookup_val = table[row-1][lookup_pos]
                count += lookup_val
            table[row][j] = count

    return table

def solve(constraint, blocks):
    table = fill_lookup_table(constraint, blocks, None)
    for j in range(len(table[-1])):
        if table[-1][j] != 0:
            return table[-1][j]