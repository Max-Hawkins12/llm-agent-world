from dataclasses import dataclass

import pygame

from src.environment.entities import Agent, Goal, Mob, GameEntity
from src.environment.game import Game
from src.ui.colours import UIColour
from src.ui.menu import StartMenu


@dataclass(frozen=True)
class GridLayout:
    offset_x: int
    offset_y: int
    width: int
    height: int


class Renderer:

    def __init__(
        self,
        window_width: int,
        window_height: int,
        grid_width: int,
        grid_height: int,
        cell_size: int = 64,
    ):
        self.screen = pygame.display.set_mode((window_width, window_height))
        self.clock = pygame.time.Clock()

        self.window_width = window_width
        self.window_height = window_height

        self.grid_width = grid_width
        self.grid_height = grid_height
        self.cell_size = cell_size

        self.font = pygame.font.Font(None, 24)
        self.large_font = pygame.font.Font(None, 40)

    def set_grid_size(self, width: int, height: int) -> None:
        self.grid_width = width
        self.grid_height = height

    def present(self, fps: int) -> None:
        pygame.display.flip()
        self.clock.tick(fps)

    def render_menu(self, menu: StartMenu) -> None:
        self.screen.fill(UIColour.MENU_BG.value)

        self._draw_centered_text(
            "LLM Agent Grid World Explorer",
            80,
            self.large_font,
        )

        self._draw_text(
            "Use arrow keys to configure settings, SPACE to start.",
            20,
            130,
            UIColour.MENU_TEXT.value,
        )

        y = 180

        for label, value, selected in menu.option_lines():
            colour = (
                UIColour.MENU_HIGHLIGHT.value if selected else UIColour.MENU_TEXT.value
            )

            prefix = ">" if selected else " "

            self._draw_text(
                f"{prefix} {label}: {value}",
                60,
                y,
                colour,
            )

            y += 40

    def render_game(self, game: Game) -> None:
        self.screen.fill(UIColour.GRID_BG.value)

        layout = self._grid_layout()

        self._draw_grid(layout)

        for entity in game.get_alive_entities():
            self._draw_entity(entity, layout)

    def render_end_screen(self, game: Game) -> None:
        self.render_game(game)

        overlay = pygame.Surface(
            (self.window_width, self.window_height),
            pygame.SRCALPHA,
        )

        overlay.fill((0, 0, 0, 160))

        self.screen.blit(overlay, (0, 0))

        self._draw_centered_text(
            "Game Finished!",
            self.window_height // 2 - 40,
            self.large_font,
        )

        self._draw_centered_text(
            "Press ESC to quit.",
            self.window_height // 2 + 40,
            self.font,
        )

    def _grid_layout(self) -> GridLayout:
        pixel_width = self.grid_width * self.cell_size
        pixel_height = self.grid_height * self.cell_size

        return GridLayout(
            offset_x=(self.window_width - pixel_width) // 2,
            offset_y=(self.window_height - pixel_height) // 2,
            width=pixel_width,
            height=pixel_height,
        )

    def _draw_grid(self, layout: GridLayout) -> None:

        rect = pygame.Rect(
            layout.offset_x,
            layout.offset_y,
            layout.width,
            layout.height,
        )

        pygame.draw.rect(
            self.screen,
            UIColour.GRID_BG.value,
            rect,
        )

        for x in range(self.grid_width + 1):

            px = layout.offset_x + x * self.cell_size

            pygame.draw.line(
                self.screen,
                UIColour.GRID_GREY.value,
                (px, layout.offset_y),
                (px, layout.offset_y + layout.height),
            )

        for y in range(self.grid_height + 1):

            py = layout.offset_y + y * self.cell_size

            pygame.draw.line(
                self.screen,
                UIColour.GRID_GREY.value,
                (layout.offset_x, py),
                (layout.offset_x + layout.width, py),
            )

    def _draw_entity(
        self,
        entity: GameEntity,
        layout: GridLayout,
    ) -> None:

        cell_x = layout.offset_x + entity.x * self.cell_size
        cell_y = layout.offset_y + entity.y * self.cell_size

        outline = self._should_outline(entity)

        if isinstance(entity, (Agent, Mob)):
            self._draw_circle_entity(
                entity,
                cell_x,
                cell_y,
                outline,
            )
        else:
            self._draw_rect_entity(
                entity,
                cell_x,
                cell_y,
                outline,
            )

    def _should_outline(self, entity: GameEntity) -> bool:

        if isinstance(entity, Goal):
            return not entity.locked

        if isinstance(entity, Agent):
            return entity.has_weapon

        return False

    def _draw_circle_entity(
        self,
        entity: Agent | Mob,
        cell_x: int,
        cell_y: int,
        outline: bool,
    ) -> None:

        centre = (
            cell_x + self.cell_size // 2,
            cell_y + self.cell_size // 2,
        )

        radius = (self.cell_size - 12) // 2

        colour = (
            UIColour.AGENT_BLUE.value
            if isinstance(entity, Agent)
            else UIColour.MOB_RED.value
        )

        pygame.draw.circle(
            self.screen,
            colour,
            centre,
            radius,
        )

        if outline and entity.outline_colour:
            pygame.draw.circle(
                self.screen,
                entity.outline_colour.value,
                centre,
                radius,
                3,
            )

    def _draw_rect_entity(
        self,
        entity: GameEntity,
        cell_x: int,
        cell_y: int,
        outline: bool,
    ) -> None:

        rect = pygame.Rect(
            cell_x + 4,
            cell_y + 4,
            self.cell_size - 8,
            self.cell_size - 8,
        )

        pygame.draw.rect(
            self.screen,
            entity.colour.value,
            rect,
        )

        if outline and entity.outline_colour:
            pygame.draw.rect(
                self.screen,
                entity.outline_colour.value,
                rect,
                3,
            )

    def _draw_text(
        self,
        text: str,
        x: int,
        y: int,
        colour=UIColour.WHITE.value,
    ) -> None:

        surface = self.font.render(
            text,
            True,
            colour,
        )

        self.screen.blit(surface, (x, y))

    def _draw_centered_text(
        self,
        text: str,
        y: int,
        font: pygame.font.Font,
    ) -> None:

        surface = font.render(
            text,
            True,
            UIColour.WHITE.value,
        )

        rect = surface.get_rect(center=(self.window_width // 2, y))

        self.screen.blit(surface, rect)
