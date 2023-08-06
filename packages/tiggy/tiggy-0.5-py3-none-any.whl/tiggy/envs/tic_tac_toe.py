import numpy as np
import numba as nb
from typing import Tuple


class TicTacToe:
    def __init__(self):
        self.board = np.zeros((3, 3))
        self.turn = 1

    def get_legal(self):
        return self.board.flatten() == 0

    def move(self, move):
        self.board[move//3, move%3] = self.turn
        final, has_won = is_final(self.board, self.turn)
        self.turn = 3 - self.turn
        obs = self.get_repr()
        if final:
            self.reset()
        return {'obs':obs, 'legal':self.get_legal(), 'is_final':final, 'reward':(reward := int(has_won))}

    def get_repr(self):
        return get_input(self.board, self.turn)

    def reset(self):
        self.board = np.zeros((3, 3))
        self.turn = 1
        return {'obs':self.get_repr(), 'legal':self.get_legal()}

@nb.njit
def is_final(board, turn) -> Tuple[bool, bool]:
    for i in range(3):
        if np.all(board[i, :] == turn) or np.all(board[:, i] == turn):
            return True, True
    if board[0, 0] == turn and board[1, 1] == turn and board[2, 2] == turn:
        return True, True
    if board[2, 0] == turn and board[1, 1] == turn and board[0, 2] == turn:
        return True, True
    if 0 not in board:
        return True, False
    return False, False

@nb.njit
def get_input(board, turn):
    in_arr = np.zeros((3, 3, 2))
    for i in range(3):
        for j in range(3):
            in_arr[i, j] = [board[i, j] == turn, board[i, j] == 3 - turn]
    return in_arr.reshape((-1, 2))