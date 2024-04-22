import numpy as np
import sys


def create_halma_board(size=10):
    # board = np.zeros((size, size), dtype=int)
    # board[:2, :4] = 1
    # board[2:3, :3] = 1
    # board[3:4, :2] = 1
    #
    # board[size - 4: size - 3, -2:] = 2
    # board[size - 3: size - 2, -3:] = 2
    # board[size - 2:, -4:] = 2

    board = np.zeros((10, 10), dtype=int)
    board[0, 0:3] = 1
    board[1, 0:3] = 1
    board[2, 0:3] = 1
    board[4, 4] = 1
    board[3, 4] = 1
    board[4, 3] = 1
    board[2, 4] = 1
    board[2, 4] = 1
    board[6, 6] = 1
    board[5, 6] = 1
    board[6, 5] = 1
    board[0, 2] = 0
    board[1, 1] = 0

    return board


def check_jump_moves(matrix, set_of_moves, x, y):
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
                check_jump_moves(matrix, set_of_moves, new_x, new_y)

    return set_of_moves


def check_close_moves(matrix: np.ndarray, x, y):
    set_of_moves = set()

    for i in range(x - 1, x + 2):
        for j in range(y - 1, y + 2):
            if (i >= 0 > matrix.shape[0] and j >= 0 > matrix.shape[1]) and not (i == x and j == y) and matrix[i][j] == 0:
                set_of_moves.add((i, j))

    return set_of_moves


def check_possible_moves(matrix, x, y):
    all_moves = set()
    jump_moves = check_jump_moves(matrix, all_moves, x, y)
    close_moves = check_close_moves(matrix, x, y)
    all_moves = jump_moves.union(close_moves)
    return all_moves


def manhattan_distance_heuristic(position, opponent_corner_coordinates=(10, 10)):
    """
    I assume computer always starts from (0,0) corner.
    This heuristic checks the distance between move position and opponent corner
    """
    return sum(abs(val1 - val2) for val1, val2 in zip(position, opponent_corner_coordinates))


def help_others_heuristic(position, matrix, player_number):
    """
    This heuristic adds value to moves, which help others pawns to make jump move.
    """
    directions = [(1, 1), (-1, 1), (1, -1), (-1, -1), (0, 1), (0, -1), (1, 0), (-1, 0)]
    move_value = 0

    for direction_x, direction_y in directions:
        new_x, new_y = position.x + 2 * direction_x, position.y + 2 * direction_y
        if matrix[new_x][new_y] == player_number:
            move_value += 1

    return move_value


def show_moves(matrix: np.ndarray, moves):
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            if (i, j) in moves:
                matrix[i][j] = 8

    return matrix


def check_if_win(matrix, size=10):
    if 1 in matrix[size - 4: size - 3, -2:] and \
            1 in matrix[size - 3: size - 2, -3:] and \
            1 in matrix[size - 2:, -4:]:
        return 1

    elif 2 in matrix[:2, :4] and \
            2 in matrix[2:3, :3] and \
            2 in matrix[3:4, :2]:
        return 2


def minimax(position, matrix, depth, maximizingPlayer):
    possible_moves = check_possible_moves(matrix, position[0], position[1])

    if depth == 0 or check_if_win(matrix) is not None or len(possible_moves) == 0:
        print(position)
        return manhattan_distance_heuristic(position), position

    if maximizingPlayer:
        maxEval = sys.maxsize
        for next_move in possible_moves:
            evaluation = minimax(next_move, matrix, depth - 1, False)
            if evaluation[0] < maxEval:
                maxEval = evaluation[0]
                position = next_move

        return maxEval, position

    else:
        minEval = -sys.maxsize - 1
        for next_move in possible_moves:
            evaluation = minimax(next_move, matrix, depth - 1, True)
            if evaluation[0] > minEval:
                minEval = evaluation[0]
                position = next_move

        return minEval, position


if __name__ == "__main__":
    input_matrix = create_halma_board()
    print(input_matrix)
    print(manhattan_distance_heuristic((7, 7)))
    print(minimax((1, 1), input_matrix, 3, True))


