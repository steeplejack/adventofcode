class ParseError(Exception):
    pass

def parse(s: str) -> list:
    assert s.count('[') == s.count(']')
    stack: list = []
    root: list | None = None
    current: list = []
    collecting: bool = False
    number: list = []

    for char in s:
        if char == '[':
            if root is None:
                stack.append(current)
                root = current
            else:
                current.append([])
                current = current[-1]
                stack.append(current)
        elif char == ']':
            if collecting:
                current.append(int(''.join(number)))
                number = []
            collecting = False
            stack.pop()
            if len(stack) > 0:
                current = stack[-1]
            else:
                break
        elif char.isdigit():
            number.append(char)
            collecting = True
        elif char == ',':
            if collecting:
                current.append(int(''.join(number)))
                number = []
            collecting = False
        elif char.isspace():
            continue
        else:
            raise ParseError(f"Unrecognised character, {char}")

    return root

