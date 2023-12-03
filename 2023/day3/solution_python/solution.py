#!/usr/bin/env python

import os
import sys
from collections import defaultdict

class Number:
    def __init__(self, value, row, start, end):
        self.value = value
        self.row = row
        self.start = start
        self.end = end
        self.collisions = []

    def __repr__(self):
        return f'Number({self.value},{self.row},{self.start},{self.end},{self.ever_collides})'

    def collides(self, symbol):
        if abs(self.row - symbol.row) > 1:
            return

        if symbol.column < (self.start - 1) or symbol.column > (self.end + 1):
            return

        self.collisions.append(symbol)
        symbol.collisions.append(self)

    @property
    def ever_collides(self):
        return len(self.collisions) > 0
        

class Symbol:
    def __init__(self, value, row, column):
        self.value = value
        self.row = row
        self.column = column
        self.collisions = []

    def __repr__(self):
        return f'Symbol({self.value},{self.row},{self.column})'

def process_infile(filename):
    def _finalise_number(current_number, number_start_col):
        assert number_start_col > -1
        number = Number(int(current_number), row,
                        number_start_col, col - 1)
        current_number = ''
        number_start_col = -1
        return number, current_number, number_start_col

    numbers = defaultdict(list)
    symbols = defaultdict(list)
    with open(filename) as infile:
        for row, line in enumerate(infile):
            current_number = ''
            number_start_col = -1
            for col, char in enumerate(line.strip()):
                if char == '.':
                    if current_number > '':
                        number, current_number, number_start_col = _finalise_number(current_number, number_start_col)
                        numbers[row].append(number)

                elif char.isdigit():
                    if number_start_col == -1:
                        number_start_col = col
                    current_number += char

                else:
                    symbol = Symbol(char, row, col)
                    symbols[row].append(symbol)
                    if current_number > '':
                        number, current_number, number_start_col = _finalise_number(current_number, number_start_col)
                        numbers[row].append(number)

            if current_number > '':
                number, _, _ = _finalise_number(current_number, number_start_col)
                numbers[row].append(number)

    return numbers, symbols

def make_grid(input_filename):
    grid = []
    with open(input_filename) as fl:
        for line in fl:
            line = line.strip()
            chars = list(line)
            grid.append(line)
    return grid

def check_collisions(numbers, symbols):
    maxrow = max(max(numbers), max(symbols))
    for row in symbols:
        for symbol in symbols[row]:
            for rownum in [row-1, row, row+1]:
                if rownum < 0 or rownum > maxrow:
                    continue
                for number in numbers[rownum]:
                    number.collides(symbol)

def get_uncollided_numbers(numbers):
    out = []
    for row in sorted(numbers):
        for number in numbers[row]:
            if number.ever_collides == False:
                out.append(number)
    return out

def get_collided_numbers(numbers):
    out = []
    for row in sorted(numbers):
        for number in numbers[row]:
            if number.ever_collides == True:
                out.append(number)
    return out

def print_grid_context(number, grid):
    area = []
    if number.ever_collides:
        area.append("!COLLIDES!")
    else:
        area.append("!NO_COLLISION!")
    width = number.end - number.start + 3
    maxrow = len(grid)
    maxcol = len(grid[0])

    for r in [number.row - 1, number.row, number.row + 1]:
        l = ''
        for c in range(number.start - 1, number.end + 2):
            if r < 0 or r >= maxrow or c < 0 or c >= maxcol:
                char = ' '
            else:
                char = grid[r][c]
            l += (char)
        area.append(l)
    return('\n'.join(area))

def part1(numbers):
    sum = 0
    for row in numbers:
        for number in numbers[row]:
            if number.ever_collides:
                sum += number.value
    return sum

def part2(symbols):
    sum = 0
    for row in symbols:
        for symbol in symbols[row]:
            prod = 1
            if symbol.value == '*' and len(symbol.collisions) > 1:
                for number in symbol.collisions:
                    prod *= number.value
                sum += prod
    return sum

def main():
    # Too lazy to do checking around whether the file exists, etc.
    input_filename = sys.argv[1]
    numbers, symbols = process_infile(input_filename)
    check_collisions(numbers, symbols)
    
    part1_sum = part1(numbers)
    print(f"Part 1 Sum = {part1_sum}")
    part2_sum = part2(symbols)
    print(f"Part 2 Sum = {part2_sum}")
    print("Done.")


if __name__ == '__main__':
    main()
