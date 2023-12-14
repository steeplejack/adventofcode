def test_row(pattern, i, max_mismatches=0):
    j = i+1
    mismatches = []
    if i < 0 or i >= len(pattern) - 1:
        return (False, mismatches)
    while i >= 0 and j < len(pattern):
        for k in range(len(pattern[i])):
            si = pattern[i][k]
            sj = pattern[j][k]
            if si != sj:
                if pattern[i][k] == '#':
                    mismatches.append((i, k))
                else:
                    mismatches.append((j, k))
            if len(mismatches) > max_mismatches:
                return (False, mismatches)
        i -= 1
        j += 1
    if len(mismatches) == max_mismatches:
        return (True, mismatches)
    return (False, mismatches)

def find_line_of_symmetry(pattern):
    for row in range(len(pattern)):
        success, _ = test_row(pattern, row, 0)
        if success:
            return ('ROW', row)
    tpattern = transpose(pattern)
    for col in range(len(tpattern)):
        success, _ = test_row(tpattern, col, 0)
        if success:
            return ('COL', col)
    return ('FAIL', -1)

def find_all_lines_of_symmetry(pattern):
    lines = []
    for row in range(len(pattern)):
        success, _ = test_row(pattern, row, 0)
        if success:
            lines.append(('ROW', row))
    tpattern = transpose(pattern)
    for col in range(len(tpattern)):
        success, _ = test_row(tpattern, col, 0)
        if success:
            lines.append(('COL', col))
    return lines

def find_smudge(pattern):
    for row in range(len(pattern)):
        success, smudge_position = test_row(pattern, row, 1)
        if success:
            return smudge_position[0]

def clean_smudge(pattern, pos):
    clean = []
    for i, row in enumerate(pattern):
        if i == pos[0]:
            new_row = row[:pos[1]] + '.' + row[pos[1]+1:]
            assert new_row != row
            assert row[pos[1]] == '#' and new_row[pos[1]] == '.'
            clean.append(new_row)
        else:
            clean.append(row)
    assert clean != pattern
    return clean

def transpose(pattern):
    ncol = len(pattern)
    nrow = len(pattern[0])
    p = [[''] * ncol for _ in range(nrow)]
    for i in range(ncol):
        for j in range(nrow):
            p[j][i] = pattern[i][j]
    return [''.join(row) for row in p]

def dim(pattern):
    return len(pattern), len(pattern[0])

with open("/Users/kg8/code/aoc/2023/day13/input.txt") as fl:
    pattern_strings = fl.read().split('\n\n')
    patterns = [s.split() for s in pattern_strings]

sm = 0
for i, pattern in enumerate(patterns):
    tpattern = transpose(pattern)
    assert transpose(tpattern) == pattern
    
    lines_of_symmetry = find_all_lines_of_symmetry(pattern)
    assert len(lines_of_symmetry) == 1
    
    smudge = find_smudge(pattern)
    if smudge is None:
        smudge = find_smudge(tpattern)
        assert smudge is not None
        
        clean = transpose(clean_smudge(tpattern, smudge))
    else:
        clean = clean_smudge(pattern, smudge)
    
    assert dim(clean) == dim(pattern)
    
    clean_lines_of_symmetry = find_all_lines_of_symmetry(clean)
    assert len(clean_lines_of_symmetry) >= 1
    
    for line in clean_lines_of_symmetry:
        if line == lines_of_symmetry[0]:
            continue
        if line[0] == 'ROW':
            sm += 100 * (line[1] + 1)
        else:
            sm += (line[1] + 1)

print(sm)