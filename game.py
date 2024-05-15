import pygame
from const import *
from board import Board
from piece import Queen


class Game:
    def __init__(self, screen):
        self.board = Board()
        self.screen = screen
        self.valid_moves = []
        self.selected = None
        self.attacker = None
        self.is_check = False
        self.turn = WHITE

    def create(self):
        self.board.draw(self.screen)

    def move(self, row, col):
        if self.selected and (row, col) in self.valid_moves:
            self.selected.moved = True
            self.board.move(row, col, self.selected)
            self.change_turn()
        else:
            return False
        return True

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.screen, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 15)

    def change_turn(self):
        self.valid_moves.clear()
        self.turn = WHITE if self.turn == BLACK else BLACK

    def possible_moves(self, piece):
        if piece.name == 'king':
            valid_moves = piece.get_valid_moves(self.board.squares)
            threats = piece.threat_squares(self.board.squares)
            return [move for move in valid_moves if move not in threats]

        valid_moves = piece.get_valid_moves(self.board.squares)
        pined_moves = piece.get_pined_moves(self.board.squares)
        if pined_moves:
            return [move for move in valid_moves if move in pined_moves]

        return valid_moves

    def pick_king(self, king):
        possible_moves = self.possible_moves(king)
        if not possible_moves:
            print("we", king.color,"lost!")
        self.valid_moves = possible_moves

    def pick_piece(self, piece):
        self.valid_moves = self.possible_moves(piece)

    def is_checking(self, piece):
        self.valid_moves = []
        valid_moves = piece.get_valid_moves(self.board.squares)
        for move in valid_moves:
            row, col = move
            square = self.board.squares[row][col]
            if square.has_piece() and square.piece.name == 'king' and square.piece.color != piece.color:
                return True
        return False

    def defender(self, piece):
        pined_moves = piece.get_pined_moves(self.board.squares)
        possible_defense_squares = self.attacker.check_path(self.board.squares) \
                                   + [(self.attacker.get_pos())]
        piece_moves = piece.get_valid_moves(self.board.squares)  # fix the duplicates moves
        for move in piece_moves:
            if move in possible_defense_squares:
                if pined_moves and move in pined_moves:
                    self.valid_moves.append(move)
                elif not pined_moves:
                    self.valid_moves.append(move)

    # added
    def promotion(self, pawn):
        prow, pcol = pawn.get_pos()
        if prow == 0 or prow == 7:
            color = pawn.color
            self.board.squares[prow][pcol].clear_square()
            self.board.squares[prow][pcol].piece = Queen(prow, pcol, color, 'queen')

    def select(self, row, col):
        if self.selected:
            destenation = self.move(row, col)
            if not destenation:
                self.selected = None
                self.select(row, col)

            elif self.is_check:
                self.is_check = False

            else:
                team = self.selected.get_team_pieces(self.board.squares)
                for piece in team:
                    if self.is_checking(piece):
                        self.attacker = piece
                        self.is_check = True
                        break

        piece = self.board.squares[row][col].piece
        if piece and piece.color == self.turn:
            self.selected = piece
            if self.is_check and not piece.name == 'king':
                self.valid_moves.clear()
                self.defender(piece)

            elif piece.name == 'king':
                self.pick_king(piece)
            else:
                self.pick_piece(piece)

            return True
        return False

    def update(self):
        self.create()
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()



