from typing import List, Optional

from src.environment.entities import GameEntity, Mob
from src.environment.entity_placement import place_entities
from src.environment.utils import is_within_bounds
from src.actions import GameAction
from src.game_options import GameSettings


class Game:
    def __init__(self, settings: GameSettings = GameSettings()):
        self.grid_width = settings.grid_size[0]
        self.grid_height = settings.grid_size[1]

        self.agent, self.goal, self.weapon, self.mobs = place_entities(settings)

        self.finished = False
        self.update_goal_lock()

    def process_action(self, action: GameAction) -> None:
        match action:
            case GameAction.MOVE_UP:
                self.try_move_agent(0, -1)
            case GameAction.MOVE_DOWN:
                self.try_move_agent(0, 1)
            case GameAction.MOVE_LEFT:
                self.try_move_agent(-1, 0)
            case GameAction.MOVE_RIGHT:
                self.try_move_agent(1, 0)

    def try_move_agent(self, dx: int, dy: int) -> None:
        target_x, target_y = self.agent.x + dx, self.agent.y + dy
        mob_at_target = self.get_mob_at(target_x, target_y)

        if not is_within_bounds(target_x, target_y, self.grid_width, self.grid_height):
            return
        elif mob_at_target and not self.agent.has_weapon:
            return

        self.agent.move_to(target_x, target_y)

        self.defeat_mob_at(mob_at_target)
        self.pick_up_weapon()
        self.resolve_goal_reached()

        self.move_mobs()

    def defeat_mob_at(self, mob) -> None:
        if mob:
            mob.alive = False
            self.update_goal_lock()

    def pick_up_weapon(self) -> None:
        if (
            not self.agent.has_weapon
            and self.agent.position() == self.weapon.position()
        ):
            self.weapon.alive = False
            self.agent.has_weapon = True

    def resolve_goal_reached(self) -> None:
        if self.agent.position() == self.goal.position() and not self.goal.locked:
            self.finished = True

    def move_mobs(self) -> None:
        for mob in self.mobs:
            if not mob.alive:
                continue

            new_x, new_y = mob.next_move(self.grid_width, self.grid_height)

            if not self.is_cell_occupied(new_x, new_y):
                # A mob will not move onto an occupied cell
                mob.move_to(new_x, new_y)

    def is_cell_occupied(self, x: int, y: int) -> bool:
        if self.agent.position() == (x, y):
            return True
        if self.weapon.alive and self.weapon.position() == (x, y):
            return True
        if self.goal.position() == (x, y):
            return True
        for mob in self.mobs:
            if mob.alive and mob.position() == (x, y):
                return True
        return False

    def update_goal_lock(self) -> None:
        if not any(mob.alive for mob in self.mobs):
            self.goal.locked = False

    def get_mob_at(self, x: int, y: int) -> Optional[Mob]:
        for mob in self.mobs:
            if mob.alive and mob.x == x and mob.y == y:
                return mob
        return None

    def has_finished(self) -> bool:
        return self.finished

    def get_alive_entities(self) -> List[GameEntity]:
        entities = [self.agent, self.weapon, self.goal] + self.mobs
        return [entity for entity in entities if entity.alive]

    def total_alive_mobs(self) -> int:
        return len([m for m in self.mobs if m.alive])
