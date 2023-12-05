import os
import sys
from typing import List


class ParseError(Exception):
    pass

class FinalisedMapError(Exception):
    pass

class RegionError(Exception):
    pass

def create_range(output, input, size):
    return Range(input, input + size, output - input)

class Range:
    def __init__(self, from_: int, to_: int, offset_: int):
        if to_ <= from_:
            raise RegionError(f"End <= Start is not allowed: to_={to_}, from_={from_}")
        self._from = from_
        self._to = to_
        self._offset = offset_

    def __repr__(self):
        return f'Range([{self._from},{self._to}), {self._offset})'

    def __lt__(self, other):
        return (self._from, self._to, self._offset) < (other._from, other._to, other._offset)

    def __eq__(self, other):
        return (self._from, self._to, self._offset) == (other._from, other._to, other._offset)

    def __call__(self, n: int):
        if self._from <= n < self._to:
            return n + self._offset
        return n

    def intersects(self, other):
        return self._from < other._to and self._to > other._from

    def intersection(self, other):
        if self.intersects(other):
            return Range(max(self._from, other._from), min(self._to, other._to), other._offset + self._offset)
    
    def difference(self, other):
        if not self.intersects(other):
            return [self]
        ranges = []
        if self._from < other._from:
            ranges.append(Range(self._from, other._from, self._offset))
        if self._to > other._to:
            ranges.append(Range(other._to, self._to, self._offset))
        return ranges

class Map:
    def __init__(self, from_: str, to_: str):
        self._from = from_
        self._to = to_
        self._ranges = []
        self.__finalised = False

    def __repr__(self):
        return f'Map(from_={self._from}, to_={self._to})'

    def add_range(self, output: int, input: int, size: int):
        if not self.__finalised:
            self._ranges.append(create_range(output, input, size))
        else:
            raise FinalisedMapError("Attempt to modify finalised Map")

    def finalise(self):
        if not self.__finalised:
            sr = sorted(self._ranges)

            if not sr[0]._from == 0:
                sr = [Range(0, sr[0]._from, 0)] + sr

            if not sr[-1]._to == sys.maxsize:
                sr = sr + [Range(sr[-1]._to, sys.maxsize, 0)]

            self._ranges = [sr[0]]
            for i in range(1, len(sr)):
                # Fill any gaps
                if sr[i - 1]._to != sr[i]._from:
                    fill = Range(sr[i-1]._to, sr[i]._from, 0)
                    self._ranges.append(fill)
                self._ranges.append(sr[i])

            self.__finalised = True

    def __call__(self, n: int):
        if not self.__finalised:
            self.finalise()
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
                map.finalise()
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
            map.finalise()
            maps.append(map)

    return seeds, maps


def read_seeds_line(line):
    return [int(x) for x in line.split(':')[1].strip().split()]


def split_range(range_: Range, partition: List[Range], l = None):
    """
    Splits the range_ into disjoint subranges
    by recursively finding its intersection with
    each interval in the partition.
    E.g. Applying split_range to
      range_ = [13, 52),
      intervals = [[0, 25), [25, 50), [50, 60)]
    results in [[13, 25), [25, 50), [50, 52)]
    """
    if l is None:
        l = []
    if len(partition) == 0:
        return [r for r in l if r is not None]
    l.append(range_.intersection(partition[0]))
    diff = range_.difference(partition[0])
    if len(diff) == 0:
        return [r for r in l if r is not None]
    return split_range(diff[-1], partition[1:], l)

def transform_range(r):
    """
    Return a new range by shifting the location of r by r's offset.
    The new range resets its offset to 0
    """
    return Range(r._from + r._offset, r._to + r._offset, 0)

def apply_map_to_range(r: Range, m: Map):
    """
    Returns a sorted list of intervals that result from applying
    the transformations represented by Map m
    1: Split the Range r according to the partition m._ranges
    2: Transform each resulting subrange according to the
    offsets in m._ranges.
    """
    f = split_range(r, m._ranges)
    i = sorted(transform_range(r) for r in f)
    return i

def apply_maps_to_ranges(ranges: List[Range], maps: List[Map]):
    """
    Returns a sorted list of intervals that result from applying
    all the maps to each of the ranges.
    """
    for map in maps:
        tmp = []
        for r in ranges:
            tmp.extend(apply_map_to_range(r, map))
        ranges = tmp
    return ranges

def part1():
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

    print(f'Part 1 Result = {min(vals)}')
    return 0

def part2():
    filename = sys.argv[1]
    if not os.path.exists(filename):
        print(f"File not found: {filename}")
        return 1
    seeds, maps = parse_input_file(filename)

    seed_ranges = [Range(seeds[i], seeds[i] + seeds[i+1], 0)
                   for i in range(0, len(seeds), 2)]

    dists = []
    for seed_range in seed_ranges:
        transformed = apply_maps_to_ranges([seed_range], maps)
        min_dist = min(transformed)._from
        dists.append(min_dist)
    print(f"Part 2 Result = {min(dists)}")
    return 0

def main():
    retval = part1()
    if retval != 0 : return retval
    return part2()

if __name__ == '__main__':
    main()
