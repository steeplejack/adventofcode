from itertools import zip_longest
import sys
from functools import cmp_to_key

class ParseError(Exception):
    pass

def parse(s: str) -> list:
    """Parses the written form of a possibly nested list of
    positive integers. Can use `eval` or `ast.literal_eval`
    or `json.reads`, but why not write my own?"""
    assert s.count('[') == s.count(']')
    stack: list = []
    root: list | None = None
    current: list = []
    collecting: bool = False
    number: list = []

    for char in s:
        if char == '[':
            if root is None:
                stack.append(current)
                root = current
            else:
                current.append([])
                current = current[-1]
                stack.append(current)
        elif char == ']':
            if collecting:
                current.append(int(''.join(number)))
                number = []
            collecting = False
            stack.pop()
            if len(stack) > 0:
                current = stack[-1]
            else:
                break
        elif char.isdigit():
            number.append(char)
            collecting = True
        elif char == ',':
            if collecting:
                current.append(int(''.join(number)))
                number = []
            collecting = False
        elif char.isspace():
            continue
        else:
            raise ParseError(f"Unrecognised character, {char}")

    return root


LT, EQ, GT = '<', '=', '>'

# Note: Python 3.10 got match expressions,
# which would have made the cmp function
# easier to write.

def cmp(l, r):
    # print(f'\n***\nComparing l="{l}" to r="{r}"')
    
    # using NEGINF=-sys.maxsize as a fill value caused a bug:
    # the list that runs out of values first should compare as
    # LT, but using an integer value meant that the "run-out"
    # vs empty list comparison returned GT, so [[],[]] > [[],[],[],[]]
    assert not (l is None and r is None)
    if l is None:
        yield LT
        return
    elif r is None:
        yield GT
        return
    intl = isinstance(l, int)
    intr = isinstance(r, int)
    # print(f'intl="{intl}" intr="{intr}"')
    if intl and intr:
        result = None
        if l < r:
            # print('  (LT)')
            result = LT
        elif l == r:
            # print('  (EQ)')
            result = EQ
        else:
            result = GT
            # print('  (GT)')
        # print(f'  Both are ints: returning "{result}"')
        yield result
        return

    # This was the final piece to solve for part 1
    # - check if both lists are empty -
    # but there was still more to fix
    if not intr and not intl:
        if len(l) == 0 and len(r) == 0:
            yield EQ
            return

    if not intr:
        if len(r) == 0:
            # print(f'r is empty list ({r}): returning "{GT}"')
            yield GT
            return
        if intl:
            # print("Converting l to [l]")
            l = [l]

    if not intl:
        if len(l) == 0:
            # print(f'l is empty list ({l}): returning "{LT}"')
            yield LT
            return
        if intr:
            # print("Converting r to [r]")
            r = [r]

    # print(f"Making sequence of comparisons: {list(zip_longest(l,r))}")
    for (ll, rr) in zip_longest(l, r):
        for result in cmp(ll, rr):
            yield result

def in_order(packet_pairs):
    l, r = packet_pairs
    for result in cmp(l, r):
        if result == LT:
            return True
        if result == GT:
            return False
    raise ValueError("No decision reached")

def sortfn(l, r):
    return -1 if in_order((l, r)) else 1

if __name__ == '__main__':
    with open("input.txt") as fl:
        x = fl.read().strip().split('\n\n')

    # TESTS
    # Very defensive coding because I got part 1 wrong 4 times
    # and part 2 wrong once.
    assert in_order(([1,1,3,1,1], [1,1,5,1,1]))
    assert not in_order(([1,1,5,1,1], [1,1,3,1,1]))
    assert in_order(([[1],[2,3,4]], [[1],4]))
    assert not in_order(([[1],4], [[1], [2,3,4]]))
    assert not in_order(([9], [[8,7,6]]))
    assert in_order(([[8,7,6]], [9]))
    assert in_order(([[4,4],4,4], [[4,4],4,4,4]))
    assert not in_order(([[4,4],4,4,4], [[4,4],4,4]))
    assert not in_order(([7,7,7,7], [7,7,7]))
    assert in_order(([7,7,7], [7,7,7,7]))
    assert in_order(([], [3]))
    assert not in_order(([3], []))
    assert not in_order(([[[]]], [[]]))
    assert in_order(([[]], [[[]]]))
    assert not in_order(([1,[2,[3,[4,[5,6,7]]]],8,9], [1,[2,[3,[4,[5,6,0]]]],8,9]))
    assert in_order(([1,[2,[3,[4,[5,6,0]]]],8,9], [1,[2,[3,[4,[5,6,7]]]],8,9]))

    packet_pairs = [tuple(parse(f) for f in y.split()) for y in x]
    packets = [[[2]],[[6]]]
    s = 0
    for (i, (l, r)) in enumerate(packet_pairs, start=1):
        packets.append(l)
        packets.append(r)
        if l == r:
            raise ValueError("Wasn't expecting identical packets")
        result = in_order((l, r))
        assert result == (not in_order((r, l)))

        if in_order((l, r)):
            s += i
    print(f'Part 1: {s}')

    packets.sort(key=cmp_to_key(sortfn))

    for i in range(0, len(packets) - 1):
        for j in range(i+1, len(packets)):
            assert in_order((packets[i], packets[j]))
            assert not in_order((packets[j], packets[i]))

    decoder = (packets.index([[2]]) + 1) * (packets.index([[6]]) + 1)
    print(f'Part 2: {decoder}')

