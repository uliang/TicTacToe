from board import Board

b = Board()


def alphabetapruning(board, alpha, beta, shouldmax):

    if board.check_win_condition():
        value = 1 if shouldmax else -1
        print("Returning", value, "from")
        print(board)
        return value
    elif board.depth == 9:
        value = 0
        print("Returning", value, "from")
        print(board)
        return value

    for move in board.generate_moveset():
        next_board = board.make_move(move)
        value_to_compare = yield from alphabetapruning(
            next_board, alpha, beta, not shouldmax
        )
        if value_to_compare is None:
            continue
        if shouldmax:
            value = -999
            value = max(value, value_to_compare)
            alpha = max(alpha, value)
            if value >= beta:
                break
        else:
            value = 999
            value = min(value, value_to_compare)
            beta = min(beta, value)
            if value <= alpha:
                break

        print("Yielding", value, "from")
        print(board)
        yield value


search = alphabetapruning(b, -999, 999, False)
while input() != "q":
    next(search)
