from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Callable

from src.environment.entities import Entity
from src.ui.colours import UIColour


class VisualShape(Enum):
    CIRCLE = "circle"
    RECT = "rect"


@dataclass(frozen=True)
class EntityVisual:
    shape: VisualShape
    fill: tuple[int, int, int]
    label: str | None = None
    label_colour: tuple[int, int, int] = UIColour.BLACK.value
    outline: tuple[int, int, int] | None = None


def background_visual(entity: Entity) -> EntityVisual:
    return _visual_for(entity, BACKGROUND_VISUALS, DEFAULT_BACKGROUND_VISUAL)


def foreground_visual(entity: Entity) -> EntityVisual:
    visual = _visual_for(entity, FOREGROUND_VISUALS, DEFAULT_FOREGROUND_VISUAL)

    if entity.name == "Player" and getattr(entity, "held_item", None) is not None:
        return EntityVisual(
            shape=visual.shape,
            fill=visual.fill,
            label=visual.label,
            label_colour=visual.label_colour,
            outline=UIColour.KEY.value,
        )

    return visual


def _visual_for(
    entity: Entity,
    registry: dict[str, EntityVisual],
    default_factory: Callable[[Entity], EntityVisual],
) -> EntityVisual:
    if entity.name in registry:
        return registry[entity.name]

    prefix = entity.name.split("_", 1)[0]
    if prefix in registry:
        return registry[prefix]

    return default_factory(entity)


def DEFAULT_BACKGROUND_VISUAL(entity: Entity) -> EntityVisual:
    fill = UIColour.WALL.value if entity.blocks_movement else UIColour.TILE.value
    return EntityVisual(VisualShape.RECT, fill)


def DEFAULT_FOREGROUND_VISUAL(entity: Entity) -> EntityVisual:
    return EntityVisual(VisualShape.RECT, UIColour.PANEL_LIGHT.value)


BACKGROUND_VISUALS = {
    "Tile": EntityVisual(VisualShape.RECT, UIColour.TILE.value),
    "Wall": EntityVisual(VisualShape.RECT, UIColour.WALL.value),
    "Goal": EntityVisual(VisualShape.RECT, UIColour.GOAL.value),
    "Door": EntityVisual(VisualShape.RECT, UIColour.DOOR.value),
}

FOREGROUND_VISUALS = {
    "Player": EntityVisual(VisualShape.CIRCLE, UIColour.PLAYER.value),
    "Mob": EntityVisual(VisualShape.CIRCLE, UIColour.MOB.value),
    "Key": EntityVisual(VisualShape.RECT, UIColour.KEY.value, label="K"),
    "Weapon": EntityVisual(VisualShape.RECT, UIColour.WEAPON.value, label="W"),
}
