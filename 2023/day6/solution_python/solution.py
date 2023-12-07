import sys
from collections import namedtuple

race = namedtuple("Race", ["time", "distance"])


def parse_input(infile, correct_the_kerning=False):
    with open(infile) as fl:
        if correct_the_kerning:
            times = fl.readline().strip().split(':')[1].replace(' ', '')
            times = [int(times)]
        else:
            times = fl.readline().strip().split(':')[1].strip().split()
            times = [int(t) for t in times]
        if correct_the_kerning:
            distances = fl.readline().strip().split(':')[1].replace(' ', '')
            distances = [int(distances)]
        else:
            distances = fl.readline().strip().split(':')[1].strip().split()
            distances = [int(d) for d in distances]
    return [race(t, d) for (t, d) in zip(times, distances)]


def outcomes(time):
    return [t * (time - t) for t in range(time + 1)]


def part1():
    infile = sys.argv[1]
    races = parse_input(infile)
    print(races)
    final_wins = []
    for i, race in enumerate(races, start = 1):
        print(f'Race {i}={race}')
        wins = 0
        results = outcomes(race.time)
        for outcome in results:
            hist = '*'*(int(outcome / max(results) * 80))
            if outcome > race.distance:
                print(f'* W = {outcome:<5} {hist}')
                wins += 1 
            else:
                print(f'  L = {outcome:<5} {hist}')
        print(f'{wins} ways to win\n\n')
        final_wins.append(wins)
    prod = 1
    for w in final_wins:
        prod *= w
    print(f"The answer to part 1 is {prod}\n\n")


def newton(guess, T, d):
    t = guess
    for _ in range(1000):
        y = T*t - t*t - d
        dy = T - 2*t
        t = t - y/dy
        if abs(y) < 1e-6:
            break
    return t


def have_a_guess(time):
    return time / 2 - 1


def get_distance(t, total_time):
    return t * (total_time - t)


def find_the_solutions(time, distance):
    guess = have_a_guess(time)
    solution = int(newton(guess, time, distance))
    y = get_distance(solution, time) - distance
    if y <= 0:
        solution += 1
    assert get_distance(solution, time) - distance > 0
    other_solution = time - solution
    return (min(solution, other_solution),
            max(solution, other_solution))


def part2():
    infile = sys.argv[1]
    races = parse_input(infile, correct_the_kerning=True)
    final_wins = []
    for i, race in enumerate(races, start = 1):
        print(f'Race {i}={race}')
        lower, upper = find_the_solutions(race.time, race.distance)
        number_of_ways_to_win = upper - lower + 1
        final_wins.append(number_of_ways_to_win)
        assert upper-lower+1 == race.time - 2*lower + 1
        print (f'  Solutions are {(lower,upper)}. There are {number_of_ways_to_win} ways to win')
    prod = 1
    for w in final_wins:
        prod *= w
    print(f"\n\nThe answer to part 2 is {prod}")
    pass


def main():
    part1()
    part2()


if __name__ == '__main__':
    sys.exit(main())

