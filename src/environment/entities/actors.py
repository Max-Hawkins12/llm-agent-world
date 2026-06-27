import random
from typing import TYPE_CHECKING

from src.environment.utils import Position

from .entity import Actor, StaticEntity

if TYPE_CHECKING:
    from src.environment.grids import Grid


class Player(Actor):
    """The player-controlled actor."""

    def __init__(self, pos: Position):
        super().__init__(pos, name="Player")
        self.held_item: StaticEntity | None = None

    def update(self, grid: "Grid") -> None:
        pass


class Mob(Actor):
    def __init__(self, pos: Position, mob_id: int):
        super().__init__(pos, name=f"Mob_{mob_id}")
        self.id = mob_id

    def next_move(self, grid: "Grid") -> Position | None:
        candidates = grid.valid_actor_moves(self)

        if not candidates:
            return None

        return random.choice(candidates)


MovableEntity = Actor
