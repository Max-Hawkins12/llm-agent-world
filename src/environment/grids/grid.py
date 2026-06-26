from typing import Optional

from src.environment.entities import Entity, BackgroundEntity, Tile, Wall, Goal
from src.environment.utils import Position, Direction


class Grid:
    """Base class for grid-based environments."""

    def __init__(
        self,
        width: int,
        height: int,
        player_start_pos: Position = Position(0, 0),
        fill_with_walls: bool = False,
    ):
        if width < 1 or height < 1:
            raise ValueError("Grid width and height must both be at least 1")

        self.grid_width = width
        self.grid_height = height

        self.grid: list[list[BackgroundEntity]] = [
            [
                self._create_cell(Position(x, y), fill_with_walls)
                for x in range(self.grid_width)
            ]
            for y in range(self.grid_height)
        ]

        self.player_pos = player_start_pos
        self.entities: list[Entity] = []

    @property  # TODO Add type checking
    def goal(self) -> Goal:
        return self.grid[self.goal_pos.y][self.goal_pos.x] if self.goal_pos else None  # type: ignore[return-value]

    # Methods used in grid creation

    def _create_cell(self, pos: Position, is_wall: bool) -> BackgroundEntity:
        entity_class = Wall if is_wall else Tile
        return entity_class(pos)

    def _make_cell_a_tile(self, pos: Position) -> None:
        self.grid[pos.y][pos.x] = Tile(pos)

    def _make_cell_a_wall(self, pos: Position) -> None:
        self.grid[pos.y][pos.x] = Wall(pos)

    def _place_goal(self, pos: Position, is_locked: bool) -> None:
        self.goal_pos: Position = pos
        self.grid[pos.y][pos.x] = Goal(pos, is_locked)

    def _all_positions(self) -> list[Position]:
        return [
            Position(x, y)
            for y in range(self.grid_height)
            for x in range(self.grid_width)
        ]

    def neighbors(self, pos: Position) -> list[Position]:
        return [
            neighbor
            for direction in Direction
            if self.is_within_bounds(neighbor := pos.moved_by(direction.value))
        ]

    # Public methods to be used during game

    def is_within_bounds(self, pos: Position) -> bool:
        return 0 <= pos.x < self.grid_width and 0 <= pos.y < self.grid_height

    def is_wall(self, pos: Position) -> bool:
        return isinstance(self.grid[pos.y][pos.x], Wall)

    def is_passable(self, pos: Position) -> bool:
        return self.grid[pos.y][pos.x].is_passable

    def next_game_step(self):
        pass

    def get_tile_positions(self) -> list[Position]:
        return [pos for pos in self._all_positions() if not self.is_wall(pos)]

    def get_wall_positions(self) -> list[Position]:
        return [pos for pos in self._all_positions() if self.is_wall(pos)]
