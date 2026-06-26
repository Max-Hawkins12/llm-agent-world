from typing import Optional

from src.environment.entities import BackgroundEntity, Tile, Wall
from src.environment.utils import Position, Direction


class Grid:
    """Base class for grid-based environments."""

    def __init__(
        self,
        width: int,
        height: int,
        start_pos: Position = Position(0, 0),
        goal_pos: Optional[Position] = None,
        fill_with_walls: bool = False,
    ):
        if width < 1 or height < 1:
            raise ValueError("Grid width and height must both be at least 1")

        self.grid_width = width
        self.grid_height = height
        self.start_pos = start_pos
        self.goal_pos = goal_pos
        self.grid: list[list[BackgroundEntity]] = [
            [
                self._create_cell(Position(x, y), fill_with_walls)
                for x in range(self.grid_width)
            ]
            for y in range(self.grid_height)
        ]

    def _create_cell(self, position: Position, is_wall: bool) -> BackgroundEntity:
        entity_class = Wall if is_wall else Tile
        return entity_class(position)

    def _make_cell_a_tile(self, position: Position) -> None:
        self.grid[position.y][position.x] = Tile(position)

    def _make_cell_a_wall(self, position: Position) -> None:
        self.grid[position.y][position.x] = Wall(position)

    def _all_positions(self) -> list[Position]:
        return [
            Position(x, y)
            for y in range(self.grid_height)
            for x in range(self.grid_width)
        ]

    def neighbors(self, position: Position) -> list[Position]:
        return [
            neighbor
            for direction in Direction
            if self.is_within_bounds(neighbor := position.moved_by(direction.value))
        ]

    def is_within_bounds(self, position: Position) -> bool:
        return 0 <= position.x < self.grid_width and 0 <= position.y < self.grid_height

    def is_wall(self, position: Position) -> bool:
        return isinstance(self.grid[position.y][position.x], Wall)

    def is_passable(self, position: Position) -> bool:
        return self.grid[position.y][position.x].is_passable

    def get_tile_positions(self) -> list[Position]:
        return [
            position for position in self._all_positions() if not self.is_wall(position)
        ]

    def get_wall_positions(self) -> list[Position]:
        return [
            position for position in self._all_positions() if self.is_wall(position)
        ]

    def render_to_text(self) -> str:
        rows = []
        for y in range(self.grid_height):
            row = []
            for x in range(self.grid_width):
                position = Position(x, y)
                if position == self.start_pos:
                    row.append("S")
                elif position == self.goal_pos:
                    row.append("G")
                else:
                    row.append(self.grid[y][x].render_char)
            rows.append("".join(row))
        return "\n".join(rows)
