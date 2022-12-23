from enum import Enum
from collections import namedtuple

Move = Enum("Move", "WALK TURN")
Player = namedtuple("Player", "position facing")

turns = {'R': {'R': 'D', 'L': 'U'},
         'U': {'R': 'R', 'L': 'L'},
         'L': {'R': 'U', 'L': 'D'},
         'D': {'R': 'L', 'L': 'R'}}

facing_score = {'R': 0, 'D': 1, 'L': 2, 'U': 3}

def pad_maze(maze):
    padded = []

    max_line_length = max(len(line) for line in maze)

    for line in maze:
        if len(line) < max_line_length:
            to_add = max_line_length - len(line)
            line = line + ' ' * to_add
        padded.append(line)
    return padded

def route_to_tokens(route):
    steps = ''
    for char in route:
        if char.isdigit():
            steps += char
        else:
            yield((Move.WALK, int(steps)))
            steps = ''
            yield((Move.TURN, char))
    if steps != '':
        yield((Move.WALK, int(steps)))
    

def _move_right(player, maze):
    assert player.facing == 'R'
    row = player.position[1]
    col = player.position[0]
    current = maze[row][col]
    assert not current.isspace()
    col += 1
    col %= len(maze[row])
    if maze[row][col] == '#':
        return player, False
    elif maze[row][col] == '.':
        position = (col, row)
        return Player(position, 'R'), True
    else:
        while maze[row][col].isspace():
            col += 1
            col %= len(maze[row])
        if maze[row][col] == '#':
            return player, False
        else:
            position = (col, row)
            return Player(position, 'R'), True


def _move_left(player, maze):
    assert player.facing == 'L'
    row = player.position[1]
    col = player.position[0]
    current = maze[row][col]
    assert not current.isspace()
    col -= 1
    col %= len(maze[row])
    if maze[row][col] == '#':
        return player, False
    elif maze[row][col] == '.':
        position = (col, row)
        return Player(position, 'L'), True
    else:
        while maze[row][col].isspace():
            col -= 1
            col %= len(maze[row])
        if maze[row][col] == '#':
            return player, False
        else:
            position = (col, row)
            return Player(position, 'L'), True

def _move_up(player, maze):
    assert player.facing == 'U'
    row = player.position[1]
    col = player.position[0]
    current = maze[row][col]
    assert not current.isspace()
    row -= 1
    row %= len(maze)
    if maze[row][col] == '#':
        return player, False
    elif maze[row][col] == '.':
        position = (col, row)
        return Player(position, 'U'), True
    else:
        while maze[row][col].isspace():
            row -= 1
            row %= len(maze)
        if maze[row][col] == '#':
            return player, False
        else:
            position = (col, row)
            return Player(position, 'U'), True

def _move_down(player, maze):
    assert player.facing == 'D'
    row = player.position[1]
    col = player.position[0]
    current = maze[row][col]
    assert not current.isspace()
    row += 1
    row %= len(maze)
    if maze[row][col] == '#':
        return player, False
    elif maze[row][col] == '.':
        position = (col, row)
        return Player(position, 'D'), True
    else:
        while maze[row][col].isspace():
            row += 1
            row %= len(maze)
        if maze[row][col] == '#':
            return player, False
        else:
            position = (col, row)
            return Player(position, 'D'), True


def move_player(player, maze, token):
    new_player = Player(player.position, player.facing)
    if token[0] == Move.TURN:
        new_player = Player(player.position, turns[player.facing][token[1]])
        return new_player
    else:
        moved = False
        for _ in range(token[1]):
            if player.facing == 'R':
                player, moved = _move_right(player, maze)
            elif player.facing == 'L':
                player, moved = _move_left(player, maze)
            elif player.facing == 'D':
                player, moved = _move_down(player, maze)
            elif player.facing == 'U':
                player, moved = _move_up(player, maze)
            if not moved:
                break
        return player


def draw(maze, player):
    col, row = player.position
    player_char = '@'
    if player.facing == 'R':
        player_char = '>'
    if player.facing == 'L':
        player_char = '<'
    if player.facing == 'U':
        player_char = '^'
    if player.facing == 'D':
        player_char = 'v'
    render = maze[:]
    render[row] = render[row][:col] + player_char + render[row][col+1:]
    print('\n'.join(render))


if __name__ == "__main__":
    filename = "input.txt"

    with open(filename) as fl:
        s = fl.read().rstrip('\n')

    maze, route = s.split('\n\n')

    maze = pad_maze(maze.split('\n'))

    tokens = route_to_tokens(route)

    player = Player((maze[0].find('.'), 0), 'R')

    for i, token in enumerate(tokens, start = 1):
        player = move_player(player, maze, token)

    score = (player.position[1]+1) * 1000 + (player.position[0]+1) * 4 + facing_score[player.facing]
    print(f'Part 1: {score}')


    
