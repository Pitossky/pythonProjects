import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, WHITE, RED
from checkers.game import Game
from minimax.algorithm import minimax

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers Game')

def get_row_column_from_mouse(pos):
    x, y = pos
    row = y//SQUARE_SIZE
    column = x//SQUARE_SIZE
    return row, column

def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    while run:
        clock.tick(FPS)

        if game.turn == WHITE:
            value, new_board = minimax(game.get_board(), 3, WHITE, game)
            game.ai_moves(new_board)

        if game.winner() != None:
            print(game.winner())
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                row, column = get_row_column_from_mouse(position)
                game.select(row, column)

        game.update()

    pygame.quit()


main()
