import time
from functools import wraps

from Node import Node
import numpy as np


def manhattan_distance(position, opponent_corner_coordinates):
    return sum(
        abs(val1 - val2) for val1, val2 in zip(position, opponent_corner_coordinates)
    )


def euclidean_distance(position, opponent_corner_coordinates=(10, 10)):
    point_a = np.array(position)
    point_b = np.array(opponent_corner_coordinates)
    return np.linalg.norm(point_a - point_b)


def check_if_win(matrix, size=10):
    if (
            1 in matrix[size - 4: size - 3, -2:]
            and 1 in matrix[size - 3: size - 2, -3:]
            and 1 in matrix[size - 2:, -4:]
    ):
        return 1

    elif 2 in matrix[:2, :4] and 2 in matrix[2:3, :3] and 2 in matrix[3:4, :2]:
        return 2


def check_positions_distances_value(matrix, distance_function):
    """
    This heuristic sums the distances between player positions and opponent corner
    I assume that player 1 always starts from top left corner and player 2 from bottom right
    """
    board_value = 0

    x_player_1_coordinate = 0
    y_player_1_coordinate = 0
    x_player_2_coordinate = matrix.shape[0] - 1
    y_player_2_coordinate = matrix.shape[1] - 1

    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            if matrix[i][j] == 1:
                board_value += (358 - distance_function(
                    (i, j), (x_player_2_coordinate, y_player_2_coordinate))
                                ) * check_properly_set_groups_player_1(matrix, (i, j))

            elif matrix[i][j] == 2:
                board_value += -358 + distance_function(
                    (i, j), (x_player_1_coordinate, y_player_1_coordinate)
                )

    return board_value


def make_move(board, move: Node, player):
    board[move.start_x][move.start_y] = 0
    board[move.end_x][move.end_y] = player


def restore_move(board, move: Node, player):
    board[move.start_x][move.start_y] = player
    board[move.end_x][move.end_y] = 0


def print_indexed_matrix(board):
    size = board.shape[0]

    header_row = "    " + "  ".join([f"{i:1}" for i in range(size)])
    print(header_row)

    print("   " + "-" * (size * 3))

    # Print each row with row index at the beginning
    for i in range(size):
        row = f"{i:1} | " + "  ".join([f"{board[i, j]:1}" for j in range(size)])
        print(row)


def check_properly_set_groups_player_1(matrix, position_to_check):
    if (position_to_check[0] >= matrix.shape[0] - 4 and position_to_check[1] >= matrix.shape[1] - 2) or \
            (position_to_check[0] >= matrix.shape[0] - 3 and position_to_check[1] >= matrix.shape[1] - 3) or \
            (position_to_check[0] >= matrix.shape[0] - 2 and position_to_check[1] >= matrix.shape[1] - 4):

        if (matrix[-4:, -1] == 1).all() or (matrix[-1:, -4:] == 1).all() == 1:
            if (matrix[-4:, -2] == 1).all() or (matrix[-1:, -4:] == 1).all() == 1:
                if matrix[-3][-3] == 1:
                    return 2
                return 2
            return 2
        else:
            return 1

    else:
        return 1


def check_win_player_1(matrix):
    if (matrix[-4:, -1] == 1).all() and (matrix[-1:, -4:] == 1).all()\
            and (matrix[-4:, -2] == 1).all() and (matrix[-1:, -4:] == 1).all()\
            and matrix[-3][-3] == 1:
        return True
    return False


def check_win_player_2(matrix):
    if ((matrix[0:2, 0:4] == 2).all() and
            (matrix[2, 0:3] == 2).all() and
            (matrix[3, 0:2] == 2).all()):
        return True
    return False


def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = (end_time - start_time) / 60
        print(f"Function {func.__name__}{args} {kwargs} Took {total_time:.4f} , minutes")
        return result

    return timeit_wrapper
