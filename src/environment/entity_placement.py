import random
from typing import List, Optional, Tuple

from src.game_options import GameSettings, MobPlacement, MobMovePattern
from src.environment.entities import Weapon, Goal, Agent, Mob


def place_entities(
    settings: GameSettings,
) -> Tuple[Agent, Goal, Optional[Weapon], Optional[List[Mob]]]:
    """
    The agent is always at (0,0)
    The goal is always at (width - 1, height - 1)
    The weapon is either at (1, height - 3) or placed randomly
    Mobs are either at:
    - mob 1: (width - 2, 3)
    - mob 2: (5, height - 3)
    - mob 3: (width - 4, 1)
    - mob 4: (1, height - 6)
    Or placed randomly
    """
    if settings.mob_placement == MobPlacement.RANDOM.value:
        return random_placement(settings)
    else:
        return fixed_placement(settings)


def random_placement(settings: GameSettings):
    grid_width = settings.grid_size[0]
    grid_height = settings.grid_size[1]

    reserved = {(0, 0), (grid_width - 1, grid_height - 1)}
    available_cells = [
        (x, y)
        for x in range(grid_width)
        for y in range(grid_height)
        if (x, y) not in reserved
    ]
    random.shuffle(available_cells)

    mobs = []
    for i in range(settings.mob_count):
        x, y = available_cells[i]
        path = create_mob_path(settings, x, y)
        mobs.append(Mob(x, y, settings.mob_move_pattern, path))

    weapon = None
    if not settings.has_weapon:
        weapon = Weapon(*available_cells[settings.mob_count])

    agent = Agent(0, 0, settings.has_weapon)
    goal = Goal(grid_width - 1, grid_height - 1)

    return (agent, goal, weapon, mobs)


def fixed_placement(settings: GameSettings):
    """
    When spawning a fixed size grid:
    agent is always (0,0)
    goal is always (width - 1, height - 1)
    weapon is always (1, height - 3)
    mobs are always:
    mob 1: (width - 2, 3)
    mob 2: (5, height - 3)
    mob 3: (width - 4, 1)
    mob 4: (1, height - 6)
    """
    grid_width = settings.grid_size[0]
    grid_height = settings.grid_size[1]

    mob_positions = [
        (grid_width - 2, 3),
        (5, grid_height - 3),
        (grid_width - 4, 1),
        (1, grid_height - 6),
    ]

    mobs = []
    for i in range(settings.mob_count):
        x, y = mob_positions[i]
        path = create_mob_path(settings, x, y)
        mobs.append(Mob(x, y, settings.mob_move_pattern, path))

    agent = Agent(0, 0, settings.has_weapon)
    weapon = Weapon(1, grid_height - 3)
    goal = Goal(grid_width - 1, grid_height - 1)

    return (agent, goal, weapon, mobs)


def create_mob_path(settings: GameSettings, start_x: int, start_y: int):
    if settings.mob_move_pattern != MobMovePattern.LINEAR.value:
        return None

    grid_width, grid_height = settings.grid_size
    goal_position = (grid_width - 1, grid_height - 1)
    axes = ["x", "y"]
    random.shuffle(axes)

    def safe_distance(axis: str, direction: int) -> int:
        if axis == "x":
            if direction == 1 and start_y == goal_position[1]:
                return min(grid_width - 1 - start_x, goal_position[0] - start_x - 1)
            return grid_width - 1 - start_x if direction == 1 else start_x
        if direction == 1 and start_x == goal_position[0]:
            return min(grid_height - 1 - start_y, goal_position[1] - start_y - 1)
        return grid_height - 1 - start_y if direction == 1 else start_y

    def build_line(axis: str) -> Optional[List[Tuple[int, int]]]:
        directions = [1, -1]
        random.shuffle(directions)
        for direction in directions:
            max_distance = safe_distance(axis, direction)
            if max_distance <= 0:
                continue

            distance = random.randint(1, max_distance)
            path = []
            for step in range(1, distance + 1):
                if axis == "x":
                    path.append((start_x + direction * step, start_y))
                else:
                    path.append((start_x, start_y + direction * step))

            # ensure the goal square is never on the mob path
            if any(position == goal_position for position in path):
                continue

            path += list(reversed(path[:-1]))
            path.append((start_x, start_y))
            return path

        return None

    for axis in axes:
        path = build_line(axis)
        if path:
            return path

    return None
