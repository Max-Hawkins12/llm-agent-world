from enum import Enum
from typing import Optional

from src.environment.utils import Direction


class GameAction(Enum):
    MOVE_UP = "move_up"
    MOVE_DOWN = "move_down"
    MOVE_LEFT = "move_left"
    MOVE_RIGHT = "move_right"

    PICK_UP = "pick_up"
    USE_UP = "use_up"
    USE_DOWN = "use_down"
    USE_LEFT = "use_left"
    USE_RIGHT = "use_right"

    QUIT = "quit"

    WAIT = "wait"  # Default action when no other action is selected, for Human Agents
    INVALID = "invalid"  # Used to keep track of any invalid actions made by the LLM

    @property
    def is_movement_action(self) -> bool:
        return self in (
            self.MOVE_UP,
            self.MOVE_DOWN,
            self.MOVE_LEFT,
            self.MOVE_RIGHT,
        )

    @property
    def is_use_action(self) -> bool:
        return self in (
            self.USE_UP,
            self.USE_DOWN,
            self.USE_LEFT,
            self.USE_RIGHT,
        )

    @property
    def direction(self) -> Optional[Direction]:
        if not (self.is_movement_action or self.is_use_action):
            return None

        direction_mapper = {
            GameAction.MOVE_UP: Direction.UP,
            GameAction.USE_UP: Direction.UP,
            GameAction.MOVE_DOWN: Direction.DOWN,
            GameAction.USE_DOWN: Direction.DOWN,
            GameAction.MOVE_LEFT: Direction.LEFT,
            GameAction.USE_LEFT: Direction.LEFT,
            GameAction.MOVE_RIGHT: Direction.RIGHT,
            GameAction.USE_RIGHT: Direction.RIGHT,
        }

        return direction_mapper[self]


class MenuAction(Enum):
    OPTION_UP = "option_up"
    OPTION_DOWN = "option_down"
    PREV_OPTION = "prev_option"
    NEXT_OPTION = "next_option"

    START = "start"
    QUIT = "quit"

    WAIT = "wait"  # Default action when no other action is selected
