import random
from typing import List, Optional, Tuple

from src.game_options import MobMovePattern
from src.environment.utils import is_within_bounds, neighbors
from src.ui.colours import UIColour


class GameEntity:
    def __init__(
        self,
        x: int,
        y: int,
        colour: UIColour,
        outline_colour: Optional[UIColour],
        label: str,
    ):
        self.x = x
        self.y = y
        self.colour = colour
        self.outline_colour = outline_colour
        self.label = label
        self.alive = True

    def position(self) -> Tuple[int, int]:
        return self.x, self.y

    def move_to(self, x: int, y: int) -> None:
        self.x = x
        self.y = y


class Weapon(GameEntity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, UIColour.WEAPON_YELLOW, None, "Weapon")


class Goal(GameEntity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, UIColour.GOAL_GREEN, UIColour.WHITE, "Goal")
        self.locked = True


class Agent(GameEntity):
    def __init__(self, x: int, y: int, has_weapon: bool = False):
        super().__init__(x, y, UIColour.AGENT_BLUE, UIColour.WEAPON_YELLOW, "Agent")
        self.has_weapon = has_weapon


class Mob(GameEntity):
    def __init__(
        self,
        x: int,
        y: int,
        pattern: MobMovePattern = MobMovePattern.RANDOM,
        path: Optional[List[Tuple[int, int]]] = None,
    ):
        super().__init__(x, y, UIColour.MOB_RED, None, "Mob")
        self.pattern = pattern
        self.path = path or []
        self.path_index = 0

    def next_move(self, grid_width: int, grid_height: int) -> Tuple[int, int]:
        if self.pattern != MobMovePattern.RANDOM and self.path:
            target = self.path[self.path_index]
            self.path_index = (self.path_index + 1) % len(self.path)
            if is_within_bounds(target[0], target[1], grid_width, grid_height):
                return target

        return self.random_move(grid_width, grid_height)

    def random_move(self, grid_width: int, grid_height: int) -> Tuple[int, int]:
        neighbor_cells = neighbors(self.x, self.y, grid_width, grid_height)
        free_positions = [
            pos
            for pos in neighbor_cells
            if is_within_bounds(pos[0], pos[1], grid_width, grid_height)
        ]
        return random.choice(free_positions) if free_positions else (self.x, self.y)
