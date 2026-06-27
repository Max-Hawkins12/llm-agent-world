from typing import TYPE_CHECKING, Optional

from src.environment.utils import Position

from .background import LockableBackgroundEntity
from .entity import Actor, Entity, StaticEntity

if TYPE_CHECKING:
    from src.environment.grids import Grid


class Key(StaticEntity):
    """A key that opens the door with the same key id."""

    def __init__(
        self,
        pos: Position,
        name: str = "",
        unlocks: Optional[LockableBackgroundEntity] = None,
    ):
        super().__init__(pos, name=f"Key_{name}")
        self.unlocks = unlocks

    def use_on(self, target: LockableBackgroundEntity) -> bool:
        if not target == self.unlocks:
            return False
        else:
            target.unlock()
            self.spend_use()
            return True


class Weapon(StaticEntity):
    def __init__(self, pos: Position):
        super().__init__(pos, name="Weapon")

    def use_on(self, target: Entity) -> bool:
        return False
