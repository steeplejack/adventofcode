import argparse
import collections
import pathlib
import uuid
from collections import deque
from enum import Enum
from typing import List

"""
Build all the workflows together into a tree. Tip nodes in the tree
are either "R" = reject, or "A" = accept. Each edge of the tree
has a rule that excludes some of the possible inputs. The goal
is to find how many inputs will end up in "accept" nodes.
"""

class InputError(Exception):
    pass

class ParseError(Exception):
    pass

class RegionError(Exception):
    pass

class Range:
    def __init__(self, from_: int, to_: int):
        if to_ <= from_:
            raise RegionError(f"End <= Start is not allowed: to_={to_}, from_={from_}")
        self._from = from_
        self._to = to_

    def __repr__(self):
        return f'Range([{self._from},{self._to}))'

    def __lt__(self, other):
        return (self._from, self._to) < (other._from, other._to)

    def __eq__(self, other):
        return (self._from, self._to) == (other._from, other._to)

    def intersects(self, other):
        return self._from < other._to and self._to > other._from

    def __and__(self, other):
        return self.intersection(other)

    def __sub__(self, other):
        return self.difference(other)

    def intersection(self, other):
        """
        Return a Range covering the interval covered by self and other
        """
        if self.intersects(other):
            return Range(max(self._from, other._from), min(self._to, other._to))
    
    def difference(self, other):
        """
        Return self minus the intersection of self and other
        """
        if not self.intersects(other):
            return [self]
        ranges = []
        if self._from < other._from:
            ranges.append(Range(self._from, other._from))
        if self._to > other._to:
            ranges.append(Range(other._to, self._to,))
        return ranges

    def size(self):
        return self._to - self._from

class RuleType(Enum):
    INTERSECT = 0
    SUBTRACT = 1

class Rule:
    def __init__(self, variable, range_, type_):
        self.variable = variable
        self.range = range_
        self.type = type_

    def __repr__(self):
        return f'Rule({self.variable},{self.range},{self.type})'

    def apply(self, inputs):
        results = []
        if self.type == RuleType.INTERSECT:
            for input_ in inputs:
                result = input_ & self.range
                if result:
                    results.append(result)      
        else:
            for input_ in inputs:
                result = input_ - self.range
                if result:
                    results.append(result)
        return list(flatten(results))

class Node:
    def __init__(self, name):
        self.name = name
        self.rules = []
        self.children = []
        self.parent = None
        self.ranges = {}

    def __repr__(self):
        return f'Node({self.name})'

    def add_child(self, node):
        self.children.append(node)
        node.parent = self

    def add_rule(self, rule):
        self.rules.append(rule)

    def preorder(self):
        yield self
        for child in self.children:
            for node in child.preorder():
                yield node

    def postorder(self):
        for child in self.children:
            for node in child.postorder():
                yield node
        yield self         

def construct_range(s, minval=1, maxval=4000):
    """
    Convert string like a<400 to ('a', Range(minval, 400)),
    or x>400 to ('x', Range(401, maxval+1)).
    minval and maxval are included in the range.
    """
    name = s[0]
    op = s[1]
    try:
        val = int(s[2:])
    except ValueError as e:
        raise ParseError(f"Error converting to an integer - {s} ({e})")
    if op == '<':
        return (name, Range(minval, val))
    elif op == '>':
        return (name, Range(val+1, maxval+1))
    else:
        raise ParseError(f"Unrecognised operator - {s}")


def construct_tree(workflows, minval=1, maxval=4000):
    """
    Iteratively builds a tree from a set of workflow instruction strings.
    """
    tree = {}
    for wf in workflows:
        tree = add_workflow_to_tree(wf, tree, minval, maxval)
    return tree


def add_workflow_to_tree(workflow, tree, minval=1, maxval=4000):
    """
    Adds a workflow instruction string, s, to the current tree
    """
    name = ''
    instructions = ''
    it = iter(workflow)
    char = next(it)
    while char != '{':
        name += char
        char = next(it)

    char = next(it)
    while char != '}':
        instructions += char
        char = next(it)

    if name in tree:
        node = tree[name]
    else:
        node = Node(name)
        tree[name] = node

    subinstructions = instructions.split(',')
    rules = []
    children = []
    for si in subinstructions:
        if ':' in si:
            parts = si.split(':')
            var, rge = construct_range(parts[0], minval, maxval)
            # A rule that accepts items in the range rge
            rule = [Rule(var, rge, RuleType.INTERSECT)]
            # A rule that rejects items in the range rge
            inverted_rule = [Rule(var, rge, RuleType.SUBTRACT)]
            childname = parts[1]
        else:
            childname = si
            rule = []
            inverted_rule = []


        if childname.startswith('A') or childname.startswith('R'):
            childname += '__' + str(uuid.uuid1())
        
        if childname in tree:
            child = tree[childname]
        
        else:
            child = Node(childname)
            tree[childname] = child
        
        child.rules += rule + rules
        rules += inverted_rule # Add the inverted rule to the next child node
        node.add_child(child)

    return tree


def flatten(lst):
    """
    Flatten a list with nested items
    """
    for item in lst:
        if isinstance(item, collections.abc.Iterable):
            for nested_item in flatten(item):
                yield nested_item
        else:
            yield item


def prod(lst: List[int]):
    """
    The product of a list of numbers
    """
    x = 1
    for item in lst:
        x *= item
    return x


def parse_input(infile):
    workflows = []
    with open(infile) as fl:
        for line in fl:
            if line.strip() == '':
                return workflows
            else:
                workflows.append(line.strip())


def parse_args():
    parser = argparse.ArgumentParser("AoC 2023 Day 19")
    parser.add_argument("infile", type=pathlib.Path)
    args = parser.parse_args()
    if not args.infile.exists():
        raise InputError(f"Input file not found: {args.infile}")
    return args


def part2(infile):
    workflows = parse_input(infile)
    tree = construct_tree(workflows, 1, 4000)

    # For each part category (XMAS), pass the range of values
    # down the tree, starting from the root, using each
    # node's rules to eliminate subregions from the range
    for var in 'xmas':
        for node in tree['in'].preorder():
            if node.parent:
                input_range = node.parent.ranges[var]
            else:
                input_range = [Range(1, 4001)]
            for rule in node.rules:
                if rule.variable == var:
                    input_range = rule.apply(input_range)
            node.ranges[var] = input_range

    # The total number of values in each category at any node of the tree
    # is the sum of the sizes allowed subranges
    # The total number of allowed parts is the product over all the categories
    # We're only interested in accepted parts
    answer = 0
    for node in tree['in'].preorder():      
        scores = {}
        for key, lst in node.ranges.items():
            score = 0
            for rg in lst:
                score += rg.size() # Sum the subrange sizes
            scores[key] = score
        node.scores = scores
        if node.name.startswith('A'): # This node represents a set of accepted parts
            answer += prod(scores.values()) # Product over all categories

    return answer


def main():
    args = parse_args()
    answer = part2(args.infile)
    print(f"The answer to part 2 is {answer}")

if __name__ == '__main__':
    main()
