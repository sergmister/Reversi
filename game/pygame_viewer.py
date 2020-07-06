import numpy as np
import pygame
from pygame import gfxdraw
from Reversi import Reversi

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
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(20)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    mx, my = pygame.mouse.get_pos()
                    mx = mx // (pix + linew)
                    my = my // (pix + linew)
                    if game.mboard[mx][my] == game.turn:
                        game.move(game.board, game.turn, mx, my)
                        game.turn *= -1
                        game.update_mboard()
                        if game.check_win(game.board, game.turn):
                            run = False
                            print(game.check_win(game.board, game.turn))

        redrawGameWindow(game.board, game.mboard, game.turn)

    input()
    pygame.quit()
