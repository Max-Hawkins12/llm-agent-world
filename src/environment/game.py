from dataclasses import dataclass

from .entities import Actor, Entity, Player
from .grids import Grid
from .utils import Direction, Position

from src.actions import GameAction


@dataclass
class ActionOutcome:
    action_name: str = ""
    outcome: str = "This is the first move."


class Game:
    def __init__(self, grid: Grid):
        self.grid = grid
        self.grid_width = grid.grid_width
        self.grid_height = grid.grid_height

        self.player = Player(self.grid.player_pos)
        self.agent = self.player

        self.action_outcome = ActionOutcome()
        self.finished = False
        self._update_grid()

    @property
    def goal(self):
        return self.grid.goal

    @property
    def entities(self) -> list[Entity]:
        return [self.player, *self.grid.entities]

    def process_action(self, action: GameAction) -> None:

        self.action_outcome.action_name = action.value

        if not self._perform_player_action(action):
            return

        self._update_actors()
        self._update_grid()
        self.finished = self._is_goal_reached()

    def _perform_player_action(self, action: GameAction) -> bool:

        if action.is_movement_action:
            target_position = self.player.pos.moved_by(action.direction.value)
            if self._try_move_actor(self.player, target_position):
                self.action_outcome.outcome = "You moved successfully."
            else:
                self.action_outcome.outcome = "You did not move."
        elif action == GameAction.PICK_UP:
            if self._pick_up_static_entity(self.player):
                self.action_outcome.outcome = "You picked up an item."
            else:
                self.action_outcome.outcome = "You did not pick anything up."
        elif action.is_use_action:
            if self._use_held_item(self.player, action.direction):
                self.action_outcome.outcome = "You used your item."
            else:
                self.action_outcome.outcome = "You did not use an item."
        elif action == GameAction.WAIT:
            self.action_outcome.outcome = "You waited."
            return False
        elif action == GameAction.INVALID:
            self.action_outcome.outcome = "This action was invalid."
            return False

        return True

    def _try_move_actor(self, actor: Actor, position: Position) -> bool:
        if position == actor.pos:
            return False
        if not self.grid.is_valid_movement_position(position):
            return False

        target_entity = self.grid.get_entity_at(position, ignore=actor)
        if target_entity and not target_entity.is_passable:
            if not target_entity.defeat():
                return False

        actor.move_to(position)
        return True

    def _pick_up_static_entity(self, actor: Player) -> bool:
        if actor.held_item is not None:
            return False

        entities = self.grid.static_entities_at(actor.pos)
        if not entities:
            return False

        entity = entities[0]
        if not entity.pick_up(actor):
            return False

        self.grid.static_entities.remove(entity)
        actor.held_item = entity
        return True

    def _use_held_item(self, actor: Player, direction: Direction) -> bool:
        item = actor.held_item
        if item is None:
            return False

        target = self.grid.target_entity_in_direction(actor, direction)
        if target is None:
            return False

        if not item.use_on(target):
            return False

        if not item.alive:
            actor.held_item = None

        return True

    def _update_actors(self) -> None:
        for actor in list(self.grid.actors):
            if not actor.alive:
                continue

            next_position = actor.next_move(self.grid)
            if next_position is not None:
                self._try_move_actor(actor, next_position)

    def _is_goal_reached(self) -> bool:
        return bool(
            self.grid.goal
            and self.player.pos == self.grid.goal.pos
            and not self.grid.goal.is_locked
        )

    def _update_grid(self) -> None:
        self.grid.update()

    def has_finished(self) -> bool:
        return self.finished

    def get_alive_entities(self) -> list[Entity]:
        entities = self.entities
        if self.grid.goal:
            entities.append(self.grid.goal)

        return [entity for entity in entities if entity.alive]

    def return_previous_action_outcome(self) -> dict:
        return {
            "action": self.action_outcome.action_name,
            "outcome": self.action_outcome.outcome,
        }
