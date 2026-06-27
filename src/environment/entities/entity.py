from typing import TYPE_CHECKING

from src.environment.utils import Direction, Position

if TYPE_CHECKING:
    from src.environment.grids import Grid


class Entity:
    """Base object with a position in the world."""

    blocks_movement = True

    def __init__(self, pos: Position, name: str):
        self.pos = pos
        self.name = name
        self.alive = True

    @property
    def position(self) -> Position:
        return self.pos

    @position.setter
    def position(self, pos: Position) -> None:
        self.pos = pos

    @property
    def is_passable(self) -> bool:
        return not self.blocks_movement

    def defeat(self) -> bool:
        return False

    def interact(self, grid: "Grid", actor: "Actor") -> None:
        pass

    def update(self, grid: "Grid") -> None:
        pass


class StaticEntity(Entity):
    """An entity that sits on top of a background cell."""

    blocks_movement = False

    def __init__(self, pos: Position, name: str, uses: int = 1):
        super().__init__(pos, name)
        self.remaining_uses = uses
        self.is_held = False

    def pick_up(self, actor: "Actor") -> bool:
        self.is_held = True
        return True

    def use_on(self, target: Entity) -> bool:
        return False

    def spend_use(self) -> None:
        self.remaining_uses -= 1
        if self.remaining_uses <= 0:
            self.alive = False
            self.is_held = False


class Actor(Entity):
    """An entity that can move and take turns in the world."""

    blocks_movement = True

    def move_in_direction(self, direction: Direction) -> None:
        self.pos = self.pos.moved_by(direction.value)

    def move_to(self, pos: Position) -> None:
        self.pos = pos

    def defeat(self) -> bool:
        self.alive = False
        return True

    def next_move(self, grid: "Grid") -> Position | None:
        return None

    def update(self, grid: "Grid") -> None:
        pass
