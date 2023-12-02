import os
import sys

def parse_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str, default='input.txt')
    return parser.parse_args()


# Aho_Corasick algorithm, which I cribbed from something called
# 'prepbytes.com'
class TrieNode:
    def __init__(self):
        self.children = {}
        self.end = False
        self.word = ''
        self.link = None

def build_trie(patterns):
    root = TrieNode()
    for pattern in patterns:
        node = root
        for char in pattern:
            if not char in node.children:
<<<<<<< Updated upstream
                node.children[char] = TrieNode()
=======
                node.children[char] = TrieNode(f'{char},{pattern}')
>>>>>>> Stashed changes
            node = node.children[char]
        node.end = True
        node.word = pattern

    # Build 'failure links'
    queue = []
    for child in root.children.values():
        queue.append(child)
        child.link = root

    while len(queue) > 0:
        node = queue.pop(0)
        for i, child in node.children.items():
            queue.append(child)
            link = node.link

            while link and not link.children.get(i):
                link = link.link

            child.link = link.children.get(i) if link else root
    return root

def search(text, trie):
    root = trie
    node = root
    result = []

<<<<<<< Updated upstream
    for char in text:
=======
    for i, char in enumerate(text):
>>>>>>> Stashed changes
        while node and not node.children.get(char):
            node = node.link

        if not node:
            node = root
            continue
        
        node = node.children.get(char)

        if node.end:
            result.append(node.word)
            
    return result

def decode_match(match):
    if match in '123456789':
        return int(match)
    decoder = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
               'six': 6, 'seven': 7, 'eight': 8, 'nine': 9}
    return decoder[match]

def calculate_result(infile, patterns):
    trie = build_trie(patterns)
    sum = 0
    with open(infile) as fl:
        for line in fl:
            matches = search(line, trie)
            first_match = matches[0]
            last_match = matches[-1]
            value = 10 * decode_match(first_match) + decode_match(last_match)
            print(f'{line.strip()} -> {value}')
            sum += value
    return sum

def part1(infile):
    patterns = list('123456789')
    return calculate_result(infile, patterns)

def part2(infile):
    patterns = ['one', 'two', 'three', 'four', 'five', 'six', 'seven',
                'eight', 'nine', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    return calculate_result(infile, patterns)

def main():
    args = parse_args()
    if not os.path.exists(args.input):
        print(f"File {args.input} not found", file=sys.stderr)
        sys.exit(1)
    result1 = part1(args.input)
    print(f"Part1 sum = {result1}")

    result2 = part2(args.input)
    print(f"Part2 sum = {result2}")

if __name__ == '__main__':
    main()
