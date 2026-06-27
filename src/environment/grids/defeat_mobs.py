import random
from typing import List

from src.environment.entities import Mob
from src.environment.utils import Position

from . import Grid


class DefeatMobs(Grid):
    """A grid where mobs are placed randomly and the goal remains locked until they are defeated."""

    def __init__(
        self,
        width: int,
        height: int,
        seed: int | None = None,
        mob_count: int = 1,
    ):
        self._random = random.Random(seed)
        self.mobs: list[Mob] = []

        self._validate_grid_size(width, height, mob_count)
        super().__init__(width, height)

        self.player_pos = self._random_position(avoid=[])
        self.goal_pos = self._random_position(avoid=[self.player_pos])
        self._place_goal(self.goal_pos, is_locked=True)

        self._place_mobs(mob_count)

    def _validate_grid_size(self, width: int, height: int, mob_count: int) -> None:
        if width < 1 or height < 1:
            raise ValueError("DefeatMobs width and height must be at least 1")

        max_mobs = width * height - 2
        if mob_count < 1:
            raise ValueError("DefeatMobs must have at least one mob")
        if mob_count > max_mobs:
            raise ValueError(
                f"DefeatMobs grid of size {width}x{height} can place at most {max_mobs} mobs"
            )

    def _place_mobs(self, mob_count: int) -> None:
        occupied = [self.player_pos, self.goal_pos]

        for mob_id in range(1, mob_count + 1):
            position = self._random_position(avoid=occupied)
            mob = Mob(position, mob_id)
            self._add_actor(mob)
            self.mobs.append(mob)
            occupied.append(position)

    def _random_position(self, avoid: List[Position]) -> Position:
        candidates = [pos for pos in self._get_passable_positions() if pos not in avoid]
        if not candidates:
            raise ValueError("No available positions for DefeatMobs placement")

        return self._random.choice(candidates)

    def get_mob_at(self, position: Position) -> Mob | None:
        for mob in self.mobs:
            if mob.alive and mob.pos == position:
                return mob
        return None

    def total_alive_mobs(self) -> int:
        return sum(1 for mob in self.mobs if mob.alive)

    def update_goal_lock(self) -> None:
        if self.total_alive_mobs() == 0:
            self.goal.unlock()

    def update(self) -> None:
        self.update_goal_lock()
