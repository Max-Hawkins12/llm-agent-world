from src.environment.utils import Position

from .entity import Entity


class BackgroundEntity(Entity):
    """Static terrain that occupies a grid cell."""

    blocks_movement = False

    @property
    def is_passable(self) -> bool:
        return not self.blocks_movement


class Tile(BackgroundEntity):
    """A passable background cell."""

    blocks_movement = False

    def __init__(self, position: Position):
        super().__init__(position)


class Wall(BackgroundEntity):
    """An impassable background cell."""

    blocks_movement = True

    def __init__(self, position: Position):
        super().__init__(position)
