import os
import re
import sys

class AoCError(Exception):
    pass


def check_card(line):
    line = re.sub(r'^Card\s+\d+:', "", line.strip())
    winners, numbers = line.split(" | ")
    winners = [int(i) for i in winners.strip().split()]
    numbers = [int(i) for i in numbers.strip().split()]
    n_winners = len(set(winners).intersection(numbers))
    return n_winners


def preprocess_file(infile):
    if not os.path.exists(infile):
        raise AoCError(f"File not found: {infile}")
    with open(infile) as fl:
        return [check_card(line) for line in fl]


def part1(winners):
    sum = 0
    for n_winners in winners:
        if n_winners > 0:
            score = 2**(n_winners-1)
        else:
            score = 0
        sum += score
    return sum


def part2(winners):
    counts = [1 for _ in range(len(winners))]
    for i, n_winners in enumerate(winners):
        for j in range(n_winners):
            counts[i+j+1] += counts[i]
    return sum(counts)

def main():
    infile = sys.argv[1]

    try:
        winners = preprocess_file(infile)
        part1_sum = part1(winners)
        print(f'Answer to part 1: {part1_sum}')
        part2_sum = part2(winners)
        print(f'Answer to part 2: {part2_sum}')
    except AoCError as e:
        print(f"Error occurred at line {e.__traceback__.tb_lineno}: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error occurred at line {e.__traceback__.tb_lineno}: {e}", file=sys.stderr)


if __name__ == '__main__':
    main()
