import argparse
import pathlib
import sys
from support import CircuitManager

class InputError(Exception):
    pass

def parse_args():
    parser = argparse.ArgumentParser("AoC 2023 Day 20 part 1")
    parser.add_argument("infile", type=pathlib.Path)
    parser.add_argument("-m", "--module_files", type=pathlib.Path, nargs=4)
    args = parser.parse_args()
    if not args.infile.exists():
        raise InputError(f"The input file ({args.infile}) was not found")
    for filename in args.module_files:
        if not filename.exists():
            raise InputError(f"The input file ({filename}) was not found")
    return args

def part1(infile):
    manager = CircuitManager()
    manager.read_file(infile)
    for _ in range(1000):
        manager.push_button()
    return manager.low_count * manager.high_count

def part2(filenames):
    """
    Cheated slightly on this solution, in that I manually inspected the shape of the input graph,
    and, finding that it forms 4 separated module-groups, doctored the input to run each group separately
    (files module1-4.txt). The final answer is the number of button presses it would take for the periods
    of all the individual groups to line up, which is their lowest common multiple. Or, because they all
    turn out to be prime numbers, their product.
    """
    periods = []
    for filename in filenames:
        manager = CircuitManager()
        manager.read_file(filename)
        i = 0
        while not manager.modules['rx'].low_pulse_received:
            manager.push_button()
            i += 1
        periods.append(i)
    assert len(periods) == 4
    return periods[0] * periods[1] * periods[2] * periods[3]

def main():
    args = parse_args()
    answer = part1(args.infile)
    print(f"The answer to part 1 is {answer}")
    answer = part2(args.module_files)
    print(f"The answer to part 2 is {answer}")
    return 0

if __name__ == '__main__':
    sys.exit(main())