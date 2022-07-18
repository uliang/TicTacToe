from ast import operator
from board import Board, InvalidMove
import dataclasses
from collections import namedtuple
from importlib import import_module
import argparse as arg
import enum
from collections import deque
import abc
from alphabeta import alphabetapruning
import operator


Event = namedtuple("Event", ["name", "payload"], defaults=[None, None])
Trans = namedtuple("Trans", ["target", "action"], defaults=[None, None])
Super = namedtuple("Super", ["target"], defaults=[None])


class GS(enum.Enum):
    HANDLED = 1
    UNHANDLED = 2
    SUPER = 3
    INITIAL = 4
    QUIT = 5
    ENTRY = 6
    EXIT = 7


class InvalidInput(Exception):
    ...


class StateMachine(abc.ABC):
    def __init__(self, *args, **kwargs):
        self._current_state = None
        self._queue = []

    def update(self, event):
        exit_stack = deque([self._current_state])
        head = self._current_state

        if event is GS.INITIAL:
            while (transition := head(GS.INITIAL)) is not None:
                head = transition.target
                head(GS.ENTRY)
            self._current_state = head
            return

        while (transition := head(event)) is None:
            handle_by_parent = head(GS.SUPER)
            if handle_by_parent is None:
                return
            head = handle_by_parent.target
            exit_stack.append(head)

        if transition is GS.HANDLED:
            return

        source = head
        target = transition.target
        head = target
        entry_stack = deque([head])

        while (transition := head(GS.INITIAL)) is not None:
            head = transition.target
            entry_stack.append(head)

        exit_path = []
        head = source
        while (state := head(GS.SUPER).target) != self.root:
            # print(state)
            head = state
            exit_path.insert(0, state)

        entry_path = []
        head = target
        # print(target)
        while (state := head(GS.SUPER).target) != self.root:
            # print(state)
            head = state
            entry_path.insert(0, state)

        lca_index = 0
        for depth, (ex_state, en_state) in enumerate(zip(exit_path, entry_path)):
            if ex_state != en_state:
                lca_index = depth - 1
                break

        for state in exit_path[-1:lca_index:-1]:
            exit_stack.append(state)

        for state in entry_path[-1:lca_index:-1]:
            entry_stack.appendleft(state)

        for state in exit_stack:
            state(GS.EXIT)

        if (action := source(event).action) is not None:
            action()

        for state in entry_stack:
            state(GS.ENTRY)

        self._current_state = state

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

    @abc.abstractmethod
    def show(self):
        ...

    @abc.abstractmethod
    def get_input(self):
        ...


@dataclasses.dataclass
class Game(StateMachine):
    _board: Board
    _with_ai: bool = False
    _msg: str = dataclasses.field(init=False, default="")

    def __post_init__(self):
        self._queue = [GS.INITIAL]
        self._current_state = self.root

    def root(self, event):
        match event:
            case GS.INITIAL:
                return Trans(self.active)

    def active(self, event):
        match event:
            case GS.INITIAL:
                return Trans(self.init)

            case GS.QUIT:
                raise SystemExit

            case GS.SUPER:
                return Super(self.root)

    def init(self, event):
        match event:
            case GS.ENTRY:
                self._msg = "Welcome. Press (c) to continue or (q) to exit."
                return GS.HANDLED

            case Event("continue"):
                return Trans(self.player1)

            case GS.SUPER:
                return Super(self.active)

    def playing(self, event):
        match event:
            case GS.INITIAL:
                return Trans(self.player1)

            case Event("win", payload={"value": p}):

                def action():
                    winning_player = 1 if p == 1 else 2
                    self._msg = f"Player {winning_player} has won\n"
                    self._msg += str(self._board) + "\n"
                    self._msg += "Continue? Press (c) to continue or (q) to quit."

                return Trans(self.complete, action)

            case Event("draw"):

                def action():
                    self._msg = "Game is drawn.\n"
                    self._msg += str(self._board) + "\n"
                    self._msg += "Continue? Press (c) to continue or (q) to quit."

                return Trans(self.complete, action)

            case Event("player_input", payload={"move": m}):
                try:
                    self._board = self._board.make_move(m)
                except InvalidMove:
                    self._msg = "Invalid move. Please key in move again"
                    return GS.HANDLED
                self._queue.append(Event("check_victory"))
                return GS.HANDLED

            case Event("check_victory"):
                if self._board.check_win_condition():
                    self._queue.append(Event("win", {"value": self._board.value}))
                    return GS.HANDLED
                elif self._board.check_terminal_state():
                    self._queue.append(Event("draw"))
                    return GS.HANDLED
                else:
                    self._queue.append(Event("next_player"))
                    return GS.HANDLED

            case GS.SUPER:
                return Super(self.active)

    def player1(self, event):
        match event:
            case Event("next_player"):
                return Trans(self.player2)

            case GS.ENTRY:
                self._msg = "Player 1 turn.\n"
                self._player_message()
                return GS.HANDLED

            case GS.SUPER:
                return Super(self.playing)

    def player2(self, event):
        match event:
            case Event("next_player"):
                return Trans(self.player1)

            case GS.ENTRY:
                self._msg = "Player 2 turn.\n"
                self._player_message()
                if self._with_ai:
                    move, _ = min(
                        [
                            (
                                move,
                                alphabetapruning(
                                    self._board.make_move(move), shouldmax=True
                                ),
                            )
                            for move in self._board.generate_moveset()
                        ],
                        key=operator.itemgetter(1),
                    )
                    self._queue.append(Event("player_input", payload={"move": move}))
                return GS.HANDLED

            case GS.SUPER:
                return Super(self.playing)

    def complete(self, event):
        match event:
            case Event("continue"):

                def action():
                    self._board = self._board.reset()

                return Trans(self.playing, action)

            case GS.SUPER:
                return Super(self.active)

    def _player_message(self):
        self._msg += str(self._board) + "\n"

        moveset = ",".join([str(m) for m in self._board.generate_moveset()])
        self._msg += "Enter move. Available moves are: {}\n".format(moveset)

    def show(self):
        print(self._msg)
        self._msg = ""

    def get_input(self):
        r = input(">")
        try:
            self.handle_input(r)
        except InvalidInput:
            self._msg = "Invalid input recived"

    def handle_input(self, keypressed):
        match keypressed:
            case "x" | "X" | "q" | "Q":
                self._queue.append(GS.QUIT)
            case "c":
                self._queue.append(Event("continue"))
            case keypressed if keypressed.isdigit():
                self._queue.append(Event("player_input", {"move": int(keypressed)}))
            case _:
                raise InvalidInput


if __name__ == "__main__":
    parser = arg.ArgumentParser()
    parser.add_argument(
        "game", help="Name of the game class specified in the board.py module"
    )
    parser.add_argument(
        "-ai",
        "--toggle-AI",
        action="store_true",
        help="Player 2 is controlled by the AI",
        dest="ai",
    )
    args = parser.parse_args()

    mod = import_module("board")
    board_factory = getattr(mod, args.game)
    board = board_factory()

    with_ai = args.ai
    g = Game(board, with_ai)
    g.run()
