from typing import List, Tuple


def is_within_bounds(x: int, y: int, grid_width: int, grid_height: int) -> bool:
    return 0 <= x < grid_width and 0 <= y < grid_height


def neighbors(
    x: int, y: int, grid_width: int, grid_height: int
) -> List[Tuple[int, int]]:
    options = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    return [
        (cx, cy)
        for cx, cy in options
        if is_within_bounds(cx, cy, grid_width, grid_height)
    ]
