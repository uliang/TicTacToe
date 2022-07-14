from board import Board 
import dataclasses 
from typing import Callable, Sequence 
from itertools import cycle
from contextlib import suppress


@dataclasses.dataclass 
class Game: 
    _board: Board = dataclasses.field(default_factory=Board) 
    _queue: list = dataclasses.field(default_factory=list)
    
    def __post_init__(self): 
        self._current_state = self.in_progress
        
    def in_progress(self, event, **kwargs): 
        position = kwargs.get('position', None) 
        match event: 
            case 'move': 
                with suppress(ValueError): 
                    self._board.make_move(position)
                if self._board.check_win_condition(): 
                    self._queue.append('win') 
                else: 
                    self._queue.append('move')
            case 'win':
                self._current_state = self.complete 
            case _: 
                raise ValueError(f'Unhandled event: {event}')
                
            
    def complete(self, event, **kwargs): 
        print('Game is completed') 
        
    def dispatch(self, event, **kwargs): 
        self._current_state(event, **kwargs)
        
    def show(self): 
        print(self._board) 
        
    def run(self): 
        while (pinput:=input()) != 'q': 
            if pinput not in '123456789q': 
                print('Enter move again')
                continue
            event = self._queue.pop() 
            pinput = int(pinput)
            self.dispatch(event, pinput)
            self.show()
            
        
    
    
        