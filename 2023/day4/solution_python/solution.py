import sys

def check_card(line):
    winners, numbers = line.split(':')[1].split('|')
    winners = winners.strip().split()
    numbers = numbers.strip().split()
    n_winners = len(set(winners).intersection(numbers))
    return n_winners

def preprocess_file(infile):
    with open(infile) as fl:
        return [check_card(line) for line in fl]

def both_parts(winners):
    counts = [1 for _ in range(len(winners))]
    sm = 0
    for i, n_winners in enumerate(winners):
        for j in range(n_winners):
            counts[i+j+1] += counts[i]
        sm += 1 << max(0, n_winners - 1)
    return sm, sum(counts)

winners = preprocess_file(sys.argv[1])
part1_sum, part2_sum = both_parts(winners)
print(f'Answer to part 1: {part1_sum}')
print(f'Answer to part 2: {part2_sum}')

