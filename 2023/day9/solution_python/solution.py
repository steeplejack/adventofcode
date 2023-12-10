import argparse
import pathlib


class PathError(Exception):
    pass


def parse_args():
    parser = argparse.ArgumentParser("AoC 2023 Day 9")
    parser.add_argument('input',
        type=lambda p: pathlib.Path(p).absolute(),
        default=pathlib.Path(__file__).absolute().parent / 'input.txt',
        nargs='?')
    return parser.parse_args()


def diff(s):
    assert len(s) > 1, 'diff requires at least two values in the sequence'
    return [s[i] - s[i-1] for i in range(1, len(s))]


def next_value(seq, acc=0):
    if len(set(seq)) == 1:
        return acc + seq[-1]
    return next_value(diff(seq), acc + seq[-1])


def line_to_sequence(line):
    return [int(x) for x in line.strip().split()]


def reverse(lst):
    lst.reverse()
    return lst


def part1(infile):
    with open(infile) as fl:
        values = [next_value(line_to_sequence(line)) for line in fl]
    return sum(values)


def part2(infile):
    with open(infile) as fl:
        values = [next_value(reverse(line_to_sequence(line))) for line in fl]
    return sum(values)


def main():
    args = parse_args()
    infile = args.input
    if not infile.exists():
        raise PathError(f"Would you believe it, the path {infile} does not exist!")
    part1_result = part1(infile)
    print(f"The answer to part 1 is {part1_result}")
    part2_result = part2(infile)
    print(f"The answer to part 2 is {part2_result}")


if __name__ == '__main__':
    main()
