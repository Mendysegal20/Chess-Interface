from const import *

def diagonal_pine(self, squares, pined_piece):
    lst = []
    line = []

    # moving up-right
    for i in range(0, 8):
        if self.row - i >= 0 and self.col + i < 8:
            lst.append((self.row - i, self.col + i))
            piece = squares[self.row - i][self.col + i].piece
            if piece:
                if piece.color == self.color and piece != self: break
                if piece.name == 'king' and piece.color != self.color:
                    if len(line) == 1 and line[0] == pined_piece:
                        return lst
                    return False
                if piece != self:
                    line.append(piece)

    # moving up-left
    lst = []
    line = []
    for i in range(0, 8):
        if self.row - i >= 0 and self.col - i >= 0:
            lst.append((self.row - i, self.col - i))
            piece = squares[self.row - i][self.col - i].piece
            if piece:
                if piece.color == self.color and piece != self: break
                if piece.name == 'king' and piece.color != self.color:
                    if len(line) == 1 and line[0] == pined_piece:
                        return lst
                    return False
                if piece != self:
                    line.append(piece)

    # moving down-right
    lst = []
    line = []
    for i in range(0, 8):
        if self.row + i < 8 and self.col + i < 8:
            lst.append((self.row + i, self.col + i))
            piece = squares[self.row + i][self.col + i].piece
            if piece:
                if piece.color == self.color and piece != self: break
                if piece.name == 'king' and piece.color != self.color:
                    if len(line) == 1 and line[0] == pined_piece:
                        return lst
                    return False
                if piece != self:
                    line.append(piece)

    # moving down-left
    lst = []
    line = []
    for i in range(0, 8):
        if self.row + i < 8 and self.col - i >= 0:
            lst.append((self.row + i, self.col - i))
            piece = squares[self.row + i][self.col - i].piece
            if piece:
                if piece.color == self.color and piece != self: break
                if piece.name == 'king' and piece.color != self.color:
                    if len(line) == 1 and line[0] == pined_piece:
                        return lst
                    return False
                if piece != self:
                    line.append(piece)

    return False

def straight_pine(self, squares, pined_piece):
    lst = []
    line = []

    # moving up
    for i in range(0, 8):
        if self.row - i >= 0:
            lst.append((self.row - i, self.col))
            piece = squares[self.row - i][self.col].piece
            if piece:
                if piece.color == self.color and piece != self: break
                if piece.name == 'king' and piece.color != self.color:
                    if len(line) == 1 and line[0] == pined_piece:
                        return lst
                    return False
                if piece != self:
                    line.append(piece)

    # moving down
    lst = []
    line = []
    for i in range(0, 8):
        if self.row + i < 8:
            lst.append((self.row + i, self.col))
            piece = squares[self.row + i][self.col].piece
            if piece:
                if piece.color == self.color and piece != self: break
                if piece.name == 'king' and piece.color != self.color:
                    if len(line) == 1 and line[0] == pined_piece:
                        return lst
                    return False
                if piece != self:
                    line.append(piece)

    # moving right
    lst = []
    line = []
    for i in range(0, 8):
        if self.col + i < 8:
            lst.append((self.row, self.col + i))
            piece = squares[self.row][self.col + i].piece
            if piece:
                if piece.color == self.color and piece != self: break
                if piece.name == 'king' and piece.color != self.color:
                    if len(line) == 1 and line[0] == pined_piece:
                        return lst
                    return False
                if piece != self:
                    line.append(piece)

    # moving left
    lst = []
    line = []
    for i in range(0, 8):
        if self.col - i >= 0:
            lst.append((self.row, self.col - i))
            piece = squares[self.row][self.col - i].piece
            if piece:
                if piece.color == self.color and piece != self: break
                if piece.name == 'king' and piece.color != self.color:
                    if len(line) == 1 and line[0] == pined_piece:
                        return lst
                    return False
                if piece != self:
                    line.append(piece)

    return False

#-------------------------------------------

