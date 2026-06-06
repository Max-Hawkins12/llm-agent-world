from enum import Enum
from typing import List, Optional

from src.environment.entities import GameEntity, Mob
from src.environment.entity_placement import place_entities
from src.environment.utils import is_within_bounds
from src.actions import GameAction
from src.game_options import GameSettings, DEFAULT_GAME_SETTINGS


class Messages(Enum):
    OUT_OF_BOUNDS_MOVEMENT = "You can't move outside the grid!"
    NO_WEAPON_MOVE_TO_MOB = "You can't move onto a mob without the weapon. Pick up the weapon first to defeat mobs."
    WEAPON_PICKUP = "Weapon picked up. You can now defeat mobs by moving into them."
    MOB_DEFEATED = "You struck a mob and defeated it!"
    GOAL_REACHED_LOCKED = "The goal is locked until all mobs are defeated."
    GAME_REACHED_UNLOCKED = "You won! All mobs are defeated and the goal is reached."
    DEFAULT = "Reach the goal after defeating all mobs."
    MOVEMENT_SUCCESS = "You moved successfully."


class Game:
    def __init__(self, settings: GameSettings = DEFAULT_GAME_SETTINGS):
        self.grid_width = settings.grid_size[0]
        self.grid_height = settings.grid_size[1]

        self.agent, self.goal, self.weapon, self.mobs = place_entities(settings)

        self.finished = False
        self.message = Messages.DEFAULT.value
        self.update_goal_lock()

    def process_action(self, action: GameAction) -> None:
        """
        Process the given action, update the game state, and generate a message for the player.
        """
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
            self.message = Messages.OUT_OF_BOUNDS_MOVEMENT.value
            return
        elif mob_at_target and not self.agent.has_weapon:
            self.message = Messages.NO_WEAPON_MOVE_TO_MOB.value
            return

        self.agent.move_to(target_x, target_y)
        self.message = Messages.MOVEMENT_SUCCESS.value

        self.defeat_mob_at(mob_at_target)
        self.pick_up_weapon()
        self.resolve_goal_reached()

        self.move_mobs()

    def defeat_mob_at(self, mob) -> None:
        if mob:
            mob.alive = False
            self.message = Messages.MOB_DEFEATED.value
            self.update_goal_lock()

    def pick_up_weapon(self) -> None:
        if (
            not self.agent.has_weapon
            and self.agent.position() == self.weapon.position()
        ):
            self.weapon.alive = False
            self.agent.has_weapon = True
            self.message = Messages.WEAPON_PICKUP.value

    def resolve_goal_reached(self) -> None:
        if self.agent.position() == self.goal.position():
            if self.goal.locked:
                self.message = Messages.GOAL_REACHED_LOCKED.value
            else:
                self.finished = True
                self.message = Messages.GAME_REACHED_UNLOCKED.value

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
