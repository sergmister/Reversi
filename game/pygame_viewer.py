import numpy as np
import pygame
from pygame import gfxdraw
from game.Reversi import Reversi
from AI.AI_random import AI_random
from AI.AI_minimax import AI_minimax

pygame.init()
pygame.font.init()

myfont = pygame.font.SysFont('Comis Sans MS', 80)
game_end_font = pygame.font.SysFont('Comis Sans MS', 200)

pix = 80
half = pix // 2
linew = 1
winw = (pix + linew) * 8 - linew
background = (0, 144, 103)
black = (0, 0, 0)
grey = (48, 48, 48)
white = (255, 255, 255)

display_width = winw
display_height = winw

win = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Reversi")


def redrawGameWindow(board, mboard, turn):
    win.fill(background)

    for x in range(1, 8):
        pygame.draw.rect(win, black, (x * (pix + linew), 0, linew, winw))
    for y in range(1, 8):
        pygame.draw.rect(win, black, (0, y * (pix + linew), winw, linew))

    for x in range(8):
        for y in range(8):
            if board[x][y] == 1:
                gfxdraw.filled_circle(win, x * (pix + linew) + half, y * (pix + linew) + half, half - 6, white)
                gfxdraw.aacircle(win, x * (pix + linew) + half, y * (pix + linew) + half, half - 6, black)
            elif board[x][y] == -1:
                gfxdraw.filled_circle(win, x * (pix + linew) + half, y * (pix + linew) + half, half - 6, black)
                gfxdraw.aacircle(win, x * (pix + linew) + half, y * (pix + linew) + half, half - 6, black)

    for x in range(8):
        for y in range(8):
            if mboard[x][y] == turn:
                gfxdraw.aacircle(win, x * (pix + linew) + half, y * (pix + linew) + half, half - 6, grey)

    pygame.display.update()


if __name__ == "__main__":
    game = Reversi()
    game.update_mboard()

    def play(x, y):
        Reversi.move(game.board, game.turn, x, y)
        game.turn *= -1
        game.update_mboard()
        game_over, white_total, black_total = Reversi.check_board(game.board, game.turn)
        if game_over:
            if white_total == black_total:
                print("Draw: {} / {}".format(white_total, black_total))
            elif white_total > black_total:
                print("White wins: {} / {}".format(white_total, black_total))
            elif white_total < black_total:
                print("Black wins: {} / {}".format(black_total, white_total))
            return False
        else:
            return True

    player1 = "player"     # -1 "black"
    player2 = AI_minimax(1)   # 1 "white"

    clock = pygame.time.Clock()
    run = True

    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        if game.turn == -1:
            if player1 == "player":
                if pygame.mouse.get_pressed()[0]:
                    mx, my = pygame.mouse.get_pos()
                    mx = mx // (pix + linew)
                    my = my // (pix + linew)
                    if game.mboard[mx][my] == game.turn:
                        run = play(mx, my)
            else:
                mx, my = player1.move(game.board)
                run = play(mx, my)

        elif game.turn == 1:
            if player2 == "player":
                if pygame.mouse.get_pressed()[0]:
                    mx, my = pygame.mouse.get_pos()
                    mx = mx // (pix + linew)
                    my = my // (pix + linew)
                    if game.mboard[mx][my] == game.turn:
                        run = play(mx, my)
            else:
                mx, my = player2.move(game.board)
                run = play(mx, my)

        clock.tick(20)
        redrawGameWindow(game.board, game.mboard, game.turn)

    pygame.quit()
