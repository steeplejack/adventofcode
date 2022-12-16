def parse_input_file(filename):
    with open(filename) as fl:
        rows = fl.read().strip().split('\n')
    grid = [[int(v) for v in row] for row in rows]
    return grid

def get_grid_size(grid):
    nrow = len(trees)
    if nrow == 0:
        raise ValueError('No rows in grid')
    ncol = len(trees[0])
    if ncol == 0:
        raise ValueError('No cols in grid')
    return (nrow, ncol)

def initial_visibilities(grid):
    v = [[False for _ in row] for row in grid]
    nrow, ncol = get_grid_size(grid)

    for col in range(ncol):
        v[0][col] = True
        v[nrow-1][col] = True

    for row in range(nrow):
        v[row][0] = True
        v[row][ncol-1] = True

    return v


def traverse_rows(trees, visibilities, from_right=False):
    nrow, ncol = get_grid_size(trees)
    ix = range(nrow)
    jx = range(ncol)
    if from_right:
        jx = list(reversed(jx))
    
    for i in ix:
        highest_tree = 0
        for j in jx:
            tree_height = trees[i][j]
            if tree_height > highest_tree:
                highest_tree = tree_height
                visibilities[i][j] = True

def traverse_cols(trees, visibilities, from_bottom=False):
    nrow, ncol = get_grid_size(trees)
    ix = range(nrow)
    jx = range(ncol)
    if from_bottom:
        ix = list(reversed(jx))
    
    for j in jx:
        highest_tree = 0
        for i in ix:
            tree_height = trees[i][j]
            if tree_height > highest_tree:
                highest_tree = tree_height
                visibilities[i][j] = True

def count_visible(v):
    return sum([sum(row) for row in v])




def test():
    x = [9, 8, 7, 1, 1, 6, 7, 1, 4, 2, 6, 10]
    subseq_starts = [0]
    subseq_ends = []
    subseq_maxes = []
    m = x[0]
    s = [-1 for _ in x]
    s[0] = 0

    for i in range(1, len(x)):
        if x[i] > m:
            m = x[i]
        if x[i-1] >= x[i]:
            # Start new subsequence
            s[i] = 1
            subseq_ends.append(i)
            subseq_starts.append(i)
            subseq_maxes.append(m)
            m = x[i]

    subseq_ends.append(len(x))
    subseq_maxes.append(m)

    return subseq_starts, subseq_ends, subseq_maxes, s


def get_row(grid, i):
    return grid[i]

def get_col(grid, j):
    nrow, _ = get_grid_size(grid)
    return [grid[i][j] for i in range(nrow)]

# Naive method to compute scenic score for (i,j)
def scenic_score(trees, i, j):
    nrow, ncol = get_grid_size(trees)
    if i==0 or i==(nrow-1) or j==0 or j==(ncol-1):
        return 0

    row = get_row(trees, i)
    col = get_col(trees, j)

    score = 1
    assert row[j] == col[i]
    h = row[j]

    # Looking left
    s = 0
    for k in range(j-1, -1, -1):
        s += 1
        if row[k] >= h:
            break
    score *= s

    # Looking right
    s = 0
    for k in range(j+1, ncol):
        s += 1
        if row[k] >= h:
            break
    score *= s

    # Looking up
    s = 0
    for k in range(i-1, -1, -1):
        s += 1
        if col[k] >= h:
            break
    score *= s

    # Looking down
    s = 0
    for k in range(i+1, ncol):
        s += 1
        if col[k] >= h:
            break
    score *= s
    
    return score

def scenic_scores(trees):
    nrow, ncol = get_grid_size(trees)
    scores = [[0 for _ in range(ncol)] for _ in range(nrow)]
    m = 0
    besti = 0
    bestj = 0
    for i in range(nrow):
        for j in range(ncol):
            s = scenic_score(trees, i, j)
            if s > m:
                m = s
                besti = i
                bestj = j
            scores[i][j] = s
    return scores, (besti, bestj)


if __name__ == '__main__':
    trees = parse_input_file('input.txt')
    visibilities = initial_visibilities(trees)

    # Traverse each row from the left
    traverse_rows(trees, visibilities, False)

    # Traverse each row from the right
    traverse_rows(trees, visibilities, True)

    # Traverse each row from the top
    traverse_cols(trees, visibilities, False)

    # Traverse each row from the bottom
    traverse_cols(trees, visibilities, True)

    total = count_visible(visibilities)
    print(f'Part 1: {total}')

    scores, (i, j) = scenic_scores(trees)
    print(f'Part 2: {scores[i][j]}')
