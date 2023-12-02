import sys

class Pattern:
    def __init__(self, pattern, value):
        self.pattern = pattern
        self.value = value

patterns = [
    Pattern("one", 1),
    Pattern("two", 2),
    Pattern("three", 3),
    Pattern("four", 4),
    Pattern("five", 5),
    Pattern("six", 6),
    Pattern("seven", 7),
    Pattern("eight", 8),
    Pattern("nine", 9),
    Pattern("1", 1),
    Pattern("2", 2),
    Pattern("3", 3),
    Pattern("4", 4),
    Pattern("5", 5),
    Pattern("6", 6),
    Pattern("7", 7),
    Pattern("8", 8),
    Pattern("9", 9)
]

def search(s):
    first = (None, 99999999)
    second = (None, -99999999)
    for p in patterns:
        index_l = s.find(p.pattern)
        index_r = s.rfind(p.pattern)
        if index_l != -1:
            if index_l < first[1]:
                first = (p.value, index_l)
            if index_r > second[1]:
                second = (p.value, index_r)
    return 10 * first[0] + second[0]


sum = 0
with open(sys.argv[1]) as fl:
    for line in fl:
        val = search(line)
        sum += val

print(sum)
