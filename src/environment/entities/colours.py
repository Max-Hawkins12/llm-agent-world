from enum import Enum


class EntityColours(Enum):

    TILE_GREY = (180, 180, 180)
    WALL_GREY = (60, 60, 60)

    AGENT_BLUE = (0, 0, 255)
    MOB_RED = (255, 0, 0)

    WEAPON_YELLOW = (255, 255, 0)
    GOAL_GREEN = (0, 255, 0)


# Backwards-compatible alias for the original misspelling.
EnitityColours = EntityColours
