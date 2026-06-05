from typing import List, Tuple

from src.constants import GRID_HEIGHT, GRID_WIDTH


def is_within_bounds(x: int, y: int) -> bool:
    return 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT


def neighbors(x: int, y: int) -> List[Tuple[int, int]]:
    options = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    return [(cx, cy) for cx, cy in options if is_within_bounds(cx, cy)]
