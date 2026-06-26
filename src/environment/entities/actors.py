import random
from typing import Optional

from src.environment.utils import Position, Direction
from src.game_options import MobMovePattern

from .colours import EntityColours
from .entity import DefeatableMixin, Entity


class MovableEntity(Entity):
    """An entity with methods to move position"""

    def move_in_direction(self, dir: Direction) -> None:
        self.position = self.position.moved_by(dir.value)

    def move_to(self, position: Position) -> None:
        self.position = position


class Player(DefeatableMixin, MovableEntity):
    def __init__(self, position: Position):
        super().__init__(position)


"""class Mob(DefeatableMixin, MovableEntity):
    def __init__(
        self,
        position: Position,
        pattern: MobMovePattern | str = MobMovePattern.RANDOM,
        path: Optional[list[Position]] = None,
    ):
        super().__init__(
            position,
            colour=EntityColours.MOB_RED,
            name="Mob",
            render_char="M",
        )
        self.pattern = pattern
        self.path = path or []
        self.path_index = 0

    def next_move(self, grid_width: int, grid_height: int) -> Position:
        if self.pattern not in (MobMovePattern.RANDOM, MobMovePattern.RANDOM.value):
            if self.path:
                target = self.path[self.path_index]
                self.path_index = (self.path_index + 1) % len(self.path)
                if is_within_bounds(target, grid_width, grid_height):
                    return target

        return self.random_move(grid_width, grid_height)

    def random_move(self, grid_width: int, grid_height: int) -> Position:
        neighbor_cells = neighbors(self.position, grid_width, grid_height)
        free_positions = [
            pos
            for pos in neighbor_cells
            if is_within_bounds(pos, grid_width, grid_height)
        ]
        return random.choice(free_positions) if free_positions else self.position
"""
