import os
import sys

def parse_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str, default='input.txt')
    return parser.parse_args()


# Aho_Corasick algorithm
class TrieNode:
    def __init__(self, id = '-1'):
        self.children = {}
        self.end = False
        self.word = ''
        self.link = None
        self.id = id
    def __str__(self):
        link_id = self.link.id if self.link else 'None'
        return f'TrieNode(id=[{self.id}],childkeys={sorted(self.children.keys())},word={self.word},end={self.end},link={link_id})'


def build_trie(patterns):
    root = TrieNode('root')
    for pattern in patterns:
        node = root
        for char in pattern:
            index = ord(char)
            if not index in node.children:
                node.children[index] = TrieNode(f'{char},{pattern}')
            node = node.children[index]
        node.end = True
        node.word = pattern

    build_failure_links(root)
    return root

def print_trie(trie):
    stack = [trie]
    while len(stack) > 0:
        node = stack.pop()
        for child in node.children.values():
            stack.append(child)
        print(node)

def build_failure_links(trie):
    root = trie
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

def search(text, trie):
    root = trie
    node = root
    result = []

    for i, char in enumerate(text):
        index = ord(char)
        while node and not node.children.get(index):
            node = node.link

        if not node:
            node = root
            continue
        
        node = node.children.get(index)

        if node.end:
            result.append((i - len(node.word) + 1, node.word))
            
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
            first_match = min(matches, key=lambda x: x[0])[1]
            last_match = max(matches, key=lambda x: x[0])[1]
            assert first_match == matches[0][1] and last_match == matches[-1][1]
            value = 10 * decode_match(first_match) + decode_match(last_match)
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
