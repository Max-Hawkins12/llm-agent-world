from src.environment.utils import Position

from .entity import Entity


class BackgroundEntity(Entity):
    """Static terrain that occupies a grid cell."""

    blocks_movement = False


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


class LockableBackgroundEntity(BackgroundEntity):
    """Background terrain that can toggle whether it blocks movement."""

    def __init__(self, pos: Position, name: str, is_locked: bool = False):
        super().__init__(pos=pos, name=name)
        self.is_locked = is_locked
        self.blocks_movement = is_locked

    def lock(self) -> None:
        self.is_locked = True
        self.blocks_movement = True

    def unlock(self) -> None:
        self.is_locked = False
        self.blocks_movement = False


class Goal(LockableBackgroundEntity):
    def __init__(self, pos: Position, is_locked: bool = False):
        super().__init__(pos=pos, name="Goal", is_locked=is_locked)


class Door(LockableBackgroundEntity):
    """A door that blocks movement until unlocked."""

    def __init__(self, pos: Position, name: str, is_locked: bool = True):
        super().__init__(pos=pos, name=f"Door_{name}", is_locked=is_locked)
