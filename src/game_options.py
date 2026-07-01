from enum import Enum


class GridType(Enum):
    DEFEAT_MOBS = "defeat_mobs"
    MAZE = "maze"
    LOCKED_DOORS = "locked_doors"

    @property
    def display_name(self) -> str:
        names = {
            GridType.DEFEAT_MOBS: "Defeat Mobs",
            GridType.MAZE: "Maze",
            GridType.LOCKED_DOORS: "Locked Doors",
        }
        return names[self]


class MobPlacement(Enum):
    FIXED = "fixed"
    RANDOM = "random"


class MobMovePattern(Enum):
    RANDOM = "random"
    LINEAR = "linear"


class AgentType(Enum):
    HUMAN = "human"
    LLM_OBJECTIVE = "llm_objective_oriented"

    @property
    def display_name(self) -> str:
        names = {
            AgentType.HUMAN: "Human",
            AgentType.LLM_OBJECTIVE: "LLM - Objective Oriented",
        }
        return names[self]


class GameOptions:
    """
    Stores the options the user can currently change about the game, and their allowed values.
    """

    GRID_TYPE = [e for e in GridType]
    AGENT_TYPE = [e for e in AgentType]
    GRID_SIZE_OPTIONS = [(8, 8), (10, 10), (12, 12), (16, 12), (20, 20)]
    RUN_COUNT_OPTIONS = [1, 3, 5, 10]
    SECTION_COUNT_OPTIONS = [2, 3, 4, 5]
    MOB_PLACEMENT_OPTIONS = [e.value for e in MobPlacement]
    MOB_COUNT_OPTIONS = [i for i in range(1, 5)]
    MOB_MOVE_PATTERNS = [e.value for e in MobMovePattern]


class GameSettings:
    """
    Represens settings that we can or might want to change about the game.
    A GameSettings created with no parameters will have the default settings
    """

    grid_size: tuple[int, int]
    mob_placement: MobPlacement
    has_weapon: bool
    mob_count: int
    mob_move_pattern: MobMovePattern

    def __init__(
        self,
        grid_size: tuple[int, int] = (8, 8),
        mob_placement: MobPlacement = MobPlacement.FIXED,
        has_weapon: bool = False,
        mob_count: int = 3,
        mob_move_pattern: MobMovePattern = MobMovePattern.RANDOM,
    ):
        self.grid_size = grid_size
        self.mob_placement = mob_placement
        self.has_weapon = has_weapon
        self.mob_count = mob_count
        self.mob_move_pattern = mob_move_pattern
