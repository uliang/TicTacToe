import abc
import numpy as np
import itertools as it


INFTY = 99999


class InvalidMove(Exception):
    def __init__(self, msg, *args, **kwargs):
        super().__init__(msg, *args, **kwargs)


class Board(abc.ABC): 

    @abc.abstractproperty 
    def depth(self): 
        ... 

    @abc.abstractproperty 
    def value(self): 
        ... 
    
    @abc.abstractmethod 
    def reset(self):
        ...

    @abc.abstractmethod 
    def make_move(self, move: int):
        ... 

    @abc.abstractmethod 
    def check_win_condition(self): 
        ... 

    @abc.abstractmethod 
    def check_terminal_state(self): 
        ...

    @abc.abstractmethod 
    def generate_moveset(self): 
        ... 


class TicTacToe(Board):
    _pos = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1),
            (1, 2), (2, 0), (2, 1), (2, 2)]
    _next_token = {'x': 'o', 'o': 'x'}
    _empty_board = np.array([[' ']*3]*3)

    def __init__(self, board=None, player_token='x'):
        if board is not None:
            self._board = board
        else:
            self._board = np.array([[' ']*3]*3)
        self._player_token = player_token

    def reset(self): 
        self._board = self._empty_board

    @property
    def depth(self):
        unfilled = np.sum(self._board == ' ')
        return 9-unfilled

    def __str__(self):
        return str(self._board)

    def make_move(self, move: int):
        x, y = self._pos[move]
        if self._board[x, y] == ' ':
            token = self._player_token
            next_board = np.array(self._board)
            next_board[x, y] = token
            new_token = self._next_token[token]
            return TicTacToe(next_board, new_token)
        else:
            raise InvalidMove("Position is occupied")

    def check_win_condition(self):
        b = self._board
        
        if any(((b[i, :] == b[i, 0]) & (b[i, 0] != ' ')).all() for i in range(3)):
            return True
        if any(((b[:, j] == b[0, j]) & (b[0,j] != ' ')).all() for j in range(3)):
            return True
        if all((b[i, i] == b[0, 0]) & (b[0,0] != ' ') for i in range(3)):
            return True
        if all((b[i, 2-i] == b[0, 2]) & (b[0,2] != ' ') for i in range(3)):
            return True
        return False

    def generate_moveset(self):
        for i in range(3):
            for j in range(3):
                if self._board[i, j] == ' ':
                    yield 3*i+j

    @property 
    def value(self): 
        if self.check_win_condition(): 
            return 1 if (self._player_token == 'o') else -1
        elif self.depth == 9: 
            return 0 
        raise ValueError('Board not in a winning or draw state.') 

    def check_terminal_state(self):
        return self.depth == 9 
