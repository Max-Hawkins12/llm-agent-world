from __future__ import annotations

from enum import Enum
from typing import NamedTuple


class Position(NamedTuple):
    x: int
    y: int

    def moved_by(self, offset: Position) -> Position:
        return Position(self.x + offset.x, self.y + offset.y)


class Direction(Enum):
    UP = Position(0, -1)
    RIGHT = Position(1, 0)
    DOWN = Position(0, 1)
    LEFT = Position(-1, 0)
