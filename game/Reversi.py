import numpy as np


class Othello:

    def __init__(self):
        self.board = np.zeros((8, 8), dtype=np.int8)  # white = 1, black = -1
        self.board[3][3] = 1
        self.board[4][4] = 1
        self.board[3][4] = -1
        self.board[4][3] = -1
        self.turn = -1

    @classmethod
    def in_board(cls, x, y):
        return x >= 0 and x <= 7 and y >= 0 and y <= 7

    @classmethod
    def valid_move(cls, board, turn, x, y):
        dirs = ((0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1))
        if board[x][y] == 0:
            found = False
            for xdir, ydir in dirs:
                px = x
                py = y
                onum = False
                while True:
                    px += xdir
                    py += ydir
                    if cls.in_board(px, py):
                        if board[px][py] == 0:
                            break
                        elif board[px][py] == -turn:
                            onum = True
                        elif board[px][py] == turn:
                            if onum:
                                return True
                            else:
                                break
                    else:
                        break
        return False

    @classmethod
    def valid_moves(cls, board, turn):
        vmoves = []
        for x in range(8):
            for y in range(8):
                if cls.valid_move(board, turn, x, y):
                    vmoves.append((x, y))
        return vmoves

    #def move(self, board, turn, x, y):


if __name__ == "__main__":
    o = Othello()
    print(Othello.valid_moves(o.board, o.turn))