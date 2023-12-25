import argparse
import pathlib
import sys

class InputError(Exception):
    pass

def parse_args():
    parser = argparse.ArgumentParser("AoC 2023 Day 20 part 1")
    parser.add_argument("infile", type=pathlib.Path)
    args = parser.parse_args()
    if not args.infile.exists():
        raise InputError(f"The input file ({args.infile}) was not found")
    return args

def part1(infile):
    return 0

def main():
    args = parse_args()
    answer = part1(args.infile)
    print(f"The answer to part 1 is {answer}")
    return 0

if __name__ == '__main__':
    sys.exit(main())