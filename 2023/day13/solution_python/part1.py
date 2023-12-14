def test_row(pattern, i):
    j = i+1
    if i < 0 or i >= len(pattern) - 1:
        return False
    while i >= 0 and j < len(pattern):
        for (si, sj) in zip(pattern[i], pattern[j]):
            if si != sj:
                return False
        i -= 1
        j += 1
    return True

def transpose(pattern):
    ncol = len(pattern)
    nrow = len(pattern[0])
    p = [[''] * ncol for _ in range(nrow)]
    for i in range(ncol):
        for j in range(nrow):
            p[j][i] = pattern[i][j]
    return [''.join(row) for row in p]

def solve(pattern):
    val = None
    for row in range(len(pattern)):
        if test_row(pattern, row):
            val = 100 * (row + 1)
            break
    if val is None:
        tpattern = transpose(pattern)
        for row in range(len(tpattern)):
            if test_row(tpattern, row):
                val = (row + 1)
                break
    if val is None:
        raise ValueError('?')
    return val    


with open("/Users/kg8/code/aoc/2023/day13/input.txt") as fl:
    pattern_strings = fl.read().split('\n\n')
    patterns = [s.split() for s in pattern_strings]

sm = 0
for pattern in patterns:
    val = solve(pattern)
    sm += val

print(sm)