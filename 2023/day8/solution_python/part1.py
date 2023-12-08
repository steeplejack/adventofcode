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


for k, v in tree.items():
    for child in v:
        assert child in tree
assert 'AAA' in tree
assert 'ZZZ' in tree

curr = 'AAA'
success = False
for count, char in enumerate(itertools.cycle(moves), start = 1):
    # print (f'curr = {curr}; count = {count}')
    if char == 'R':
        curr = tree[curr][1]
    elif char == 'L':
        curr = tree[curr][0]
    else:
        raise Exception(f'Something wrong with "moves" string - "{moves}"')
    if curr == 'ZZZ':
        success = True
        break
    if count >= 10000000:
        break

print(f"# steps = {count}")
if not success:
    print("The routine did not end successfully")

