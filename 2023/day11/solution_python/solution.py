import argparse
import pathlib
import sys
def parse_args():
    parser = argparse.ArgumentParser("AoC 2023 Day 11")
    parser.add_argument("infile", type=pathlib.Path)
    parser.add_argument("-e", "--expansion", type=int, default=2)
    return parser.parse_args()

def find_empty_rows(array):
    empties = []
    for i, row in enumerate(array):
        if all(char == '.' for char in row):
            empties.append(i)
    return empties

def find_empty_cols(array):
    empties = []
    nrows = len(array)
    ncols = len(array[0])
    for j in range(ncols):
        if all(array[i][j] == '.' for i in range(nrows)):
            empties.append(j)
    return empties

def find_galaxies(array):
    nrows = len(array)
    ncols = len(array[0])
    return [(i, j) 
            for i in range(nrows) 
            for j in range(ncols)
            if array[i][j] == '#']

def get_expanded_galaxies(galaxies, empty_rows, empty_cols, expansion_units=2):
    """
    Empty rows and columns cause galaxies to appear `expansion_units` times
    further away from each other. A value of 2 means each empty row is replaced
    by two empty rows - it doubles in size (and the same for columns). A value
    of 1000000 makes empty rows 1000000 times bigger.
    """
    return [(i + (expansion_units - 1) * len([r for r in empty_rows if r < i]),
             j + (expansion_units - 1) * len([c for c in empty_cols if c < j])) for i, j in galaxies]
        
def get_distances(galaxies):
    dists = []
    for i in range(len(galaxies)):
        for j in range(i + 1, len(galaxies)):
            gal_i = galaxies[i]
            gal_j = galaxies[j]
            dists.append(abs(gal_i[0] - gal_j[0]) + abs(gal_i[1] - gal_j[1]))
    return dists

def part1(infile):
    with open(infile) as fl:
        array = [list(line.strip()) for line in fl]

    empty_rows = find_empty_rows(array)
    empty_cols = find_empty_cols(array)
    galaxies = find_galaxies(array)
    expanded_galaxies = get_expanded_galaxies(galaxies,
                                              empty_rows,
                                              empty_cols)
    distances = get_distances(expanded_galaxies)

    return sum(distances) 

def part2(infile, unit):
    with open(infile) as fl:
        array = [list(line.strip()) for line in fl]

    empty_rows = find_empty_rows(array)
    empty_cols = find_empty_cols(array)
    galaxies = find_galaxies(array)
    expanded_galaxies = get_expanded_galaxies(galaxies,
                                              empty_rows,
                                              empty_cols,
                                              unit)
    distances = get_distances(expanded_galaxies)

    return sum(distances) 

def main():
    args = parse_args()
    answer1 = part1(args.infile)
    answer2 = part2(args.infile, args.expansion)
    print(f"The answer to part 1 is {answer1}")
    print(f"The answer to part 2 is {answer2}")
    return 0

if __name__ == '__main__':
    sys.exit(main())
