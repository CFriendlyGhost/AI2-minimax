import sys

from Node import Node
from auxiliary_functions import (
    check_positions_distances_value,
    restore_move,
    make_move,
    print_indexed_matrix,
    check_win_player_1,
    check_win_player_2,
    manhattan_distance,
    euclidean_distance,
    timeit
)
from Halma import create_halma_board, check_possible_moves


def minimax(
        board,
        depth,
        player,
        returning_move=False,
        visited_player_1=None,
        visited_player_2=None,
):
    if depth == 0:
        return check_positions_distances_value(board, manhattan_distance)

    best_move = None

    if player == 1:
        maxEval = -sys.maxsize - 1
        for next_move in check_possible_moves(board, player, visited_player_1)[0]:
            make_move(board, next_move, player)
            evaluation = minimax(
                board,
                depth - 1,
                2,
                visited_player_1=visited_player_1,
                visited_player_2=visited_player_2,
            )
            restore_move(board, next_move, player)
            if evaluation > maxEval:
                maxEval = evaluation
                best_move = next_move
        if returning_move:
            return maxEval, best_move
        return maxEval

    else:
        minEval = sys.maxsize
        for next_move in check_possible_moves(board, player, visited_player_2)[0]:
            make_move(board, next_move, player)
            evaluation = minimax(
                board,
                depth - 1,
                1,
                visited_player_1=visited_player_1,
                visited_player_2=visited_player_2,
            )
            restore_move(board, next_move, player)
            if evaluation < minEval:
                minEval = evaluation
                best_move = next_move
        if returning_move:
            return minEval, best_move
        return minEval


def minimax_alfa_beta(
        board,
        depth,
        player,
        heuristic_function,
        alpha=-sys.maxsize,
        beta=sys.maxsize,
        returning_move=False,
        visited_player_1=None,
        visited_player_2=None,
):
    if depth == 0:
        eval_value = heuristic_function(board, euclidean_distance)
        if returning_move:
            return eval_value, None
        return eval_value

    best_move = None

    if player == 1:
        maxEval = -sys.maxsize - 1
        for next_move in check_possible_moves(board, player, visited_player_1)[0]:
            make_move(board, next_move, player)
            evaluation = minimax_alfa_beta(
                board,
                depth - 1,
                2,
                heuristic_function,
                alpha,
                beta,
                False,
                visited_player_1=visited_player_1,
                visited_player_2=visited_player_2,
            )
            restore_move(board, next_move, player)
            if evaluation > maxEval:
                maxEval = evaluation
                best_move = next_move
            alpha = max(alpha, maxEval)
            if beta <= alpha:
                break
        if returning_move:
            return maxEval, best_move
        return maxEval

    else:
        minEval = sys.maxsize
        for next_move in check_possible_moves(board, player, visited_player_2)[0]:
            make_move(board, next_move, player)
            evaluation = minimax_alfa_beta(
                board,
                depth - 1,
                1,
                heuristic_function,
                alpha,
                beta,
                False,
                visited_player_1=visited_player_1,
                visited_player_2=visited_player_2,
            )
            restore_move(board, next_move, player)
            if evaluation < minEval:
                minEval = evaluation
                best_move = next_move
            beta = min(beta, minEval)
            if beta <= alpha:
                break
        if returning_move:
            return minEval, best_move
        return minEval


def evaluate_minimax(board, depth, player):
    best_eval, best_move = minimax(board, depth, player, returning_move=True)

    if best_move:
        make_move(board, best_move, player)
    return board, best_eval


def evaluate_minimax_alfa_beta(board, depth, player, heuristic_function=check_positions_distances_value):
    best_eval, best_move = minimax_alfa_beta(board, depth, player, returning_move=True,
                                             heuristic_function=heuristic_function)

    if best_move:
        make_move(board, best_move, player)
    return board, best_eval


def readValues():
    try:
        arg_start_coordinates = tuple(
            map(
                int,
                input('Type actual position coordinates value eg.: "1,1" ').split(
                    ","
                ),
            )
        )
        arg_destination_coordinates = tuple(
            map(
                int,
                input(
                    'Type destiny position coordinates value eg.: "2,2" '
                ).split(","),
            )
        )
        return arg_start_coordinates, arg_destination_coordinates

    except ValueError:
        print("Bad value.")


@timeit
def bots_play_game(board):
    i = 0
    prev_eval: int = 0
    evaluation = 1
    while True:

        if prev_eval == evaluation or i > 50:
            prev_eval = evaluation
            _, evaluation = evaluate_minimax_alfa_beta(board, 3, 1)

        else:
            prev_eval = evaluation
            _, evaluation = evaluate_minimax_alfa_beta(board, 2, 1)

        if check_win_player_1(board):
            print("player 1 won")
            break
        if check_win_player_2(board):
            print("player 2 won")
            break

        if prev_eval == evaluation:
            prev_eval = evaluation
            _, evaluation = evaluate_minimax_alfa_beta(board, 3, 2)

        else:
            prev_eval = evaluation
            _, evaluation = evaluate_minimax_alfa_beta(board, 2, 2)
        i += 1
        print_indexed_matrix(board)
        print(check_positions_distances_value(board, manhattan_distance))
        print(i)

    print_indexed_matrix(board)


def user_play_game(board):
    prev_eval = 0
    evaluation = 1

    while True:
        print_indexed_matrix(board)

        if prev_eval == evaluation:
            prev_eval = evaluation
            _, evaluation = evaluate_minimax_alfa_beta(board, 4, 1)

        else:
            prev_eval = evaluation
            _, evaluation = evaluate_minimax_alfa_beta(board, 2, 1)

        if check_win_player_1(board):
            print("player 1 won")
            break
        if check_win_player_2(board):
            print("player 2 won")
            break

        pos_start, pos_end = readValues()
        player_move = Node(pos_start[0], pos_start[1], pos_end[0], pos_end[1])
        make_move(board, player_move, 2)


if __name__ == "__main__":
    input_matrix = create_halma_board()
    bots_play_game(input_matrix)
