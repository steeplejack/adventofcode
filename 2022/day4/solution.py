def parse_line(line):
    """
    Lines in input have the form "A-B,C-D", e.g. "12-15,33-60"
    Convert to a list of four integers
    """
    ab, cd = line.strip().split(',')
    a, b = ab.split('-')
    c, d = cd.split('-')
    return [int(x) for x in (a, b, c, d)]


def fully_contains(a, b, c, d):
    """
    True if the range a-b fully contains c-d
    """
    assert c <= d and a <= b
    return c >= a and d <= b


def overlaps(a, b, c, d):
    assert a <= b and c <= d
    return b >= c and a <= d

if __name__ == '__main__':
    with open("input.txt") as fl:
        inputs = [line.strip() for line in fl.readlines()]

    fc = 0
    ov = 0
    for i in inputs:
        a, b, c, d = parse_line(i)
        fc += (fully_contains(a, b, c, d) or fully_contains(c, d, a, b))
        ov += overlaps(a, b, c, d)
    print(f"Fully contained = {fc}\nOverlapping = {ov}")




