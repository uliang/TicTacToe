from board import Board 
import dataclasses 
from contextlib import suppress
from collections import namedtuple 
from board import InvalidMove


Event = namedtuple('Event', ['name', 'payload'], defaults=[None, None])


@dataclasses.dataclass 
class Game: 
    _board: Board = dataclasses.field(default_factory=Board) 
    _queue: list = dataclasses.field(default_factory=list)
    
    def __post_init__(self): 
        self._current_state = self.in_progress
        self._queue.append(Event('tick'))
        
    def in_progress(self, event: Event): 
        match event.name: 
            case 'tick': 
                print('Enter next move', 'Valid moves are:', sep='\n' )
                print('q', *self._board.generate_moveset(), sep= ',') 
                pinput = input('>')
                if pinput == 'q': 
                    raise SystemExit 
                position = int(pinput)

                with suppress(InvalidMove): 
                    self._board = self._board.make_move(position)

                if self._board.check_win_condition(): 
                    self._current_state = self.complete 
                self._queue.append(Event('tick'))

        self.show()
                
            
    def complete(self, event:Event): 
        match event.name: 
            case 'tick': 
                print('Game is completed. Play again? (y/n)') 
                pinput = input('>') 
                match pinput: 
                    case 'y': 
                        self._board = Board()
                        self._current_state = self.in_progress
                        self._queue.append(Event('tick'))
                    case 'n': 
                        self._queue.append(Event('exit'))
            case 'exit': 
                print('Exiting...')
                raise SystemExit

    def show(self): 
        print(self._board) 

    def update(self, event): 
        self._current_state(event)
        
    def run(self): 
        while self._queue: 
            event = self._queue.pop() 
            try: 
                self.update(event)
            except SystemExit: 
                break
            
        
    
    
g=Game()
g.run()
