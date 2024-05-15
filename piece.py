import pygame
from const import *
import movment


class Piece:
    def __init__(self, row, col, color, name):

        self.row = row
        self.col = col
        self.name = name
        self.color = WHITE if color == 'white' else BLACK
        self.valid_moves = []
        self.moved = False
        self.pos = (row * SQUARE_SIZE, col * SQUARE_SIZE)

        self.x = 0
        self.y = 0
        self._calc_pos()

        img = './const' + '\\' + color + '_' + name + '.png'
        self.image = pygame.image.load(img).convert_alpha()
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def get_pos(self):
        return self.row, self.col

    def _get_enemy_pieces(self, squares):
        enemies = []
        for row in range(ROWS):
            for col in range(COLS):
                piece = squares[row][col].piece
                if piece and piece.color != self.color:
                    enemies.append(piece)
        return enemies

    def get_team_pieces(self, squares):
        team = []
        for row in range(ROWS):
            for col in range(COLS):
                piece = squares[row][col].piece
                if piece and piece.color == self.color and piece.name != 'king':
                    team.append(piece)
        return team

    def get_pined_moves(self, squares):
        enemies = self._get_enemy_pieces(squares)
        res = []
        for enemy in enemies:
            if not res:
                if enemy.name == 'queen':
                    res1 = movment.diagonal_pine(enemy,squares, self)
                    if res1: res = res1
                    else:
                        res = movment.straight_pine(enemy, squares, self)

                elif enemy.name == 'rook':
                    res = movment.straight_pine(enemy, squares, self)

                elif enemy.name == 'bishop':
                    res = movment.diagonal_pine(enemy, squares, self)

        if res: return res
        return []

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def _calc_pos(self):
        self.x = self.col * SQUARE_SIZE
        self.y = self.row * SQUARE_SIZE

    def move(self, row, col):
        self.col = col
        self.row = row
        self._calc_pos()

    def _valid_square(self, row, col, squares):
        piece = squares[row][col].piece
        if not piece or piece.color != self.color:
            return True
        return False

    def _is_enemy_piece(self, row, col, squares):
        piece = squares[row][col].piece
        if piece:
            return piece.color != self.color
        return False

    def _is_row_col(self, row, col):
        return -1 < row < ROWS and -1 < col < COLS

    def check_path(self, squares):
        if self.name == 'bishop':
            return movment.diagonal_check(self, squares)
        elif self.name == 'queen':
            return movment.straight_check(self, squares) \
                + movment.diagonal_check(self, squares)
        elif self.name == 'rook':
            return movment.straight_check(self, squares)
        return []


class King(Piece):
    def __init__(self, row, col, color, name='king'):
        super().__init__(row, col, color, name)

    def get_threats(self, squares):
        moves = []
        # moving up
        next_row = self.row + 1
        for col in [self.col - 1, self.col, self.col + 1]:
            if self._is_row_col(next_row, col):
                moves.append((next_row, col))

        # moving down
        next_row = self.row - 1
        for col in [self.col - 1, self.col, self.col + 1]:
            if self._is_row_col(next_row, col):
                moves.append((next_row, col))

        # moving aside
        if self._is_row_col(self.row, self.col + 1):
            moves.append((self.row, self.col + 1))

        if self._is_row_col(self.row, self.col - 1):
            moves.append((self.row, self.col - 1))

        return moves

    def threat_squares(self, squares):
        threats = []
        for row in range(ROWS):
            for col in range(COLS):
                if self._is_enemy_piece(row, col, squares):
                    threats += squares[row][col].piece.get_threats(squares)

        return threats

    def get_valid_moves(self, squares):
        if self.valid_moves: self.valid_moves.clear()  # clear and use again

        # moving up
        next_row = self.row + 1
        for col in [self.col - 1, self.col, self.col + 1]:
            if self._is_row_col(next_row, col) and self._valid_square(next_row, col, squares):
                self.valid_moves.append((next_row, col))

        # moving down
        next_row = self.row - 1
        for col in [self.col - 1, self.col, self.col + 1]:
            if self._is_row_col(next_row, col) and self._valid_square(next_row, col, squares):
                self.valid_moves.append((next_row, col))

        # moving aside
        if self._is_row_col(self.row, self.col + 1) and self._valid_square(self.row, self.col + 1, squares):
            self.valid_moves.append((self.row, self.col + 1))

        if self._is_row_col(self.row, self.col - 1) and self._valid_square(self.row, self.col - 1, squares):
            self.valid_moves.append((self.row, self.col - 1))

        return self.valid_moves


class Queen(Piece):
    def __init__(self, row, col, color, name='queen'):
        super().__init__(row, col, color, name)

    def get_valid_moves(self, squares):
        return self.valid_moves + movment.straight_movement(self, squares) + \
            movment.diagonal_movement(self, squares)  # self.valid_moves +... ???

    def get_threats(self, squares):
        return movment.diagonal_squares(self, squares) + movment.straight_squares(self,squares)


