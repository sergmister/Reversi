import numpy as np
import random
from game.Reversi import Reversi


class AI_random:

    def __init__(self, player):
        self.player = player

    def move(self, board):
        x, y = random.choice(Reversi.valid_moves(board, self.player))
        return x, y
