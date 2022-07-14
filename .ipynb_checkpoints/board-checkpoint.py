import numpy as np 
import itertools as it


INFTY = 99999 


class InvalidMove(Exception): 
    def __init__(self, msg, *args, **kwargs): 
        super().__init__(msg, *args, **kwargs)


class Board:  
    _pos = [(0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2)]
    _next_token = {'x': 'o', 'o': 'x'}
        
        
    def __init__(self, board=None, player_token='x'): 
        if board is not None: 
            self._board = board
        else: 
            self._board = np.array([[' ']*3]*3)
        self._player_token = player_token 
        
    @property
    def depth(self): 
        unfilled = np.sum(self._board == ' ')
        return 9-unfilled
               
    def __str__(self): 
        return str(self._board)
    
    def make_move(self, move:int): 
        x,y = self._pos[move]
        if self._board[x,y] == ' ': 
            token = self._player_token
            next_board = np.array(self._board)
            next_board[x,y] = token 
            new_token = self._next_token[token]
            return Board(next_board, new_token) 
        else: 
            raise InvalidMove("Position is occupied") 
        
    def check_win_condition(self): 
        token = self._player_token
        if any((self._board[i, :]==token).all() for i in range(3)): 
            return True 
        if any((self._board[:, j]==token).all() for j in range(3)): 
            return True 
        if all(self._board[i,i]==token for i in range(3)): 
            return True 
        if all(self._board[i, 2-i]==token for i in range(3)): 
            return True 
        return False
    
    def generate_moveset(self): 
        for i in range(3): 
            for j in range(3): 
                if self._board[i,j]==' ': 
                    yield 3*i+j
                
