from typing import List, Optional, Tuple

from src.environment.entities.entity import Entity, Tile, Wall

Position = Tuple[int, int]


class Grid:
    """Base class for grid-based environments."""

    tile_entity_class = Tile
    wall_entity_class = Wall

    def __init__(
        self,
        width: int,
        height: int,
        start: Position = (0, 0),
        goal: Optional[Position] = None,
        default_wall: bool = False,
    ):
        if width < 1 or height < 1:
            raise ValueError("Grid width and height must both be at least 1")

        self.grid_width = width
        self.grid_height = height
        self.start = start
        self.goal = goal
        self.grid: List[List[Entity]] = [
            [self._create_cell(x, y, default_wall) for x in range(self.grid_width)]
            for y in range(self.grid_height)
        ]

    def _create_cell(self, x: int, y: int, is_wall: bool) -> Entity:
        entity_class = self.wall_entity_class if is_wall else self.tile_entity_class
        return entity_class(x, y)

    def _open_cell(self, x: int, y: int) -> None:
        self.grid[y][x] = self.tile_entity_class(x, y)

    def _all_positions(self) -> List[Position]:
        return [(x, y) for y in range(self.grid_height) for x in range(self.grid_width)]

    def neighbors(self, x: int, y: int) -> List[Position]:
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        return [
            (nx, ny)
            for dx, dy in directions
            if self.is_within_bounds(nx := x + dx, ny := y + dy)
        ]

    def is_within_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.grid_width and 0 <= y < self.grid_height

    def is_wall(self, x: int, y: int) -> bool:
        return isinstance(self.grid[y][x], Wall)

    def is_passable(self, x: int, y: int) -> bool:
        return self.grid[y][x].is_passable

    def render_to_text(self) -> str:
        rows = []
        for y in range(self.grid_height):
            row = []
            for x in range(self.grid_width):
                if (x, y) == self.start:
                    row.append("S")
                elif (x, y) == self.goal:
                    row.append("G")
                else:
                    row.append(self.grid[y][x].render_char)
            rows.append("".join(row))
        return "\n".join(rows)

    def get_open_positions(self) -> List[Position]:
        return [(x, y) for x, y in self._all_positions() if not self.is_wall(x, y)]

    def get_wall_positions(self) -> List[Position]:
        return [(x, y) for x, y in self._all_positions() if self.is_wall(x, y)]
