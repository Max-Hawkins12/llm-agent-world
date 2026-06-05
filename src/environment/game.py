from enum import Enum
from typing import List, Optional

from src.environment.entities import Weapon, Goal, Agent, Mob, MovePattern
from src.environment.utils import is_within_bounds

from src.constants import GRID_HEIGHT, GRID_WIDTH
from src.actions import Action


class GameState(Enum):
    RUNNING = "running"
    WON = "won"


class Game:
    def __init__(self):

        mob_path = [
            (5, 4),
            (5, 3),
            (5, 2),
            (5, 1),
            (5, 0),
            (5, 1),
            (5, 2),
            (5, 3),
            (5, 4),
            (5, 5),
            (5, 6),
            (5, 7),
            (5, 6),
            (5, 5),
        ]
        self.agent = Agent(1, 1)
        self.weapon = Weapon(3, 5)
        self.goal = Goal(GRID_WIDTH - 2, GRID_HEIGHT - 2)
        self.mobs: List[Mob] = [
            Mob(7, 2, MovePattern.RANDOM),
            Mob(5, 4, MovePattern.LOOP, path=mob_path),
        ]

        self.state = GameState.RUNNING
        self.message = "Reach the goal after defeating all mobs."

    def handle_action(self, action: Action) -> None:
        """
        Process the given action, update the game state, and generate a message for the player.
        """
        match action:
            case Action.MOVE_UP:
                self.try_move_agent(0, -1)
            case Action.MOVE_DOWN:
                self.try_move_agent(0, 1)
            case Action.MOVE_LEFT:
                self.try_move_agent(-1, 0)
            case Action.MOVE_RIGHT:
                self.try_move_agent(1, 0)
            case Action.INVALID:
                # This case can be used for telling the LLM it has generated an invalid action, but for now we just ignore it.
                self.message = "Invalid action."

    def try_move_agent(self, dx: int, dy: int) -> None:
        target_x, target_y = self.agent.x + dx, self.agent.y + dy
        if not is_within_bounds(target_x, target_y):
            self.message = "You can't move outside the grid!"
            return

        mob = self.get_mob_at(target_x, target_y)

        if mob and not self.agent.has_weapon:
            self.message = "You can't move onto a mob without the weapon. Pick up the weapon first to defeat mobs."
            return

        self.agent.move_to(target_x, target_y)

        if mob:
            mob.alive = False
            self.message = "You struck the mob while moving."
            self.update_goal_lock()
            return

        self.pick_up_weapon()
        self.resolve_goal_reached()
        self.move_mobs()

    def pick_up_weapon(self) -> None:
        if (
            not self.agent.has_weapon
            and self.agent.position() == self.weapon.position()
        ):
            self.agent.has_weapon = True
            self.message = (
                "Weapon picked up. You can now defeat mobs by moving into them."
            )

    def resolve_goal_reached(self) -> None:
        if self.agent.position() == self.goal.position():
            if self.goal.locked:
                self.message = "The goal is locked until all mobs are defeated."
            else:
                self.state = GameState.WON
                self.message = "You won! All mobs are defeated and the goal is reached."

    def move_mobs(self) -> None:
        for mob in self.mobs:
            if not mob.alive:
                continue

            new_x, new_y = mob.next_move()
            if (new_x, new_y) == self.agent.position():
                if self.agent.has_weapon:
                    mob.alive = False
                    self.message = "A mob moved into you and was defeated."
                    self.update_goal_lock()
                return

            mob.move_to(new_x, new_y)

    def update_goal_lock(self) -> None:
        if not any(mob.alive for mob in self.mobs):
            self.goal.locked = False

    def get_mob_at(self, x: int, y: int) -> Optional[Mob]:
        for mob in self.mobs:
            if mob.alive and mob.x == x and mob.y == y:
                return mob
        return None
