from src.environment.utils import Position

from .entity import Entity, InteractableMixin


class Key(InteractableMixin, Entity):
    """A key that opens the door with the same key id."""

    def __init__(self, pos: Position, key_id: int):
        super().__init__(pos, name=f"Key_{key_id}")
        self.key_id = key_id

    @property
    def is_passable(self) -> bool:
        return True


class Weapon(Entity):
    def __init__(self, pos: Position):
        super().__init__(pos, name="Weapon")
