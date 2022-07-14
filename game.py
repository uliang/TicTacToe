from board import Board 
import dataclasses 
from collections import namedtuple 
from board import InvalidMove
from importlib import import_module 
import argparse as arg 



Event = namedtuple('Event', ['name', 'payload'], defaults=[None, None])


@dataclasses.dataclass 
class Game: 
    _board: Board 
    _msg: str = dataclasses.field(init=False, default='')
    
    def __post_init__(self): 
        self._queue =  [Event('init')]
        self._current_state = self.startup 

    def startup(self, event): 
        match event.name: 
            case 'player_input': 
                kp=event.payload.get('keypressed', '')
                if kp == 'c': 
                    return self.player1
                elif kp in 'qQxX': 
                    raise SystemExit
            
            case 'init': 
                self._msg = 'Welcome. Press (c) to continue or (q) to exit.'
                return 'HANDLED'

    def player1(self, event): 
        match event.name: 
            case 'player_input': 

                move = event.payload.get('keypressed') 
                if move in 'qQxX': 
                    raise SystemExit

                if move: 
                    try: 
                        move = int(move) 
                        self._board = self._board.make_move(move)
                        if self._board.check_win_condition(): 
                            self._queue.append(Event('winner', {'player': self._board.value}))
                            return self.complete
                        elif self._board.check_terminal_state(): 
                            self._queue.append(Event('draw'))
                            return self.complete
                    except InvalidMove: 
                        self._msg = 'Invalid input. Try again\n'
                        self._player_message()
                        return 'HANDLED'
                    else: 
                        return self.player2

            case 'on_entry': 
                self._msg = 'Player 1 turn.\n'
                self._player_message()
                return 'HANDLED'

            case 'on_exit': 
                self._msg = ''

    def player2(self, event): 
        match event.name: 
            case 'player_input': 

                move = event.payload.get('keypressed') 
                if move in 'qQxX': 
                    raise SystemExit

                if move: 
                    try: 
                        move = int(move) 
                        self._board = self._board.make_move(move)
                        if self._board.check_win_condition(): 
                            self._queue.append(Event('winner', {'player': self._board.value}))
                            return self.complete
                        elif self._board.check_terminal_state(): 
                            self._queue.append(Event('draw'))
                            return self.complete
                    except InvalidMove: 
                        self._msg = 'Invalid input. Try again\n'
                        self._player_message()
                        return 'HANDLED'
                    else: 
                        return self.player1

            case 'on_entry': 
                self._msg = 'Player 2 turn.\n'
                self._player_message()
                return 'HANDLED'
            case 'on_exit': 
                self._msg = ''

    def _player_message(self): 
        self._msg += str(self._board) + '\n'

        moveset = ','.join([str(m) for m in self._board.generate_moveset()])
        self._msg += 'Enter move. Available moves are: {}\n'.format(moveset)

    def complete(self, event): 
        match event.name: 
            case 'winner': 
                winning_player = event.payload.get('player')
                winning_player = 1 if winning_player == 1 else 2
                self._msg = f'Player {winning_player} has won\n'
                self._msg += 'Continue? Press (c) to continue or (q) to quit.'
                return 'HANDLED'
            
            case 'player_input': 
                if (kp:=event.payload.get('keypressed', '')) == 'c': 
                    return self.player1
                elif kp in 'qQxX': 
                    raise SystemExit

            case 'draw':
                self._msg = 'Game is drawn.'
                self._msg += 'Continue? Press (c) to continue or (q) to quit.'
                return 'HANDLED'

            case 'on_entry': 
                self._board.reset()

    def update(self, event):     
        state = self._current_state(event)
        if state == 'HANDLED':
            return
        self._current_state(Event('on_exit'))
        self._current_state = state 
        self._current_state(Event('on_entry'))

    def show(self): 
        print(self._msg)

    def get_input(self): 
        r = input('>') 
        e = Event('player_input', {'keypressed': r})
        self._queue.append(e)

    def run(self): 
        while True: 
            try: 
                while self._queue: 
                    event = self._queue.pop()
                    self.update(event)
            except SystemExit: 
                break
            self.show()
            self.get_input()

            
if __name__ == '__main__' : 
    parser = arg.ArgumentParser() 
    parser.add_argument('game', help='Name of the game class specified in the board.py module')
    args = parser.parse_args() 

    mod = import_module('board')
    board_factory = getattr(mod, args.game)
    board = board_factory()

    g = Game(board)
    g.run()
