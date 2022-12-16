def find_start(s, n):
    for i in range(len(s)-n):
        letters = set(s[i:(i+n)])
        if len(letters) == n:
            return i + n


if __name__ == '__main__':
    # Tests
    assert find_start('mjqjpqmgbljsphdztnvjfqwrcgsmlb', 4) == 7
    assert find_start('bvwbjplbgvbhsrlpgdmjqwftvncz', 4) == 5
    assert find_start('nppdvjthqldpwncqszvftbrmjlhg', 4) == 6
    assert find_start('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg', 4) == 10
    assert find_start('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw', 4) == 11

    assert find_start('mjqjpqmgbljsphdztnvjfqwrcgsmlb', 14) == 19
    assert find_start('bvwbjplbgvbhsrlpgdmjqwftvncz', 14) == 23
    assert find_start('nppdvjthqldpwncqszvftbrmjlhg', 14) == 23
    assert find_start('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg', 14) == 29
    assert find_start('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw', 14) == 26

    with open("input.txt") as fl:
        text = fl.readline().strip()
        
    print(f"Part 1: {find_start(text, 4)}")
    print(f"Part 2: {find_start(text, 14)}")

