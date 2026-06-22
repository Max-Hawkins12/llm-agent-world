from enum import Enum
from typing import Optional, Tuple

from .colours import EntityColours


class Entity:
    def __init__(
        self,
        x: int,
        y: int,
        colour: Optional[EntityColours] = None,
        name: Optional[str] = None,
        render_char: str = "?",
    ):
        self.x = x
        self.y = y
        self.colour = colour
        self.name = name or self.__class__.__name__
        self.render_char = render_char

    def position(self) -> Tuple[int, int]:
        return self.x, self.y


class BackgroundEntity(Entity):
    """Static terrain that occupies a grid cell."""

    blocks_movement = False

    @property
    def is_passable(self) -> bool:
        return not self.blocks_movement


class Tile(BackgroundEntity):
    """A passable background cell."""

    blocks_movement = False

    def __init__(self, x: int, y: int):
        super().__init__(
            x,
            y,
            colour=EntityColours.TILE_GREY,
            name="Tile",
            render_char=".",
        )


class Wall(BackgroundEntity):
    """An impassable background cell."""

    blocks_movement = True

    def __init__(self, x: int, y: int):
        super().__init__(
            x,
            y,
            colour=EntityColours.WALL_GREY,
            name="Wall",
            render_char="#",
        )


class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


class MovableEntity(Entity):
    def move_in_direction(self, dir: Direction):
        x, y = dir.value

        self.x += x
        self.y += y


class InteractableMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.interacted = False

    def interact_with(self):
        self.interacted = not self.interacted


class DefeatableMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.alive = True

    def defeat(self):
        self.alive = False


class GoalEntity(InteractableMixin, Entity):
    def __init__(self, x: int, y: int):
        super().__init__(
            x,
            y,
            colour=EntityColours.GOAL_GREEN,
            name="Goal",
            render_char="G",
        )


class PlayerEntity(DefeatableMixin, MovableEntity):
    def __init__(self, x: int, y: int):
        super().__init__(
            x,
            y,
            colour=EntityColours.AGENT_BLUE,
            name="Player",
            render_char="P",
        )


class MazeTile(Tile):
    """Passable terrain for maze grids."""


class MazeWall(Wall):
    """Blocking terrain for maze grids."""


class MazePlayer(PlayerEntity):
    """The controllable player entity for maze grids."""


class MazeGoal(GoalEntity):
    """The target entity for maze grids."""


# Friendly generic aliases for the current maze-only game.
Player = MazePlayer
Goal = MazeGoal
