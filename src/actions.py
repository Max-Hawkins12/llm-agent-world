from enum import Enum


class GameAction(Enum):
    MOVE_UP = "move_up"
    MOVE_DOWN = "move_down"
    MOVE_LEFT = "move_left"
    MOVE_RIGHT = "move_right"

    QUIT = "quit"

    WAIT = "wait"  # Default action when no other action is selected
    INVALID = "invalid"  # TODO: Use when LLM generates an invalid action


class MenuAction(Enum):
    OPTION_UP = "option_up"
    OPTION_DOWN = "option_down"
    PREV_OPTION = "prev_option"
    NEXT_OPTION = "next_option"

    START = "start"
    QUIT = "quit"

    WAIT = "wait"  # Default action when no other action is selected
