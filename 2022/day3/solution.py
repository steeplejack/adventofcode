def split_compartments(text):
    l = len(text.strip())
    assert l % 2 == 0
    return (text[:l//2], text[l//2:])

# def find_common_item(compartment1, compartment2):
#     isct = set(compartment1).intersection(compartment2)
#     if isct:
#         return isct.pop()
#     else:
#         return ''

def get_priority(char):
    import string
    return string.ascii_letters.index(char) + 1

def find_common_item(inputs):
    from functools import reduce
    common = reduce(set.intersection, (set(item) for item in inputs))
    assert len(common) == 1
    return common.pop()

if __name__ == "__main__":
    with open("input.txt") as fl:
        inputs = [line.strip() for line in fl.readlines()]

    total = sum(get_priority(find_common_item(split_compartments(line))) for line in inputs)
    print(total)


    from itertools import islice
    gen = iter(inputs)
    bags = list(islice(gen, 3))
    total = 0
    while bags:
        total += get_priority(find_common_item(bags))
        bags = list(islice(gen, 3))
    print (total)


