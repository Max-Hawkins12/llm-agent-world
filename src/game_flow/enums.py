from enum import Enum


class GameState(Enum):
    MENU = "menu"
    RUNNING = "running"
    END_SCREEN = "finished"

    QUIT = "quit"


class EndState(Enum):
    WIN = "win"
    TIMEOUT = "timeout"
    TOO_MANY_INVALIDS = "too_many_invalids"
    TOO_MANY_CONSECUTIVE_INVALIDS = "too_many_consecutive_invalids"