def straight_squares(self, squares):
    lst = []

    # looking up
    for row in range(self.row, ROWS):
        if row != self.row:
            lst.append((row, self.col))
            piece = squares[row][self.col].piece
            if piece:
                if not self._is_enemy_piece(row, self.col, squares):
                    break
                if self._is_enemy_piece(row, self.col, squares) and piece.name != 'king':
                    break

    # looking down
    for row in range(self.row, -1, -1):
        if row != self.row:
            lst.append((row, self.col))
            piece = squares[row][self.col].piece
            if piece:
                if not self._is_enemy_piece(row, self.col, squares):
                    break
                if self._is_enemy_piece(row, self.col, squares) and piece.name != 'king':
                    break

    # looking right
    for col in range(self.col, COLS):
        if col != self.col:
            lst.append((self.row, col))
            piece = squares[self.row][col].piece
            if piece:
                if not self._is_enemy_piece(self.row, col, squares):
                    break
                if self._is_enemy_piece(self.row, col, squares) and piece.name != 'king':
                    break

    # looking left
    for col in range(self.col, -1, -1):
        if col != self.col:
            lst.append((self.row, col))
            piece = squares[self.row][col].piece
            if piece:
                if not self._is_enemy_piece(self.row, col, squares):
                    break
                if self._is_enemy_piece(self.row, col, squares) and piece.name != 'king':
                    break

    return lst

def diagonal_squares(self, squares):
    lst = []

    next_row = 0
    # moving up-right
    for col in range(self.col, COLS):
        if col != self.col:
            lst.append((self.row - next_row, col))
            piece = squares[self.row - next_row][col].piece
            if piece:
                if not self._is_enemy_piece(self.row - next_row, col, squares):
                    break
                if self._is_enemy_piece(self.row - next_row, col, squares) and piece.name != 'king':
                    break
        next_row += 1

    # moving up-left
    next_row = 0
    for col in range(self.col, -1, -1):
        if col != self.col:
            lst.append((self.row - next_row, col))
            piece = squares[self.row - next_row][col].piece
            if piece:
                if not self._is_enemy_piece(self.row - next_row, col, squares):
                    break
                if self._is_enemy_piece(self.row - next_row, col, squares) and piece.name != 'king':
                    break
        next_row += 1

    # moving down-right
    next_row = 0
    for col in range(self.col, COLS):
        if -1 < self.row + next_row < 8:
            if col != self.col:
                lst.append((self.row + next_row, col))
                piece = squares[self.row + next_row][col].piece
                if piece:
                    if not self._is_enemy_piece(self.row + next_row, col, squares):
                        break
                    if self._is_enemy_piece(self.row + next_row, col, squares) and piece.name != 'king':
                        break
            next_row += 1

    # moving down-left
    next_row = 0
    for col in range(self.col, -1, -1):
        if -1 < self.row + next_row < 8:
            if col != self.col:
                lst.append((self.row + next_row, col))
                piece = squares[self.row + next_row][col].piece
                if piece:
                    if not self._is_enemy_piece(self.row + next_row, col, squares):
                        break
                    if self._is_enemy_piece(self.row + next_row, col, squares) and piece.name != 'king':
                        break
            next_row += 1
    return lst

#-------------------------------------------

def diagonal_movement(self, squares):
    if self.valid_moves: self.valid_moves.clear()  # clear and use again

    # moving up-right
    for i in range(0, 8):
        if self.row - i >= 0 and self.col + i < 8:
            if self._valid_square(self.row - i, self.col + i, squares):
                self.valid_moves.append((self.row - i, self.col + i))
                if squares[self.row - i][self.col + i].has_piece():
                    break
            elif self.col + i != self.col and not self._valid_square(self.row - i, self.col + i, squares):
                break

    # moving up-left
    for i in range(0, 8):
        if self.row - i >= 0 and self.col - i >= 0:
            if self._valid_square(self.row - i, self.col - i, squares):
                self.valid_moves.append((self.row - i, self.col - i))
                if squares[self.row - i][self.col - i].has_piece():
                    break
            elif self.col - i != self.col and not self._valid_square(self.row - i, self.col - i, squares):
                break

    # moving down-right
    for i in range(0, 8):
        if self.row + i < 8 and self.col + i < 8:
            if self._valid_square(self.row + i, self.col + i, squares):
                self.valid_moves.append((self.row + i, self.col + i))
                if squares[self.row + i][self.col + i].has_piece():
                    break
            elif self.col + i != self.col and not self._valid_square(self.row + i, self.col + i, squares):
                break

    # moving down-left
    for i in range(0, 8):
        if self.row + i < 8 and self.col - i >= 0:
            if self._valid_square(self.row + i, self.col - i, squares):
                self.valid_moves.append((self.row + i, self.col - i))
                if squares[self.row + i][self.col - i].has_piece():
                    break
            elif self.col - i != self.col and not self._valid_square(self.row + i, self.col - i, squares):
                break

    return self.valid_moves

