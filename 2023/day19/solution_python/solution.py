import argparse
import pathlib

class InputError(Exception):
    pass

class Part:
    def __init__(self, x, m, a, s):
        self.x = x
        self.m = m
        self.a = a
        self.s = s

    def __repr__(self):
        return f'Part({self.x},{self.m},{self.a},{self.s})'

    def sum(self):
        return self.x + self.m + self.a + self.s

class Workflow:
    def __init__(self, name, instructions):
        self.name = name
        self.instructions = instructions
        functions = []
        cases = instructions.split(',')
        for case in cases[:-1]:
            field = case[0]
            operator = case[1]
            threshold, output = case[2:].split(':')
            functions.append(make_function(output, field, operator, threshold))
        functions.append(make_function(cases[-1]))
        self.functions = functions

    def __repr__(self):
        return f'Workflow({self.name},{self.instructions})'

    def __call__(self, part):
        for function in self.functions:
            output = function(part)
            if output is not None:
                return output

def parse_args():
    parser = argparse.ArgumentParser("AoC 2023 Day 19")
    parser.add_argument("infile", type=pathlib.Path)
    args = parser.parse_args()
    if not args.infile.exists():
        raise InputError(f"Input file not found: {args.infile}")
    return args

def parse_input(infile):
    workflows = []
    parts = []

    collect_parts = False
    with open(infile) as fl:
        for line in fl:
            if line.strip() == '':
                collect_parts = True
                continue
            if collect_parts:
                parts.append(construct_part(line.strip()))
            else:
                workflows.append(construct_workflow(line.strip()))

    workflows_dict = {}
    for workflow in workflows:
        workflows_dict[workflow.name] = workflow
    return workflows_dict, parts

def construct_workflow(s):
    name = ''
    instructions = ''
    it = iter(s)
    char = next(it)
    while char != '{':
        name += char
        char = next(it)

    char = next(it)
    while char != '}':
        instructions += char
        char = next(it)

    return Workflow(name, instructions)

def construct_part(s):
    args_dict = {}
    args = s.lstrip('{').rstrip('}').split(',')
    for arg in args:
        k, v = arg.split('=')
        args_dict[k] = int(v)
    return Part(**args_dict)

def make_function(output, field=None, operator=None, threshold=None):
    def fn(part):
        if field is None or operator is None or threshold is None:
            return output
        if operator == '<':
            if part.__getattribute__(field) < int(threshold):
                return output
        elif operator == '>':
            if part.__getattribute__(field) > int(threshold):
                return output
        else:
            return None
    return fn

def run_workflow(part, workflows_dict):
    key = 'in'
    while key not in 'RA':
        key = workflows_dict[key](part)
    return key

def part1(infile):
    total = 0
    workflows, parts = parse_input(infile)
    for part in parts:
        if run_workflow(part, workflows) == 'A':
            total += part.sum()
    return total

def main():
    args = parse_args()
    answer = part1(args.infile)
    print(f"The answer to part 1 is {answer}")
    return 0

if __name__ == '__main__':
    main()