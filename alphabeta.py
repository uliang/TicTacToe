from board import Board

b = Board()


def alphabetapruning(board, alpha, beta, shouldmax):

    if board.check_win_condition() or board.depth == 9:
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


if __name__ == '__main__':
    value = alphabetapruning(b, -999, 999, True)
    print(value)
