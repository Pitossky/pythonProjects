import pygame
from .constants import BLACK, ROWS, RED, SQUARE_SIZE, COLUMNS, WHITE
from .piece import Piece

class Board:
    def __init__(self):
        self.board = []
        self.red_left = self.white_left = 12
        self.red_kings = self.white_kings = 0
        self.create_board()

    def draw_squares(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            for column in range(row % 2, ROWS, 2):
                pygame.draw.rect(win, RED, (row*SQUARE_SIZE, column*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def evaluate(self):
        return self.white_left - self.red_left + (self.white_kings * 0.5 - self.red_kings * 0.5)

    def get_all_pieces(self, colour):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.colour == colour:
                    pieces.append(piece)

        return pieces

    def move(self, piece, row, column):
        self.board[piece.row][piece.column], self.board[row][column] = self.board[row][column], self.board[piece.row][piece.column]
        piece.move(row, column)

        if row == ROWS or row == 0:
            piece.make_king()
            if piece.colour == WHITE:
                self.white_kings += 1
            else:
                self.red_kings += 1

    def get_piece(self, row, column):
        return self.board[row][column]

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for column in range(COLUMNS):
                if column % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, column, WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row, column, RED))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for column in range(COLUMNS):
                piece = self.board[row][column]
                if piece != 0:
                    piece.draw(win)

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.column] = 0
            if piece != 0:
                if piece.colour == RED:
                    self.red_left -= 1
                else:
                    self.white_left -= 1

    def winner(self):
        if self.red_left <= 0:
            return WHITE
        elif self.white_left <= 0:
            return RED

        return None

    def get_valid_moves(self, piece):
        moves = {}
        left = piece.column - 1
        right = piece.column + 1
        row = piece.row

        if piece.colour == RED or piece.king:
            moves.update(self._move_left(row -1, max(row-3, -1), -1, piece.colour, left))
            moves.update(self._move_right(row -1, max(row-3, -1), -1, piece.colour, right))
        if piece.colour == WHITE or piece.king:
            moves.update(self._move_left(row +1, min(row+3, ROWS), 1, piece.colour, left))
            moves.update(self._move_right(row +1, min(row+3, ROWS), 1, piece.colour, right))

        return moves

    def _move_left(self, start, stop, step, colour, left, skipped=[]):
        moves = {}
        last = []
        for row in range(start, stop, step):
            if left < 0:
                break
            current = self.board[row][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(row, left)] = last + skipped
                else:
                    moves[(row, left)] = last

                if last:
                    if step == -1:
                        row = max(row-3, 0)
                    else:
                        row = min(row+3, ROWS)

                    moves.update(self._move_left(row+step, row, step, colour, left-1, skipped=last))
                    moves.update(self._move_right(row + step, row, step, colour, left+1, skipped=last))
                break

            elif current.colour == colour:
                break
            else:
                last = [current]

            left -= 1
        return moves

    def _move_right(self, start, stop, step, colour, right, skipped=[]):
        moves = {}
        last = []
        for row in range(start, stop, step):
            if right >= COLUMNS:
                break
            current = self.board[row][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(row, right)] = last + skipped
                else:
                    moves[(row, right)] = last

                if last:
                    if step == -1:
                        row = max(row - 3, 0)
                    else:
                        row = min(row + 3, ROWS)

                    moves.update(self._move_left(row + step, row, step, colour, right-1, skipped=last))
                    moves.update(self._move_right(row + step, row, step, colour, right+1, skipped=last))
                break

            elif current.colour == colour:
                break
            else:
                last = [current]

            right += 1
        return moves







