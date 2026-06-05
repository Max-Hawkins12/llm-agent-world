from enum import Enum


class Action(Enum):
    MOVE_UP = "move_up"
    MOVE_DOWN = "move_down"
    MOVE_LEFT = "move_left"
    MOVE_RIGHT = "move_right"
    WAIT = "wait"
    QUIT = "quit"

    INVALID = "invalid"
