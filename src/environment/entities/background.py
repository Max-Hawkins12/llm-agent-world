from src.environment.utils import Position

from .entity import Entity, LockableMixin


class BackgroundEntity(Entity):
    """Static terrain that occupies a grid cell."""

    blocks_movement = False

    @property
    def is_passable(self) -> bool:
        return not self.blocks_movement


class Tile(BackgroundEntity):
    """A passable background cell."""

    blocks_movement = False

    def __init__(self, pos: Position):
        super().__init__(pos, name="Tile")


class Wall(BackgroundEntity):
    """An impassable background cell."""

    blocks_movement = True

    def __init__(self, pos: Position):
        super().__init__(pos, name="Wall")


class Goal(LockableMixin, BackgroundEntity):

    def __init__(self, pos: Position, is_locked: bool = False):
        super().__init__(pos=pos, name="Goal", is_locked=is_locked)
        self.blocks_movement = is_locked


class Door(LockableMixin, BackgroundEntity):
    """A door that blocks movement until unlocked."""

    def __init__(self, pos: Position, key_id: int, is_locked: bool = True):
        super().__init__(pos=pos, name=f"Door_{key_id}", is_locked=is_locked)
        self.key_id = key_id
        self.blocks_movement = is_locked
