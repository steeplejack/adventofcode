import re

class Monkey():

    def __init__(self, items, operation, test, targets, relief = True):
        self.items = items
        self.operation = operation
        self.test = test
        self.targets = targets
        self.inspections = 0
        self.relief = relief

    def __repr__(self):
        return f'Monkey(items={self.items})'

    def has_items(self):
        return len(self.items) > 0

    def handle_item(self, other_monkeys):
        # Pop left, but can't be bothered to import a deque
        item = self.items[0]
        self.items = self.items[1:]

        self.inspections += 1
        item = self.operation(item)
        if self.relief:
            item //= 3
        test_result = self.test(item)
        target = self.pick_target(test_result)
        self.throw(item, other_monkeys[target])

    def take_turn(self, other_monkeys):
        while self.has_items():
            self.handle_item(other_monkeys)

    def pick_target(self, result):
        if result:
            return self.targets[0]
        return self.targets[1]

    def throw(self, item, target):
        assert isinstance(target, Monkey)
        target.items.append(item)

    def count_inspections(self):
        return self.inspections


def op_factory(operator, val):
    if val == 'old':
        if operator == '*':
            return lambda x: x * x
    else:
        val = int(val)
        if operator == '*':
            return lambda x: x * val
        elif operator == '+':
            return lambda x: x + val

def modulo_factory(val):
    val = int(val)
    return lambda x: x % val == 0


def play_round(monkeys):
    for monkey in monkeys:
        monkey.take_turn(monkeys)


class Parser():

    def __init__(self, relief = True):
        self.regexes = {
                'monkeys': re.compile(r'Monkey (\d):'),
                'items': re.compile(r'Starting items: ([0-9, ]+)'),
                'ops': re.compile(r'Operation: new = old (.) (.+)'),
                'tests': re.compile(r'Test: divisible by (\d+)'),
                'target_1s': re.compile(r'If true: throw to monkey (\d)'),
                'target_2s': re.compile(r'If false: throw to monkey (\d)')
                }

        self.values = {
            'monkeys': [],
            'items': [],
            'ops': [],
            'tests': [],
            'target_1s': [],
            'target_2s': []
        }

        self.relief = relief

    def parse_inputs(self, lines):
        for line in lines:
            line = line.strip()
            for key, rgx in self.regexes.items():
                search = rgx.search(line)
                if search:
                    match = search.groups()
                    self.values[key].append(match)

    def construct_monkeys(self):
        n = set(len(item) for item in self.values.values())
        assert len(n) == 1
        n = n.pop()

        monkeys = []
        for i in range(n):
            items = [int(x) for x in self.values['items'][i][0].split(', ')]
            op, val = self.values['ops'][i]
            operation = op_factory(op, val)
            test = modulo_factory(self.values['tests'][i][0])
            targets = tuple(int(self.values[key][i][0])
                            for key in ('target_1s', 'target_2s'))
            monkey = Monkey(items, operation, test, targets, relief = self.relief)
            monkeys.append(monkey)

        return monkeys


if __name__ == '__main__':

    parser = Parser(relief = True)
    with open("input.txt") as fl:
        inputs = fl.readlines()

    parser.parse_inputs(inputs)
    monkeys = parser.construct_monkeys()
    
    for _ in range(20):
        play_round(monkeys)

    for i, monkey in enumerate(monkeys):
        n = monkey.count_inspections()
        print(f'Monkey {i} inspected items {n} times.')

    counts = [monkey.count_inspections() for monkey in monkeys]
    top, second = sorted(counts, reverse = True)[:2]
    monkey_business = top * second

    print(f'Level of monkey business = {monkey_business}')
    
    # parser = Parser(relief = False)
    # parser.parse_inputs(inputs)
    # monkeys = parser.construct_monkeys()
    # 
    # check_in = [1, 20, 500]

    # for r in range(501):
    #     if r in check_in:
    #         print(f"== After round {r} ==")
    #         for i, monkey in enumerate(monkeys):
    #             n = monkey.count_inspections()
    #             print(f'Monkey {i} inspected items {n} times.')
    #     else:
    #         print(r)
    #     play_round(monkeys)


