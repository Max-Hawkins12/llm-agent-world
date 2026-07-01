from __future__ import annotations

from dataclasses import dataclass

import pygame

from src.environment.entities import Entity
from src.environment.game import Game
from src.ui.colours import UIColour
from src.ui.context import RenderContext
from src.ui.visuals import (
    EntityVisual,
    VisualShape,
    background_visual,
    foreground_visual,
)


@dataclass(frozen=True)
class GridLayout:
    offset_x: int
    offset_y: int
    cell_size: int
    width: int
    height: int


class GridRenderer:
    def __init__(self, context: RenderContext):
        self.context = context

    def render(self, game: Game, area: pygame.Rect) -> None:
        layout = self._layout(game, area)
        self._draw_grid(game, layout)
        for entity in game.get_alive_entities():
            self._draw_entity(entity, layout)

    def _layout(self, game: Game, area: pygame.Rect) -> GridLayout:
        cell_size = max(
            8,
            min(area.width // game.grid_width, area.height // game.grid_height),
        )
        width = cell_size * game.grid_width
        height = cell_size * game.grid_height
        return GridLayout(
            offset_x=area.x + (area.width - width) // 2,
            offset_y=area.y + (area.height - height) // 2,
            cell_size=cell_size,
            width=width,
            height=height,
        )

    def _draw_grid(self, game: Game, layout: GridLayout) -> None:
        for y in range(game.grid_height):
            for x in range(game.grid_width):
                rect = self._cell_rect(layout, x, y)
                entity = game.grid.background[y][x]
                visual = background_visual(entity)
                pygame.draw.rect(self.context.screen, visual.fill, rect)
                pygame.draw.rect(self.context.screen, UIColour.GRID_LINE.value, rect, 1)

    def _draw_entity(self, entity: Entity, layout: GridLayout) -> None:
        rect = self._cell_rect(layout, entity.position.x, entity.position.y).inflate(
            -8, -8
        )
        self._draw_visual(foreground_visual(entity), rect)

    def _draw_visual(self, visual: EntityVisual, rect: pygame.Rect) -> None:
        if visual.shape == VisualShape.CIRCLE:
            pygame.draw.circle(
                self.context.screen,
                visual.fill,
                rect.center,
                max(5, rect.width // 2),
            )
            if visual.outline:
                pygame.draw.circle(
                    self.context.screen,
                    visual.outline,
                    rect.center,
                    max(7, rect.width // 2),
                    3,
                )
        else:
            pygame.draw.rect(self.context.screen, visual.fill, rect, border_radius=4)
            if visual.outline:
                pygame.draw.rect(
                    self.context.screen,
                    visual.outline,
                    rect,
                    width=3,
                    border_radius=4,
                )

        if visual.label:
            self.context.draw_centered_text(
                visual.label,
                rect,
                self.context.small_font,
                visual.label_colour,
            )

    def _cell_rect(self, layout: GridLayout, x: int, y: int) -> pygame.Rect:
        return pygame.Rect(
            layout.offset_x + x * layout.cell_size,
            layout.offset_y + y * layout.cell_size,
            layout.cell_size,
            layout.cell_size,
        )
