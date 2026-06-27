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
        player_start_pos: Position = Position(0, 0),
        seed: int | None = None,
    ):
        super().__init__(
            width,
            height,
            player_start_pos=player_start_pos,
            fill_with_walls=True,
        )

        self._random = random.Random(seed)
        self._generate_maze(player_start_pos)

    def _generate_maze(self, start_pos: Position) -> None:
        self._make_passage(start_pos)
        self._place_goal_furthest_from_start(start_pos)

    def _make_passage(self, pos: Position) -> None:
        self._place_tile(pos)
        directions = self._random.sample(self.neighbors(pos), len(self.neighbors(pos)))

        for neighbor in directions:
            if not self.is_wall(neighbor) or self._count_open_neighbors(neighbor) > 1:
                continue

            self._make_passage(neighbor)

    def _place_goal_furthest_from_start(self, start_pos: Position) -> None:
        queue = deque([start_pos])
        distances = {start_pos: 0}
        furthest: Position = start_pos

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

        self._place_goal(furthest, is_locked=False)

    def _count_open_neighbors(self, pos: Position) -> int:
        return sum(1 for neighbor in self.neighbors(pos) if not self.is_wall(neighbor))
