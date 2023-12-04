import os
import re
import sys

class AoCError(Exception):
    pass

def check_card(line):
    card_no = int(re.search(r'^Card\s+(\d+)', line).group(1))
    line = re.sub(r'^Card\s+\d+:', "", line.strip())
    winners, numbers = line.split(" | ")
    winners = [int(i) for i in winners.strip().split()]
    numbers = [int(i) for i in numbers.strip().split()]
    n_winners = len(set(winners).intersection(numbers))
    return card_no, n_winners


def part1(infile):
    if not os.path.exists(infile):
        raise AoCError(f"File not found: {infile}")
    sum = 0
    with open(infile) as fl:
        for line in fl:
            card_no, n_winners = check_card(line)
            if n_winners > 0:
                score = 2**(n_winners-1)
            else:
                score = 0
            sum += score
    return sum

def part2(infile):
    if not os.path.exists(infile):
        raise AoCError(f"File not found: {infile}")
    sum = 0
    nlines = 0
    with open(infile) as fl:
        for line in fl:
            nlines += 1

    counts = [0 for _ in range(nlines)]

    with open(infile) as fl:
        for i, line in enumerate(fl):
            counts[i] += 1
            _, n_winners = check_card(line)
            for _ in range(counts[i]):
                for k in range(1, n_winners+1):
                    counts[i + k] += 1
    return counts

def main():
    infile = sys.argv[1]

    try:
        part1_sum = part1(infile)
        print(f'Answer to part 1: {part1_sum}')
        counts = part2(infile)
        print(f'Answer to part 2: {sum(counts)}')
    except AoCError as e:
        print(f"Error occurred at line {e.__traceback__.tb_lineno}: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error occurred at line {e.__traceback__.tb_lineno}: {e}", file=sys.stderr)


if __name__ == '__main__':
    main()
