import os
import re
import sys

class AoCError(Exception):
    pass

def part1(infile):
    if not os.path.exists(infile):
        raise AoCError(f"File not found: {infile}")
    sum = 0
    with open(infile) as fl:
        for line in fl:
            card_no = re.search(r'^Card\s+(\d+)', line).group(1)
            line = re.sub(r'^Card\s+\d+:', "", line.strip())
            winners, numbers = line.split(" | ")
            winners = [int(i) for i in winners.strip().split()]
            numbers = [int(i) for i in numbers.strip().split()]
            n_winners = len(set(winners).intersection(numbers))
            if n_winners > 0:
                score = 2**(n_winners-1)
            else:
                score = 0
            print(f'Card {card_no}: score = {score}')
            sum += score
    return sum


def main():
    infile = sys.argv[1]

    try:
        sum = part1(infile)
        print(f'Answer to part 1: {sum}')
    except AoCError as e:
        print(f"Error occurred at line {e.__traceback__.tb_lineno}: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error occurred at line {e.__traceback__.tb_lineno}: {e}", file=sys.stderr)


if __name__ == '__main__':
    main()
