import pygame
from .constants import RED, WHITE, SQUARE_SIZE, GREY, CROWN

class Piece:
    PADDING = 15
    OUTLINE = 2

    def __init__(self, row, column, colour):
        self.row = row
        self.column = column
        self.colour = colour
        self.king = False
        self.direction = 1
        self.x = 0
        self.y = 0
        self.calculate_position()

    def calculate_position(self):
        self.x = self.column * SQUARE_SIZE + SQUARE_SIZE//2
        self.y = self.row * SQUARE_SIZE + SQUARE_SIZE//2

    def make_king(self):
        self.king = True

    def draw(self, win):
        radius = SQUARE_SIZE//2 - self.PADDING
        pygame.draw.circle(win, GREY, (self.x, self.y), radius + self.OUTLINE)
        pygame.draw.circle(win, self.colour, (self.x, self.y), radius)
        if self.king:
            win.blit(CROWN, (self.x - CROWN.get_width()//2, self.y - CROWN.get_height()//2))

    def move(self, row, column):
        self.row = row
        self.column = column
        self.calculate_position()

    def __repr__(self):
        return str(self.colour)

