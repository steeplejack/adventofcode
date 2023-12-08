import itertools
import sys

tree = {}

with open(sys.argv[1]) as fl:
    moves = fl.readline().strip()
    fl.readline()

    for line in fl:
        try:
            node, children = [s.strip() for s in line.split('=')]
            children = [s.strip() for s in children.strip('()').split(',')]
        except Exception as e:
            print(f'Error occurred reading line "{line}"')
            print(f'Error was {e}')
        tree[node] = children


ends_a = 0
ends_z = 0
for k, v in tree.items():
    for child in v:
        assert child in tree
    if k.endswith('A'):
        ends_a += 1
    if k.endswith('Z'):
        ends_z += 1


assert ends_a == ends_z
assert ends_a > 0

a_nodes = [k for k in tree if k.endswith('A')]
# solve for each individually
solutions = []
for a_node in a_nodes:
    curr = [a_node]
    success = False
    for count, char in enumerate(itertools.cycle(moves), start = 1):
        # print (f'curr = {curr}; count = {count}')
        if char == 'R':
            curr = [tree[c][1] for c in curr]
        elif char == 'L':
            curr = [tree[c][0] for c in curr]
        else:
            raise Exception(f'Something wrong with "moves" string - "{moves}"')
        if all(c.endswith('Z') for c in curr):
            success = True
            solutions.append(count)
            break
        if count >= 100000:
            break

# result is lcm of the individual results
def gcd(a, b):
    if a % b == 0:
        return b
    return gcd(b, a % b)

def lcm(a, b):
    return a * b // gcd(a, b)
import functools

answer = functools.reduce(lcm, solutions)

print(f"# steps = {answer}")
if not success:
    print("The routine did not end successfully")

