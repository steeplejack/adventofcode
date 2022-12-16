def parse_instruction(line):
    """ Return change in value of register X over a
    sequence of clock cycles. """
    line = line.strip().split()
    assert len(line) > 0
    if line[0] == "noop":
        return [0]
    elif line[0] == "addx":
        assert len(line) > 1
        delta = int(line[1])
        return [0, delta]
    raise ValueError(f"Unknown instruction {line[0]}")

def render(cycle, x):
    covered = (x-1, x, x+1)
    pos = (cycle - 1) % 40
    if pos in covered:
        return (cycle - 1, '#')
    else:
        return (cycle - 1, '.')

if __name__ == '__main__':

    with open("input.txt") as fl:
        inputs = fl.readlines()

    cycle = 1
    x = 1
    outputs = []
    display = ['@'] * 250
    for op in inputs:
        deltas = parse_instruction(op)
        for delta in deltas:
            pos, pixel = render(cycle, x)
            display[pos] = pixel
            cycle += 1
            x += delta
            if (cycle - 20) % 40 == 0:
                outputs.append(cycle * x)

    print(f"Part 1: {sum(outputs)}")

    for i in range(0, 240, 40):
        print(''.join(display[i:(i+40)]))
