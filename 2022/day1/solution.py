with open('input.txt') as fl:
    data = fl.readlines()

elves = list()

for item in data:
    item = item.strip()
    if len(elves) == 0 or item == '':
        elves.append(list())
    if item > '':
        calories = int(item)
        elves[-1].append(calories)

totals = [sum(x) for x in elves]
top_three = sorted(totals, key = lambda x: -x)[:3]

print("The most calories carried by a single elf, and the total carried by the top three elves:\n")
print(f"{top_three[0]}\n{sum(top_three)}")

