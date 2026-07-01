from typing import Optional

from src.environment.entities import (
    Actor,
    BackgroundEntity,
    Goal,
    StaticEntity,
    Tile,
    Wall,
)
from src.environment.utils import Position, Direction


class Grid:
    """Base class for grid-based environments."""

    def __init__(
        self,
        width: int,
        height: int,
        player_start_pos: Position = Position(0, 0),
        fill_with_walls: bool = False,
    ):
        if width < 1 or height < 1:
            raise ValueError("Grid width and height must both be at least 1")

        self.grid_width = width
        self.grid_height = height

        self.background: list[list[BackgroundEntity]] = [
            [
                self._create_cell(Position(x, y), fill_with_walls)
                for x in range(self.grid_width)
            ]
            for y in range(self.grid_height)
        ]

        self.player_pos = player_start_pos
        self.goal_pos: Position | None = None
        self._actors: list[Actor] = []
        self._static_entities: list[StaticEntity] = []

    @property
    def goal(self) -> Optional[Goal]:
        return (
            self.background[self.goal_pos.y][self.goal_pos.x] if self.goal_pos else None
        )

    @property
    def actors(self) -> list[Actor]:
        return self._actors

    @property
    def static_entities(self) -> list[StaticEntity]:
        return self._static_entities

    @property
    def entities(self) -> list[Actor | StaticEntity]:
        return [*self._actors, *self._static_entities]

    # Methods used by subclasses during grid creation.

    def _create_cell(self, pos: Position, is_wall: bool) -> BackgroundEntity:
        return Wall(pos) if is_wall else Tile(pos)

    def _set_background_entity(self, entity: BackgroundEntity) -> None:
        self.background[entity.pos.y][entity.pos.x] = entity

    def _place_tile(self, pos: Position) -> None:
        self._set_background_entity(Tile(pos))

    def _place_wall(self, pos: Position) -> None:
        self._set_background_entity(Wall(pos))

    def _place_goal(self, pos: Position, is_locked: bool) -> None:
        self.goal_pos: Position = pos
        self._set_background_entity(Goal(pos, is_locked))

    def _add_actor(self, actor: Actor) -> None:
        self._actors.append(actor)

    def _add_static_entity(self, entity: StaticEntity) -> None:
        self._static_entities.append(entity)

    def _all_positions(self) -> list[Position]:
        return [
            Position(x, y)
            for y in range(self.grid_height)
            for x in range(self.grid_width)
        ]

    def _get_passable_positions(self) -> list[Position]:
        return [pos for pos in self._all_positions() if self.is_passable(pos)]

    def _get_wall_positions(self) -> list[Position]:
        return [pos for pos in self._all_positions() if self.is_wall(pos)]

    # Public movement and terrain checks.

    def neighbors(self, pos: Position) -> list[Position]:
        return [
            neighbor
            for direction in Direction
            if self.is_within_bounds(neighbor := pos.moved_by(direction.value))
        ]

    def is_within_bounds(self, pos: Position) -> bool:
        return 0 <= pos.x < self.grid_width and 0 <= pos.y < self.grid_height

    def is_wall(self, pos: Position) -> bool:
        return isinstance(self.background[pos.y][pos.x], Wall)

    def is_passable(self, pos: Position) -> bool:
        return self.background[pos.y][pos.x].is_passable

    def is_valid_movement_position(self, pos: Position) -> bool:
        return self.is_within_bounds(pos) and self.is_passable(pos)

    def is_new_position_valid(self, pos: Position) -> bool:
        return self.is_valid_movement_position(pos)

    def get_entity_at(
        self,
        position: Position,
        ignore: Actor | StaticEntity | None = None,
    ) -> Actor | StaticEntity | None:
        for entity in self.entities:
            if entity is ignore:
                continue
            if entity.alive and entity.pos == position:
                return entity
        return None

    def static_entities_at(self, position: Position) -> list[StaticEntity]:
        return [
            entity
            for entity in self._static_entities
            if entity.alive and entity.pos == position
        ]

    def is_position_occupied(
        self,
        position: Position,
        ignore: Actor | StaticEntity | None = None,
    ) -> bool:
        entity = self.get_entity_at(position, ignore=ignore)
        return bool(entity and not entity.is_passable)

    def valid_actor_moves(self, actor: Actor) -> list[Position]:
        return [
            position
            for position in self.neighbors(actor.pos)
            if self.can_actor_move_to(actor, position)
        ]

    def can_actor_move_to(self, actor: Actor, position: Position) -> bool:
        return self.is_valid_movement_position(
            position
        ) and not self.is_position_occupied(position, ignore=actor)

    def target_entity_in_direction(
        self,
        actor: Actor,
        direction: Direction,
    ) -> Actor | StaticEntity | BackgroundEntity | None:
        target_position = actor.pos.moved_by(direction.value)
        if not self.is_within_bounds(target_position):
            return None

        return (
            self.get_entity_at(target_position)
            or self.background[target_position.y][target_position.x]
        )

    def update(self) -> None:
        pass

    def get_tile_positions(self) -> list[Position]:
        return self._get_passable_positions()

    def get_wall_positions(self) -> list[Position]:
        return self._get_wall_positions()
