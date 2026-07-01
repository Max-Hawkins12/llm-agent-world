from enum import Enum


class GameState(Enum):
    START_MENU = "start_menu"
    MENU = "start_menu"
    RUNNING = "running"
    END_SCREEN = "end_screen"
    RESULTS = "results"

    QUIT = "quit"


class EndState(Enum):
    WIN = "win"
    TIMEOUT = "timeout"
    TOO_MANY_INVALIDS = "too_many_invalids"
    TOO_MANY_CONSECUTIVE_INVALIDS = "too_many_consecutive_invalids"
