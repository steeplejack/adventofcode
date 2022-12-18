from collections import namedtuple
from enum import Enum

Point = namedtuple("Point", "x y")
PieceType = Enum("PieceType", "MINUS PLUS J I O")

class Piece():
    # For reference, the origin point of each piece is its
    # bottom left corner, (0, 0). Increasing y means UP,
    # not DOWN. Increasing x means RIGHT.
    def __init__(self, transform: Point):
        self.points = []
        self.transform = transform

    def get_transformed_points(self):
        r = self.transform
        return [Point(p.x + r.x, p.y + r.y)
                for p in self.points]

    def __str__(self):
        max_x = self.max_x()
        max_y = self.max_y()
        grid = [['.'] * (max_x + 1)
                for _ in range(max_y + 1)]
        for x, y in self.points:
            grid[max_y - y][x] = '#'
        return '\n'.join(''.join(row) for row in grid)

    def max_x(self):
        return max(point.x for point in self.points)

    def max_y(self):
        return max(point.y for point in self.points)

    def max_transformed_x(self):
        return self.max_x() + self.transform.x

    def min_transformed_x(self):
        return self.transform.x

    def max_transformed_y(self):
        return self.max_y() + self.transform.y

    def move_left(self):
        self.transform = Point(self.transform.x - 1,
                               self.transform.y)
    def move_right(self):
        self.transform = Point(self.transform.x + 1,
                               self.transform.y)
    def move_up(self):
        self.transform = Point(self.transform.x,
                               self.transform.y + 1)
    def move_down(self):
        self.transform = Point(self.transform.x,
                               self.transform.y - 1)

class Minus(Piece):
    def __init__(self, transform):
        super().__init__(transform)
        self.points = [
            Point(0, 0), Point(1, 0), Point(2, 0), Point(3, 0)
        ]

class Plus(Piece):
    def __init__(self, transform):
        super().__init__(transform)
        self.points = [
                          Point(1, 2),
             Point(0, 1), Point(1, 1), Point(2, 1),
                          Point(1, 0)       
        ]

class J(Piece):
    def __init__(self, transform):
        super().__init__(transform)
        self.points = [
                                      Point(2, 2),
                                      Point(2, 1),
            Point(0, 0), Point(1, 0), Point(2, 0)
        ]

class I(Piece):
    def __init__(self, transform):
        super().__init__(transform)
        self.points = [
            Point(0, 3),
            Point(0, 2),
            Point(0, 1),
            Point(0, 0)
        ]

class O(Piece):
    def __init__(self, transform):
        super().__init__(transform)
        self.points = [
            Point(0, 1), Point(1, 1),
            Point(0, 0), Point(1, 0)
        ]

class Board():
    def __init__(self, width) -> None:
        self.occupied = set()
        self.width = width
        self.highest = -1
        self.pieces = [PieceType.MINUS,
            PieceType.PLUS,
            PieceType.J,
            PieceType.I,
            PieceType.O]
        self.piece_index = 0
        self.piece_count = 0

    def __str__(self):
        rows = self.as_grid(self.highest + 1)
        return '\n'.join(''.join(row) for row in reversed(rows))

    def as_grid(self, y) -> list:
        rows = [['+'] + ['-'] * self.width + ['+']]
        for _ in range(y):
            rows.append(['|'] + ['.'] * self.width + ['|'])
        for point in self.occupied:
            rows[point.y + 1][point.x + 1] = '#'
        return rows

    def highest_occupied(self) -> int:
        return self.highest

    def next_origin(self) -> Point:
        return Point(2, self.highest_occupied() + 4)

    def insert_point(self, p: Point) -> None:
        self.occupied.add(p)
        if p.y > self.highest:
            self.highest = p.y

    def collides(self, piece: Piece) -> bool:
        for point in piece.get_transformed_points():
            if point.x < 0 or point.x >= self.width:
                return True
            if point in self.occupied:
                return True
            if point.y < 0:
                return True
        return False

    def create_piece(self) -> Piece:
        o = self.next_origin()
        piece_type = self.pieces[self.piece_index]
        piece = Minus(o)
        if piece_type == PieceType.PLUS:
            piece = Plus(o)
        elif piece_type == PieceType.I:
            piece = I(o)
        elif piece_type == PieceType.J:
            piece = J(o)
        elif piece_type == PieceType.O:
            piece = O(o)

        self.piece_index += 1
        self.piece_index %= len(self.pieces)
        self.piece_count += 1
        return piece

    def insert_piece(self, piece: Piece) -> None:
        for point in piece.get_transformed_points():
            self.insert_point(point)

    def draw_active_piece(self, piece) -> str:
        y = max(self.highest_occupied() + 1, piece.max_transformed_y() + 1)
        rows = self.as_grid(y)
        for point in piece.get_transformed_points():
            rows[point.y + 1][point.x + 1] = '@'
        return '\n'.join(''.join(row) for row in reversed(rows))

    def try_move_right(self, piece: Piece) -> bool:
        piece.move_right()
        if self.collides(piece):
            piece.move_left()
            return False
        return True

    def try_move_left(self, piece: Piece) -> bool:
        piece.move_left()
        if self.collides(piece):
            piece.move_right()
            return False
        return True

    def try_move_down(self, piece: Piece) -> bool:
        piece.move_down()
        if self.collides(piece):
            piece.move_up()
            return False
        return True


class Jets():
    def __init__(self, jets):
        self.jets = jets
        self.i = 0

    def next(self):
        jet = self.jets[self.i]
        self.i += 1
        self.i %= len(self.jets)
        return jet


def progress_piece(board: Board, jets: Jets, printme: bool = False):
    piece = board.create_piece()
    if printme: print('\n' + board.draw_active_piece(piece))
    while True:
        jet = jets.next()
        if jet == '>':
            moved = board.try_move_right(piece)
            if moved and printme: print('\n' + board.draw_active_piece(piece))
        elif jet == '<':
            moved = board.try_move_left(piece)
            if moved and printme: print('\n' + board.draw_active_piece(piece))
        moved_down = board.try_move_down(piece)
        if moved_down and printme:
            print('\n' + board.draw_active_piece(piece))
        elif not moved_down:
            board.insert_piece(piece)
            if printme: print('\n' + str(board))
            return


if __name__ == "__main__":
    filename = "input.txt"
    with open(filename) as fl:
        jets = Jets(fl.read().strip())

    heights = [1, 4, 6, 7, 9, 10, 13, 15, 17, 17]
    board = Board(7)
    
    for _ in range(100000):
        progress_piece(board, jets, printme = False)

    print(board.highest_occupied() + 1)


    
