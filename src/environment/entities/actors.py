import random
from typing import Optional

from src.environment.utils import Position, Direction
from src.game_options import MobMovePattern

from .entity import DefeatableMixin, Entity


class MovableEntity(Entity):
    """An entity with methods to move pos"""

    def move_in_direction(self, dir: Direction) -> None:
        self.pos = self.pos.moved_by(dir.value)

    def move_to(self, pos: Position) -> None:
        self.pos = pos


class Player(DefeatableMixin, MovableEntity):
    def __init__(self, pos: Position):
        super().__init__(pos, name="Player")


class Mob(DefeatableMixin, MovableEntity):
    def __init__(self, pos: Position, mob_id: int):
        super().__init__(pos, name=f"Mob_{mob_id}")
        self.id = mob_id

    def next_move(self) -> Position:
        return Position(0, 0)  # TODO implement mob movements
