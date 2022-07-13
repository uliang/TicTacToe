import numpy as np 
import dataclasses
from typing import ClassVar


INFTY = 99999 


@dataclasses.dataclass
class Board:  
    _pos: ClassVar[list[tuple[int]]] = [(0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2)]
    
    board: dataclasses.InitVar = None
                   
    _value: int = dataclasses.field(init=False, default=0)  
    _alpha: int = dataclasses.field(init=False, default=-INFTY) 
    _beta: int = dataclasses.field(init=False, default=INFTY) 
    
    def __post_init__(self, board): 
        if board: 
            self._board = board
        else: 
            self._board = np.array([[' ']*3]*3)
        
    def __str__(self): 
        return str(self._board)
    
    def make_move(self, move:int, token:str): 
        x,y = self._pos[move-1]
        if self._board[x,y] == ' ': 
            self._board[x,y] = token  
        else: 
            raise ValueError
        
    def check_win_condition(self, token:str): 
        if any((self._board[i, :]==token).all() for i in range(3)): 
            return True 
        if any((self._board[:, j]==token).all() for j in range(3)): 
            return True 
        if all(self._board[i,i]==token for i in range(3)): 
            return True 
        if all(self._board[i, 2-i]==token for i in range(3)): 
            return True 
        return False
    
    def generate_next_board_state(self, token:str): 
        next_board = np.array(self._board)
        cls = self.__class__
        for i in range(3): 
            for j in range(3): 
                if next_board[i,j]==' ': 
                    next_board[i,j]=token 
                    yield cls(next_board)
                else: 
                    continue
                next_board[i,j]=' '