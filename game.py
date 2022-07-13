from board import Board 
import dataclasses 
from typing import Callable, Sequence 
from itertools import cycle


@dataclasses.dataclass 
class Game: 
    _p1_token: str = 'x' 
    _p2_token: str = 'o'  
    
    _board: Board = dataclasses.field(default_factory=Board) 
    
    def __post_init__(self): 
        self._players = cycle([self._p1_token, self._p2_token]) 
        self._current_state = self.in_progress
        
    def in_progress(self, **kwargs): 
        pos = kwargs.pop('position')  
        token = next(self._players) 
        try: 
            self._board.make_move(pos, token)
        except ValueError: 
            next(self._players)
            
        if self._board.check_win_condition(token): 
            self._current_state = self.complete 
            print(f'Player {token} has won')
            
    def complete(self, **kwargs): 
        print('Game is completed') 
        
    def move(self, pos:int): 
        self._current_state(position=pos) 
        
    def show(self): 
        print(self._board) 
        
    def run(self): 
        while (pinput:=input('Move (1-9, q to exit)')) != 'q': 
            if pinput not in '123456789q': 
                print('Enter move again')
                continue
            pinput = int(pinput)
            self.move(pinput)
            self.show()
            
        
    
    
        