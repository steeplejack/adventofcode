import os
import sys


class ParseError(Exception):
    pass


class Range:
    def __init__(self, output: int, input: int, size: int):
        self._from = input
        self._to = input + size
        self._offset = output - input

    def __repr__(self):
        return f'Range(output={self._offset + self._from}, input={self._from}, size={self._to - self._from})'

    def __call__(self, n: int):
        if self._from <= n < self._to:
            return n + self._offset
        return n


class Map:
    def __init__(self, from_: str, to_: str):
        self._from = from_
        self._to = to_
        self._ranges = []

    def __repr__(self):
        return f'Map(from_={self._from}, to_={self._to})'

    def add_range(self, output: int, input: int, size: int):
        self._ranges.append(Range(output, input, size))

    def __call__(self, n: int):
        for rng in self._ranges:
            output = rng(n)
            if output != n:
                return output
        return n

    def goes_from(self, query: str):
        return self._from == query

    def goes_to(self, query: str):
        return self._to == query


def parse_input_file(filename: str):
    """
    The input file has a structure like this:
        a 'seeds' line "seeds: #1 #2 #3 (...)"
        mapping lines "x-to-y map:"
        numeric lines that belong to the most recently seen map
        blank lines that end seeds and map definitions
    """
    seeds = []
    maps = []
    with open(filename) as fl:
        seeds_line = fl.readline().strip()
        seeds = read_seeds_line(seeds_line)
        fl.readline()

        processing_a_map = False
        map = Map('', '')
        for line in fl:
            line = line.strip()
            if line.endswith('map:'):
                processing_a_map = True
                from_, _, to_ = line.split(' ')[0].split('-')
                map = Map(from_, to_)
            elif line == '':
                assert len(map._ranges) > 0
                maps.append(map)
                processing_a_map = False
                map = Map('', '')
            elif line[0].isdigit():
                params = [int(x) for x in line.split()]
                map.add_range(*params)
                assert len(map._ranges) > 0
            else:
                raise ParseError("What happened?")
        if processing_a_map:
            maps.append(map)

    return seeds, maps


def read_seeds_line(line):
    return [int(x) for x in line.split(':')[1].strip().split()]


def construct_map_from_description(line):
    desc = line.split(' ')[0]
    from_, _, to_ = desc.split('-')
    return Map(from_, to_)

def main():
    filename = sys.argv[1]
    if not os.path.exists(filename):
        print(f"File not found: {filename}")
        return 1
    seeds, maps = parse_input_file(filename)
    for i in range(1, len(maps)):
        assert maps[i-1].goes_to(maps[i]._from)
        assert maps[i].goes_from(maps[i-1]._to)
    assert maps[0].goes_from("seed")
    assert maps[-1].goes_to("location")


    vals = []
    for seed in seeds:
        for map in maps:
            seed = map(seed)
        vals.append(seed)

    print(f'Result = {min(vals)}')
    return 0


if __name__ == '__main__':
    main()
