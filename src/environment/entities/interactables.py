from src.environment.utils import Position

from .colours import EntityColours
from .entity import Entity, InteractableMixin


class GoalEntity(InteractableMixin, Entity):
    def __init__(self, position: Position):
        super().__init__(position)
        self.locked = True


class Door(Entity):
    """A door that blocks movement until unlocked."""

    def __init__(self, position: Position, key_id: int):
        super().__init__(
            position,
            colour=EntityColours.WALL_GREY,
            name=f"Door {key_id}",
            render_char="D",
        )
        self.key_id = key_id
        self.locked = True

    @property
    def is_passable(self) -> bool:
        return not self.locked

    def unlock(self) -> None:
        self.locked = False
        self.render_char = "/"


class Key(InteractableMixin, Entity):
    """A key that opens the door with the same key id."""

    def __init__(self, position: Position, key_id: int):
        super().__init__(
            position,
            colour=EntityColours.WEAPON_YELLOW,
            name=f"Key {key_id}",
            render_char="K",
        )
        self.key_id = key_id

    @property
    def is_passable(self) -> bool:
        return True


class Weapon(Entity):
    def __init__(self, position: Position):
        super().__init__(
            position,
            colour=EntityColours.WEAPON_YELLOW,
            name="Weapon",
            render_char="W",
        )


Goal = GoalEntity
