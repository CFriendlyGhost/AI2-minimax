import numpy as np
from node import Node


def create_halma_board(size=10):
    board = np.zeros((size, size), dtype=int)

    board[size - 4: size - 3, -2:] = 2
    board[size - 3: size - 2, -3:] = 2
    board[size - 2:, -4:] = 2

    board[0:2, 0:4] = 1
    board[2, 0:3] = 1
    board[3, 0:2] = 1

    return board


def check_jump_moves(matrix, x, y, set_of_moves=None):
    """
    This function tries to find moves that required jumping over other pawns
    :param matrix: halma game board
    :param x: x coordinate of pawn
    :param y: y coordinate of pawn
    :param set_of_moves: set of previously made moves, required for recursive function
    :return: returns available jump moves for exact pawn
    """
    if set_of_moves is None:
        set_of_moves = set()
    directions = [(1, 1), (-1, 1), (1, -1), (-1, -1), (0, 1), (0, -1), (1, 0), (-1, 0)]

    for direction_x, direction_y in directions:
        new_x, new_y = x + 2 * direction_x, y + 2 * direction_y
        if 0 <= new_x < matrix.shape[0] and 0 <= new_y < matrix.shape[1]:
            if (
                matrix[x + direction_x][y + direction_y] != 0
                and matrix[new_x][new_y] == 0
                and (new_x, new_y) not in set_of_moves
            ):
                set_of_moves.add((new_x, new_y))
                check_jump_moves(matrix, new_x, new_y, set_of_moves)

    return set_of_moves


def check_close_moves(matrix: np.ndarray, x, y):
    set_of_moves = set()

    for i in range(x - 1, x + 2):
        for j in range(y - 1, y + 2):
            if (
                (0 <= i < matrix.shape[0] and 0 <= j < matrix.shape[1])
                and not (i == x and j == y)
                and matrix[i][j] == 0
            ):
                set_of_moves.add((i, j))

    return set_of_moves


def check_possible_moves(matrix, player, visited=None):
    """
    It tries to find all possible jump and close moves for all player's pawns.
    """
    nodes = set()
    if visited is None:
        visited = set()

    all_moves = set()

    for x in range(matrix.shape[0]):
        for y in range(matrix.shape[1]):
            if matrix[x][y] == player and (x, y) not in visited:
                jump_moves = check_jump_moves(matrix, x, y)
                close_moves = check_close_moves(matrix, x, y)
                all_moves.update(jump_moves.union(close_moves))
                nodes.update(
                    {
                        Node(x, y, move[0], move[1])
                        for move in jump_moves.union(close_moves)
                    }
                )

    visited.update(all_moves)

    return nodes, visited
