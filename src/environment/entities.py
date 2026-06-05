import random
from enum import Enum
from typing import List, Optional, Tuple

from src.environment.utils import is_within_bounds, neighbors
from src.ui.colours import UIColour


class MovePattern(Enum):
    RANDOM = "random"
    LOOP = "loop"


class GameEntity:
    def __init__(self, x: int, y: int, color: UIColour, label: str):
        self.x = x
        self.y = y
        self.color = color
        self.label = label
        self.alive = True

    def position(self) -> Tuple[int, int]:
        return self.x, self.y

    def move_to(self, x: int, y: int) -> None:
        self.x = x
        self.y = y


class Weapon(GameEntity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, UIColour.WEAPON_YELLOW, "Weapon")


class Goal(GameEntity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, UIColour.GOAL_GREEN, "Goal")
        self.locked = True


class Agent(GameEntity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, UIColour.AGENT_BLUE, "Agent")
        self.has_weapon = False


class Mob(GameEntity):
    def __init__(
        self,
        x: int,
        y: int,
        pattern: MovePattern = MovePattern.RANDOM,
        path: Optional[List[Tuple[int, int]]] = None,
    ):
        super().__init__(x, y, UIColour.MOB_RED, "Mob")
        self.pattern = pattern
        self.path = path or []
        self.path_index = 0

    def next_move(self) -> Tuple[int, int]:
        if self.pattern == MovePattern.LOOP and self.path:
            target = self.path[self.path_index]
            self.path_index = (self.path_index + 1) % len(self.path)
            return target

        return self.random_move()

    def random_move(self) -> Tuple[int, int]:
        neighbor_cells = neighbors(self.x, self.y)
        free_positions = [
            pos for pos in neighbor_cells if is_within_bounds(pos[0], pos[1])
        ]
        return random.choice(free_positions) if free_positions else (self.x, self.y)
