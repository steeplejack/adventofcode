import argparse
import pathlib

class AoCInputError(Exception):
    pass

def parse_args():
    parser = argparse.ArgumentParser("AoC 2023 Day 15")
    parser.add_argument("infile", type=pathlib.Path)
    return parser.parse_args()

def parse_file(infile):
    with open(infile) as fl:
        return fl.read().strip().split(',')

def hash_chars(chars):
    value = 0
    for char in chars:
        value += ord(char)
        value *= 17
        value %= 256
    return value

def part1(infile):
    strings = parse_file(infile)
    return sum(hash_chars(chars) for chars in strings)

def main():
    args = parse_args()
    if not args.infile.exists():
        raise AoCInputError(f"The file {args.infile} does not exist")
    result = part1(args.infile)
    print(f'Answer to part 1 = {result}')
    return 0

if __name__ == '__main__':
    main()
