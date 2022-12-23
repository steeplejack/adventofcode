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

    if (player.position, player.facing) in telep:
        next_pos, dir = telep[(player.position, player.facing)]
        next_col, next_row = next_pos
        if maze[next_row][next_col] == '#':
            return player, False
        else:
            return Player(position = next_pos, facing = dir), True
    else:
        col += 1
        col %= len(maze[row])
        if maze[row][col] == '#':
            return player, False
        elif maze[row][col] == '.':
            position = (col, row)
            return Player(position, 'R'), True
        else:
            raise ValueError("Fell into the void")

def _move_left(player, maze):
    assert player.facing == 'L'
    row = player.position[1]
    col = player.position[0]
    current = maze[row][col]
    assert not current.isspace()

    if (player.position, player.facing) in telep:
        next_pos, dir = telep[(player.position, player.facing)]
        next_col, next_row = next_pos
        if maze[next_row][next_col] == '#':
            return player, False
        else:
            return Player(position = next_pos, facing = dir), True
    else:
        col -= 1
        col %= len(maze[row])
        if maze[row][col] == '#':
            return player, False
        elif maze[row][col] == '.':
            position = (col, row)
            return Player(position, 'L'), True
        else:
            raise ValueError("Fell into the void")

def _move_up(player, maze):
    assert player.facing == 'U'
    row = player.position[1]
    col = player.position[0]
    current = maze[row][col]
    assert not current.isspace()

    if (player.position, player.facing) in telep:
        next_pos, dir = telep[(player.position, player.facing)]
        next_col, next_row = next_pos
        if maze[next_row][next_col] == '#':
            return player, False
        else:
            return Player(position = next_pos, facing = dir), True
    else:
        row -= 1
        row %= len(maze)
        if maze[row][col] == '#':
            return player, False
        elif maze[row][col] == '.':
            position = (col, row)
            return Player(position, 'U'), True
        else:
            raise ValueError("Fell into the void")

def _move_down(player, maze):
    assert player.facing == 'D'
    row = player.position[1]
    col = player.position[0]
    current = maze[row][col]
    assert not current.isspace()

    if (player.position, player.facing) in telep:
        next_pos, dir = telep[(player.position, player.facing)]
        next_col, next_row = next_pos
        if maze[next_row][next_col] == '#':
            return player, False
        else:
            return Player(position = next_pos, facing = dir), True
    else:
        row += 1
        row %= len(maze)
        if maze[row][col] == '#':
            return player, False
        elif maze[row][col] == '.':
            position = (col, row)
            return Player(position, 'D'), True
        else:
            raise ValueError("Fell into the void")


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


def edge_size(maze):
    height = len(maze) # TODO if height is 0 throw error
    width = len(maze[0])
    assert height // 4 == width // 3
    return height // 4


if __name__ == "__main__":
    filename = "input.txt"

    with open(filename) as fl:
        s = fl.read().rstrip('\n')

    maze, route = s.split('\n\n')

    maze = pad_maze(maze.split('\n'))

    tokens = route_to_tokens(route)

    player = Player((maze[0].find('.'), 0), 'R')



    # hard code teleportations for part2 - when the player
    # walks off the edge of the 2D grid it will get teleported
    # to the location in this dictionary, pointed in the right direction,
    # appropriate for the grid being wrapped onto the faces of a cube.
    telep = {}
    for i in range(edge_size(maze)):
        telep[((0, 150 + i), 'L')] = ((50 + i, 0), 'D')    # from 1 going left
        telep[((0, 100 + i), 'L')] = ((50, 49 - i), 'R')   # from 2 going left
        telep[((i, 100), 'U')] = ((50, 50 + i), 'R')       # from 2 going up
        telep[((50, 50 + i), 'L')] = ((i, 100), 'D')       # from 4 going left
        telep[((50, i), 'L')] = ((0, 149 - i), 'R')        # from 5 going left
        telep[((50 + i, 0), 'U')] = ((0, 150 + i), 'R')    # from 5 going up
        telep[((100 + i, 0), 'U')] = ((i, 199), 'U')       # from 6 going up
        telep[((149, i), 'R')] = ((99, 149 - i), 'L')      # from 6 going right
        telep[((100 + i, 49), 'D')] = ((99, 50 + i), 'L')  # from 6 going down
        telep[((99, 50 + i), 'R')] = ((100 + i, 49), 'U')  # from 4 going right
        telep[((99, 100 + i), 'R')] = ((149, 49 - i), 'L') # from 3 going right
        telep[((50 + i, 149), 'D')] = ((49, 150 + i), 'L') # from 3 going down
        telep[((49, 150 + i), 'R')] = ((50 + i, 149), 'U') # from 1 going right
        telep[((i, 199), 'D')] = ((100 + i, 0), 'D')       # from 1 going down


    # test on a maze with no walls
    old_maze = maze[:]
    new_maze = []
    for line in maze:
        new_maze.append(line.replace('#', '.'))
    maze = new_maze

    # Walking 200 steps from any point on the cube should result
    # in returning to the origin, so test along three axes
    player = Player(position=(34, 187), facing='D')
    assert move_player(player, maze, (Move.WALK, 200)) == player
    player = Player(position=(34, 187), facing='R')
    assert move_player(player, maze, (Move.WALK, 200)) == player
    player = Player(position=(34, 187), facing='L')
    assert move_player(player, maze, (Move.WALK, 200)) == player
    player = Player(position=(34, 187), facing='U')
    assert move_player(player, maze, (Move.WALK, 200)) == player
    player = Player(position=(34, 137), facing='R')
    assert move_player(player, maze, (Move.WALK, 200)) == player
    player = Player(position=(34, 137), facing='L')
    assert move_player(player, maze, (Move.WALK, 200)) == player

    maze = old_maze
    player = Player((maze[0].find('.'), 0), 'R')

    for i, token in enumerate(tokens, start = 1):
        player = move_player(player, maze, token)
    
    score = (player.position[1]+1) * 1000 + (player.position[0]+1) * 4 + facing_score[player.facing]
    print(f'Part 2: {score}')
        
