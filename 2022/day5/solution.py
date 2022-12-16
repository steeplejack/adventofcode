def split_stack_line(line, width = 4):
    marks = list(range(0, len(line), width))
    assert len(marks) == len(line) / width
    items = [line[mark:(mark+width)] for mark in marks]
    return items

def parse_item(item):
    item = item.strip()
    if len(item) == 0:
        return None
    if item[0] == '[' and item[2] == ']':
        return item[1]
    raise ValueError(f"Expected item to be a single digit enclosed in square brackets, not {item}")

def parse_stack_line(line, width = 4):
    return [parse_item(item) for item in split_stack_line(line, width)]

def parse_move(move):
    import re
    rgx = re.compile(r'^move (\d+) from (\d+) to (\d+)$')
    match = rgx.search(move)
    if match:
        return (int(match.group(1)), match.group(2), match.group(3))
    else:
        raise ValueError(f"Expected regex '{rgx.pattern}' to match input '{move}'")

def apply_actions(actions, stacks):
    for _ in range(actions[0]):
        item = stacks[actions[1]].pop()
        stacks[actions[2]].append(item)

def apply_actions_part2(actions, stacks):
    in_motion = [stacks[actions[1]].pop() for _ in range(actions[0])]
    for _ in range(actions[0]):
        stacks[actions[2]].append(in_motion.pop())


if __name__ == '__main__':
    with open("input.txt") as fl:
        inputs = fl.readlines()

    # Split input into header and footer - header describes
    # the setup, footer describes the operations
    split_pos = 0
    for split_pos, line in enumerate(inputs):
        if line.strip() == '':
            break

    header = inputs[:split_pos]
    footer = inputs[(split_pos + 1):]

    # Check all entries in the header are the same size
    assert len(set(len(entry) for entry in header)) == 1

    stack_names = header.pop().strip().split()
    stacks = {name: list() for name in stack_names}

    # Read stacks from bottom to top, adding to stack dict on the way
    for i in range(len(header)-1, -1, -1):
        items = parse_stack_line(header[i])
        for (key, item) in zip(stack_names, items):
            if item is not None:
                stacks[key].append(item)

    import copy
    original_stacks = copy.deepcopy(stacks)

    # PART 1
    for move in footer:
        actions = parse_move(move)
        apply_actions(actions, stacks)

    print('PART 1')
    print(''.join([stacks[name][-1] for name in stack_names]))

    # Restore initial state
    stacks = copy.deepcopy(original_stacks)
    
    # PART 2
    for move in footer:
        actions = parse_move(move)
        apply_actions_part2(actions, stacks)

    print('PART 2')
    print(''.join([stacks[name][-1] for name in stack_names]))

