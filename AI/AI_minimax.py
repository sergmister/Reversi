import numpy as np
import random
from game.Reversi import Reversi


class AI_minimax:

    def __init__(self, player, depth=3):
        self.player = player
        self.depth = depth

    @classmethod
    def minimax(cls, board, depth, maximizingPlayer, player, turn, alpha, beta):
        if depth == 0 or not Reversi.valid_moves(board, turn):
            game_over, white_total, black_total = Reversi.check_board(board, turn)
            if game_over:
                if white_total == black_total:
                    return 1, []
                elif white_total > black_total:
                    return player * 100, []
                elif white_total < black_total:
                    return player * -100, []
            else:
                if player == 1:
                    return white_total / black_total, []
                elif player == -1:
                    return black_total / white_total, []

        elif maximizingPlayer:
            maxv = -1000000
            for x, y in Reversi.valid_moves(board, turn):
                tboard = board.copy()
                Reversi.move(tboard, turn, x, y)
                cmax, dlist = cls.minimax(tboard, depth - 1, False, player, -turn, alpha, beta)
                if cmax > maxv:
                    maxv = cmax
                    xmax, ymax = x, y
                alpha = max(alpha, cmax)
                if beta <= alpha:
                    break
            dlist.insert(0, (xmax, ymax))
            return maxv, dlist

        else:
            minv = 1000000
            for x, y in Reversi.valid_moves(board, turn):
                tboard = board.copy()
                Reversi.move(tboard, turn, x, y)
                cmin, dlist = cls.minimax(tboard, depth - 1, True, player, -turn, alpha, beta)
                if cmin < minv:
                    minv = cmin
                    xmin, ymin = x, y
                beta = min(beta, cmin)
                if beta <= alpha:
                    break
            dlist.insert(0, (xmin, ymin))
            return minv, dlist


    def move(self, board):
        x, y = self.minimax(board, self.depth, True, self.player, self.player, -1000000, 1000000)[1][0]
        return x, y

if __name__ == "__main__":
    game = Reversi()
    player = AI_minimax(-1)
    print(player.move(game.board))