class Rook(Piece):
    def __init__(self, row, col, color, name='rook'):
        super().__init__(row, col, color, name)

    def get_valid_moves(self, squares):
        return movment.straight_movement(self, squares)

    def get_threats(self, squares):
        return movment.straight_squares(self, squares)


class Bishop(Piece):
    def __init__(self, row, col, color, name='bishop'):
        super().__init__(row, col, color, name)

    def get_valid_moves(self, squares):
        return movment.diagonal_movement(self, squares)

    def get_threats(self, squares):
        return movment.diagonal_squares(self, squares)


class Knight(Piece):
    def __init__(self, row, col, color, name='knight'):
        super().__init__(row, col, color, name)

    def get_valid_moves(self, squares):
        if self.valid_moves: self.valid_moves.clear()  # clear and use again

        for row in range(1, 3):
            if self.row + row < 8:
                if row == 1 and self.col + 2 < COLS and self._valid_square(self.row + row, self.col + 2, squares):
                    self.valid_moves.append((self.row + row, self.col + 2))
                if row == 1 and self.col - 2 >= 0 and self._valid_square(self.row + row, self.col - 2, squares):
                    self.valid_moves.append((self.row + row, self.col - 2))

                if row == 2 and self.col + 1 < COLS and self._valid_square(self.row + row, self.col + 1, squares):
                    self.valid_moves.append((self.row + row, self.col + 1))
                if row == 2 and self.col - 1 >= 0 and self._valid_square(self.row + row, self.col - 1, squares):
                    self.valid_moves.append((self.row + row, self.col - 1))

            if self.row - row >= 0:
                if row == 1 and self.col + 2 < COLS and self._valid_square(self.row - row, self.col + 2, squares):
                    self.valid_moves.append((self.row - row, self.col + 2))
                if row == 1 and self.col - 2 >= 0 and self._valid_square(self.row - row, self.col - 2, squares):
                    self.valid_moves.append((self.row - row, self.col - 2))

                if row == 2 and self.col + 1 < COLS and self._valid_square(self.row - row, self.col + 1, squares):
                    self.valid_moves.append((self.row - row, self.col + 1))
                if row == 2 and self.col - 1 >= 0 and self._valid_square(self.row - row, self.col - 1, squares):
                    self.valid_moves.append((self.row - row, self.col - 1))

        return self.valid_moves

    def get_threats(self, squares):
        threats = []

        for row in range(1, 3):
            if self.row + row < 8:
                if row == 1 and self.col + 2 < COLS:
                    threats.append((self.row + row, self.col + 2))
                if row == 1 and self.col - 2 >= 0:
                    threats.append((self.row + row, self.col - 2))

                if row == 2 and self.col + 1 < COLS:
                    threats.append((self.row + row, self.col + 1))
                if row == 2 and self.col - 1 >= 0:
                    threats.append((self.row + row, self.col - 1))

            if self.row - row >= 0:
                if row == 1 and self.col + 2 < COLS:
                    threats.append((self.row - row, self.col + 2))
                if row == 1 and self.col - 2 >= 0:
                    threats.append((self.row - row, self.col - 2))

                if row == 2 and self.col + 1 < COLS:
                    threats.append((self.row - row, self.col + 1))
                if row == 2 and self.col - 1 >= 0:
                    threats.append((self.row - row, self.col - 1))

        return threats


class Pawn(Piece):
    def __init__(self, row, col, color, name='pawn'):
        super().__init__(row, col, color, name)
        self.dir = 1 if color == 'black' else -1

    def get_valid_moves(self, squares):
        if self.valid_moves: self.valid_moves.clear()  # clear and use again
        next_row = self.row + self.dir

        # move 2 steps at the opening
        if not self.moved and self._is_row_col(self.row + self.dir * 2, self.col):
            first_square = squares[self.row + self.dir][self.col]
            second_square = squares[self.row + self.dir * 2][self.col]
            if not first_square.has_piece() and not second_square.has_piece():
                self.valid_moves.append((self.row + self.dir * 2, self.col))

        if -1 < next_row < ROWS:
            # straight movement
            if not squares[next_row][self.col].has_piece():
                self.valid_moves.append((next_row, self.col))

            # diagonal capture
            right_col = self.col + 1
            left_col = self.col - 1
            if right_col < COLS and self._is_enemy_piece(next_row, right_col, squares):
                self.valid_moves.append((next_row, right_col))

            if left_col > -1 and self._is_enemy_piece(next_row, left_col, squares):
                self.valid_moves.append((next_row, left_col))

        return self.valid_moves

    def get_threats(self, squares):
        lst = []
        right_col = self.col + 1
        left_col = self.col - 1
        next_row = self.row + self.dir
        if self._is_row_col(next_row, right_col):
            lst.append((next_row, right_col))

        if self._is_row_col(next_row, left_col):
            lst.append((next_row, left_col))

        return lst
