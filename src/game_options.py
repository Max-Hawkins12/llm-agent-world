from enum import Enum
from dataclasses import dataclass


class EntityPlacement(Enum):
    FIXED = "fixed"
    RANDOM = "random"


class MobMovePattern(Enum):
    RANDOM = "random"
    LINEAR = "linear"


class GameOptions:
    GRID_SIZE_OPTIONS = [(8, 8), (10, 10), (12, 12)]
    ENTITY_PLACEMENT_OPTIONS = [e.value for e in EntityPlacement]
    AGENT_START_WITH_WEAPON = [False, True]

    MOB_COUNT_OPTIONS = [i for i in range(0, 5)]
    MOB_MOVE_PATTERNS = [e.value for e in MobMovePattern]


@dataclass
class GameSettings:
    grid_size: tuple[int, int]
    entity_placement: EntityPlacement
    has_weapon: bool
    mob_count: int
    mob_move_pattern: MobMovePattern


DEFAULT_GAME_SETTINGS = GameSettings(
    grid_size=(8, 8),
    entity_placement=EntityPlacement.FIXED,
    has_weapon=False,
    mob_count=2,
    mob_move_pattern=MobMovePattern.RANDOM,
)
