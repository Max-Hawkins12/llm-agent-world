import random
from collections import deque

from src.environment.entities.entity import MazeGoal, MazePlayer, MazeTile, MazeWall

from .grid import Grid, Position


class Maze(Grid):
    """Generate a maze using randomized DFS.

    This maze uses a fixed start at (0, 0). The goal is placed in the furthest
    reachable open cell from that start after the maze has been carved.
    """

    tile_entity_class = MazeTile
    wall_entity_class = MazeWall

    def __init__(self, width: int, height: int, seed: int | None = None):

        self._random = random.Random(seed)
        self.player: MazePlayer | None = None
        self.goal_entity: MazeGoal | None = None
        super().__init__(width, height, default_wall=True)

        self._generate_maze()

    def _generate_maze(self) -> None:
        self._carve_passage(*self.start)

        self.goal = self._place_goal_furthest_from_start()
        self.player = MazePlayer(*self.start)
        self.goal_entity = MazeGoal(*self.goal)

    def _carve_passage(self, x: int, y: int) -> None:
        self._open_cell(x, y)
        directions = self._random.sample(
            self.neighbors(x, y), len(self.neighbors(x, y))
        )

        for nx, ny in directions:
            if not self.is_wall(nx, ny):
                continue

            if self._count_open_neighbors(nx, ny) > 1:
                continue

            self._carve_passage(nx, ny)

    def _place_goal_furthest_from_start(self) -> Position:
        queue = deque([self.start])
        distances = {self.start: 0}
        furthest: Position = self.start

        while queue:
            current = queue.popleft()
            current_distance = distances[current]

            if current_distance > distances[furthest]:
                furthest = current

            for neighbor in self.neighbors(*current):
                if neighbor in distances:
                    continue
                if self.is_wall(*neighbor):
                    continue

                distances[neighbor] = current_distance + 1
                queue.append(neighbor)

        return furthest

    def _count_open_neighbors(self, x: int, y: int) -> int:
        return sum(1 for nx, ny in self.neighbors(x, y) if not self.is_wall(nx, ny))
