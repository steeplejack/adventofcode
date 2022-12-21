op_fns = {
        '+': lambda x, y: x + y,
        '-': lambda x, y: x - y,
        '*': lambda x, y: x * y,
        '/': lambda x, y: x / y
        }

class Node():
    def __init__(self, name):
        self.name = name
        self.left = None
        self.right = None
        self.op = None
        self.value = None

def postorder(node):
    if node.left:
        postorder(node.left)
    if node.right:
        postorder(node.right)
    if node.op:
        node.value = node.op(node.left.value, node.right.value)

def parse_line(line):
    s = {}
    name, contents = line.strip().split(': ')
    if contents[-1].isdigit():
        s['value'] = int(contents)
        s['left'] = None
        s['right'] = None
        s['op'] = None
    else:
        left, op, right = contents.split()
        s['left'] = left
        s['right'] = right
        s['op'] = op
        s['value'] = None
    s['name'] = name
    return s

def evaluate(n):
    nodes['humn'].value = n
    postorder(nodes['root'])
    return nodes['root'].value

def binary_search(lower = 0, upper = 10000000000000):
    guess = (upper + lower) // 2
    result = evaluate(guess)
    converged = False
    if result > 0: # too small
        lower = guess
    elif result < 0: # too big
        upper = guess
    else:
        converged = True
    return (lower, upper, converged)

if __name__ == "__main__":
    filename = 'input.txt'

    nodes = {}
    structs = {}
    with open(filename) as fl:
        for line in fl:
            s = parse_line(line)
            structs[s['name']] = s
            node = Node(s['name'])
            if s['op']:
                node.op = op_fns[s['op']]
            if s['value']:
                node.value = s['value']
            nodes[s['name']] = node
    
    for s in structs.values():
        if s['left']:
            assert s['right']
            nodes[s['name']].left = nodes[s['left']]
            nodes[s['name']].right = nodes[s['right']]

    root = nodes['root']
    postorder(root)
    print(f'Part 1: {root.value}')

    # Part 2
    for node in nodes.values():
        if node.left:
            node.value = None
    root.op = op_fns['-']

    lower, upper, converged = binary_search()
    while not converged:
        lower, upper, converged = binary_search(lower, upper)
        guess = (lower + upper) // 2
        result = evaluate(guess)
        print(f'Guess={guess} Bracket={upper-lower} Result={result}')
    print(f'Part 2: {guess}')


        

    
