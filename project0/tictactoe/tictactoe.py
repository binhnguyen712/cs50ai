"""
Tic Tac Toe Player
"""

import math
import copy
X = "X"
O = "O"
EMPTY = None

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = 0
    o_count = 0
    for row in board:
        for tile in row:
            if tile == X:
                x_count += 1
            elif tile == O:
                o_count += 1
    if x_count == o_count:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for i, row in enumerate(board):
        for j, tile in enumerate(row):
            if tile != X and tile != O:
                actions.add((i, j))
    return actions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    copy_board = copy.deepcopy(board)
    current_player = player(copy_board)
    i, j = action
    if 0 <= i <= 2 and 0 <= j <= 2:
        if copy_board[i][j] == EMPTY:
            copy_board[i][j] = current_player
            return copy_board
        else:
            raise ValueError("Invalid action")
    else:
        raise ValueError("Invalid action")

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for row in board:
        if row[0] == row[1] == row[2] != EMPTY:
            return row[0]
    for j in range(len(board)):
        if board[0][j] == board[1][j] == board[2][j] != EMPTY:
            return board[0][j]
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
            return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
            return board[0][2]
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) == X or winner(board) == O:
        return True
    else:
        for row in board:
            for tile in row:
                if tile == EMPTY:
                    return False
        return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board) == True:
        return None
    else:
        if player(board) == X:
            _, action = maxvalue(board)
        else:
            _, action = minvalue(board)
        return action


def maxvalue(board):
    best_action = None
    v = -10000000
    if terminal(board):
        return (utility(board), None)
    for action in actions(board):
        value, _ = minvalue(result(board, action))
        if value > v:
            v = value
            best_action = action
    return (v, best_action)

def minvalue(board):
    v = 10000000
    if terminal(board):
        return (utility(board), None)
    for action in actions(board):
        value, _ = maxvalue(result(board, action))
        if value < v:
            v = value
            best_action = action
    return (v, best_action)
