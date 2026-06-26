import random
from collections import deque

from src.environment.utils import Position

from .grid import Grid


class Maze(Grid):
    """Generate a maze using randomized DFS.

    This maze uses a fixed start at (0, 0). The goal is placed in the furthest
    reachable open cell from that start.
    """

    def __init__(
        self,
        width: int,
        height: int,
        start_pos: Position = Position(0, 0),
        seed: int | None = None,
    ):
        super().__init__(width, height, start_pos=start_pos, fill_with_walls=True)

        self._random = random.Random(seed)
        self._generate_maze()

    def _generate_maze(self) -> None:
        self._make_passage(self.start_pos)

        self.goal_pos = self._place_goal_furthest_from_start()

    def _make_passage(self, position: Position) -> None:
        self._make_cell_a_tile(position)
        directions = self._random.sample(
            self.neighbors(position), len(self.neighbors(position))
        )

        for neighbor in directions:
            if not self.is_wall(neighbor) or self._count_open_neighbors(neighbor) > 1:
                continue

            self._make_passage(neighbor)

    def _place_goal_furthest_from_start(self) -> Position:
        queue = deque([self.start_pos])
        distances = {self.start_pos: 0}
        furthest: Position = self.start_pos

        while queue:
            current = queue.popleft()
            current_distance = distances[current]

            if current_distance > distances[furthest]:
                furthest = current

            for neighbor in self.neighbors(current):
                if neighbor in distances:
                    continue
                if self.is_wall(neighbor):
                    continue

                distances[neighbor] = current_distance + 1
                queue.append(neighbor)

        return furthest

    def _count_open_neighbors(self, position: Position) -> int:
        return sum(
            1 for neighbor in self.neighbors(position) if not self.is_wall(neighbor)
        )
