import argparse
import pathlib
import os
import sys

class PathError(Exception):
    pass

def parse_args():
    parser = argparse.ArgumentParser("AoC 2023 Day 9")
    parser.add_argument('input',
        type=lambda p: pathlib.Path(p).absolute(),
        default=pathlib.Path(__file__).absolute().parent / 'input.txt')
    return parser.parse_args()

def diff(s):
    return [s[i] - s[i-1] for i in range(1, len(s))]

def next_value(seq, val = 0):
    if len(seq) == 0:
        return val
    if all([i == 0 for i in seq]):
        return val + seq[-1]
    return next_value(diff(seq), val + seq[-1])

def line_to_sequence(line):
    return [int(x) for x in line.strip().split()]

def part1(infile):
    with open(infile) as fl:
        values = [next_value(line_to_sequence(line)) for line in fl]
    return sum(values)

def main():
    args = parse_args()
    infile = args.input
    if not infile.exists():
        raise PathError(f"Would you believe it, the path {infile} does not exist!")
    part1_result = part1(infile)
    print(f"The answer to part 1 is {part1_result}")

if __name__ == '__main__':
    main()
