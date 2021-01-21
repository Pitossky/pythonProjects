import pygame
from .constants import RED, WHITE, BLUE, SQUARE_SIZE
from .board import Board


class Game:
    def __init__(self, win):
        self._init()
        self.win = win

    def update(self):
        self.boards.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.boards = Board()
        self.turn = RED
        self.valid_moves = {}

    def winner(self):
        return self.boards.winner()

    def reset(self):
        self._init()

    def select(self, row, column):
        if self.selected:
            result = self._move(row, column)
            if not result:
                self.selected = None
                self.select(row, column)

        piece = self.boards.get_piece(row, column)
        if piece != 0 and piece.colour == self.turn:
            self.selected = piece
            self.valid_moves = self.boards.get_valid_moves(piece)
            return True

        return False


    def _move(self, row, column):
        piece = self.boards.get_piece(row, column)
        if self.selected and piece == 0 and (row, column) in self.valid_moves:
            self.boards.move(self.selected, row, column)
            skipped = self.valid_moves[(row, column)]
            if skipped:
                self.boards.remove(skipped)
            self.change_turn()
        else:
            return False

        return True

    def draw_valid_moves(self, moves):
        for move in moves:
            row, column = move
            pygame.draw.circle(self.win, BLUE, (column * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 15)

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED

    def get_board(self):
        return self.boards

    def ai_moves(self, board):
        self.boards = board
        self.change_turn()

