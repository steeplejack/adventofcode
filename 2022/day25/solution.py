char_to_val = {
    '2': 2,
    '1': 1,
    '0': 0,
    '-': -1,
    '=': -2
}

val_to_char = {
    2: '2',
    1: '1',
    0: '0',
    -1: '-',
    -2: '='
}

def snafu_to_decimal(s):
    n = 0
    x = 1
    for char in reversed(s.strip()):
        val = char_to_val[char]
        n += val * x
        x *= 5
    return n

def max_power_of_5(n):
    f = 1
    e = 0
    while n // f > 0:
        f *= 5
        e += 1
    div = n // (f // 5)
    rem = n % (f // 5)

    if div <= 2:
        e -= 1

    w = [0] * (e + 1)

    if div > 2:
        w[e - 1] = (div % 5) - 5
        w[e] = (div + 2) // 5
    else:
        w[e] = div
    return w, rem

def w_to_snafu(w):
    # deal with carries
    while max(w) > 2:
        if w[-1] > 2:
            w.append(0)
        for i in range(len(w) - 1):
            while w[i] > 2:
                w[i] -= 5
                w[i+1] += 1
    digits = [val_to_char[digit] for digit in reversed(w)]
    return ''.join(digits)

def decimal_to_snafu(d):
    w, rem = max_power_of_5(d)
    while rem:
        v, rem = max_power_of_5(rem)
        for i in range(len(v)):
            w[i] += v[i]
    try:
        return w_to_snafu(w)
    except KeyError:
        print(w)

test_snafus = [
    '1', '2', '1=', '1-', '10', '11', '12',
    '2=', '2-', '20', '1=0', '1-0', '1=11-2',
    '1-0---0', '1121-1110-1=0'
]
test_decimals = [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
    15, 20, 2022, 12345, 314159265
]

def test_snafu_to_decimal():
    decimals = [snafu_to_decimal(s) for s in test_snafus]
    return decimals == test_decimals

def test_decimal_to_snafu():
    snafus = [decimal_to_snafu(d) for d in test_decimals]
    return snafus == test_snafus

def test_random_roundtrip(reps):
    import random
    results = []
    for _ in range(reps):
        n = random.randint(0, 10000000000)
        snafu = decimal_to_snafu(n)
        try:
            dec = snafu_to_decimal(snafu)
        except AttributeError:
            print(f'AttributeError thrown for input snafu_to_decimal({n})')
        results.append(dec == n)
    return all(results)

def test_random_roundtrip_s(reps):
    import random
    results = []
    for _ in range(reps):
        s = [random.choice('12')]
        for _ in range(random.randint(0, 20)):
            s.append(random.choice('-=012'))
        snafu = ''.join(s)
        dec = snafu_to_decimal(snafu)
        snafu2 = decimal_to_snafu(dec)
        results.append(snafu == snafu2)
    return all(results)

if __name__ == "__main__":
    assert test_snafu_to_decimal()
    assert test_decimal_to_snafu()

    filename = "input.txt"

    with open(filename) as fl:
        decimals = [snafu_to_decimal(line) for line in fl]

    print(f'Part 1: {decimal_to_snafu(sum(decimals))}')