def straight_movement(self, squares):
    if self.valid_moves: self.valid_moves.clear()  # clear and use again

    # looking up
    for i in range(0, 8):
        if self.row - i >= 0:
            if self._valid_square(self.row - i, self.col, squares):
                self.valid_moves.append((self.row - i, self.col))
                if squares[self.row - i][self.col].has_piece():
                    break
            elif self.row - i != self.row and not self._valid_square(self.row - i, self.col, squares):
                break

    # looking down
    for i in range(0, 8):
        if self.row + i < 8:
            if self._valid_square(self.row + i, self.col, squares):
                self.valid_moves.append((self.row + i, self.col))
                if squares[self.row + i][self.col].has_piece():
                    break
            elif self.row + i != self.row and not self._valid_square(self.row + i, self.col, squares):
                break

    # looking right
    for i in range(0, 8):
        if self.col + i < 8:
            if self._valid_square(self.row, self.col + i, squares):
                self.valid_moves.append((self.row, self.col + i))
                if squares[self.row][self.col + i].has_piece():
                    break
            elif self.col + i != self.col and not self._valid_square(self.row, self.col + i, squares):
                break

    # looking left
    for i in range(0, 8):
        if self.col - i >= 0:
            if self._valid_square(self.row, self.col - i, squares):
                self.valid_moves.append((self.row, self.col - i))
                if squares[self.row][self.col - i].has_piece():
                    break
            elif self.col - i != self.col and not self._valid_square(self.row, self.col - i, squares):
                break

    return self.valid_moves

#-------------------------------------------

def straight_check(self, squares):
    line = []

    # moving up
    for i in range(0, 8):
        if self.row - i >= 0:
            line.append((self.row - i, self.col))  # might be a problem
            piece = squares[self.row - i][self.col].piece
            if piece and piece != self:
                if piece.name == 'king' and piece.color != self.color:
                    return line
                else: break

    # moving down
    line = []
    for i in range(0, 8):
        if self.row + i < 8:
            line.append((self.row + i, self.col))
            piece = squares[self.row + i][self.col].piece
            if piece and piece != self:
                if piece.name == 'king' and piece.color != self.color:
                    return line
                else: break

    # moving right
    line = []
    for i in range(0, 8):
        if self.col + i < 8:
            line.append((self.row, self.col + i))
            piece = squares[self.row][self.col + i].piece
            if piece and piece != self:
                if piece.name == 'king' and piece.color != self.color:
                    return line
                else: break

    # moving left
    line = []
    for i in range(0, 8):
        if self.col - i >= 0:
            line.append((self.row, self.col - i))
            piece = squares[self.row][self.col - i].piece
            if piece and piece != self:
                if piece.name == 'king' and piece.color != self.color:
                    return line
            elif self.col - i == 0:
                line = []  # make it butter

    return line

def diagonal_check(self, squares):
    line = []

    # moving up
    for i in range(0, 8):
        if self.row - i >= 0 and self.col + i < 8:
            line.append((self.row - i, self.col + i))  # might be a problem
            piece = squares[self.row - i][self.col + i].piece
            if piece and piece != self:
                if piece.name == 'king' and piece.color != self.color:
                    return line
                else: break

    # moving down
    line.clear()
    for i in range(0, 8):
        if self.row - i >= 0 and self.col - i >= 0:
            line.append((self.row - i, self.col - i))
            piece = squares[self.row - i][self.col - i].piece
            if piece and piece != self:
                if piece.name == 'king' and piece.color != self.color:
                    return line
                else: break

    # moving right
    line.clear()
    for i in range(0, 8):
        if self.row + i < 8 and self.col + i < 8:
            line.append((self.row + i, self.col + i))
            piece = squares[self.row + i][self.col + i].piece
            if piece and piece != self:
                if piece.name == 'king' and piece.color != self.color:
                    return line
                else: break

    # moving left
    line.clear()
    for i in range(0, 8):
        if self.row + i < 8 and self.col - i >= 0:
            line.append((self.row + i, self.col - i))
            piece = squares[self.row + i][self.col - i].piece
            if piece and piece != self:
                if piece.name == 'king' and piece.color != self.color:
                    return line
                else:
                    line.clear()
                    break
        else: line.clear()

    return line


