import argparse
import pathlib
from collections import namedtuple


Operation = namedtuple("Operation", "key box op focal_length")


class HashMapItem:
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __repr__(self):
        return f'<{self.key}, {self.value}>'

    def __eq__(self, other):
        return self.key == other.key


class AoCInputError(Exception):
    pass


def parse_args():
    parser = argparse.ArgumentParser("AoC 2023 Day 15")
    parser.add_argument("infile", type=pathlib.Path)
    return parser.parse_args()


def parse_file(infile):
    with open(infile) as fl:
        return fl.read().strip().split(',')


def parse_op(s):
    if '=' in s:
        key, op, fl = s.partition('=')
        return Operation(key, hash_chars(key), op, int(fl))
    else:
        key = s.partition('-')[0]
        return Operation(key, hash_chars(key), '-', None)


def hash_chars(chars):
    value = 0
    for char in chars:
        value += ord(char)
        value *= 17
        value %= 256
    return value


def part1(infile):
    strings = parse_file(infile)
    return sum(hash_chars(chars) for chars in strings)


def part2(infile):
    strings = parse_file(infile)

    # `boxes` is a simple hash map
    boxes = [list() for _ in range(256)]
    
    # Construct the hash map from the inputs
    for string in strings:
        op = parse_op(string)
        box = boxes[op.box]
        if op.op == '=': # add/overwrite the item with the key
            found = False
            for item in box:
                if item.key == op.key:
                    item.value = op.focal_length
                    found = True
                    break
            if not found:
                box.append(HashMapItem(op.key, op.focal_length))

        else: # delete the item with the key, if it exists
            item = HashMapItem(op.key, op.focal_length)
            if item in box:
                box.remove(HashMapItem(op.key, None))

    # Compute the required sum
    total = 0
    for box_num, box in enumerate(boxes, start = 1):
        for slot_num, item in enumerate(box, start = 1):
            total += box_num * slot_num * item.value
    return total


def main():
    args = parse_args()
    if not args.infile.exists():
        raise AoCInputError(f"The file {args.infile} does not exist")
    result = part1(args.infile)
    print(f'Answer to part 1 = {result}')

    result = part2(args.infile)
    print(f'Answer to part 2 = {result}')
    return 0

if __name__ == '__main__':
    main()
