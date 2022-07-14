from importlib import import_module
import argparse as args
from board import Board


def alphabetapruning(board: Board, alpha, beta, shouldmax):

    if board.check_win_condition() or board.check_terminal_state():
        # print(board)
        # print(board.value)
        return board.value

    if shouldmax:
        value = -999
        for move in board.generate_moveset():
            next_board = board.make_move(move)
            value_to_compare = alphabetapruning(next_board, alpha, beta, False)
            value = max(value, value_to_compare)
            if value >= beta:
                break
            alpha = max(alpha, value)
    else:
        value = 999
        for move in board.generate_moveset():
            next_board = board.make_move(move)
            value_to_compare = alphabetapruning(next_board, alpha, beta, True)
            value = min(value, value_to_compare)
            if value <= alpha:
                break
            beta = min(beta, value)

    # print("Returning", value, "from")
    # print(board)
    return value


if __name__ == "__main__":
    parser = args.ArgumentParser()
    parser.add_argument("game")
    arg = parser.parse_args()

    mod = import_module("board")
    game_factory = getattr(mod, arg.game)
    b = game_factory()

    value = alphabetapruning(b, -999, 999, True)
    print(value)
