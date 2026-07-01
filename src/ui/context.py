from __future__ import annotations

from typing import Iterable

import pygame

from src.ui.colours import UIColour


class RenderContext:
    def __init__(self, screen: pygame.Surface, window_width: int, window_height: int):
        self.screen = screen
        self.window_width = window_width
        self.window_height = window_height
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 20)
        self.large_font = pygame.font.Font(None, 42)
        self.title_font = pygame.font.Font(None, 34)
        self.click_regions: dict[str, pygame.Rect] = {}

    def begin_frame(self) -> None:
        self.click_regions = {}
        self.screen.fill(UIColour.BG.value)

    def hit_test(self, pos: tuple[int, int]) -> str | None:
        for action_id, rect in reversed(self.click_regions.items()):
            if rect.collidepoint(pos):
                return action_id
        return None

    def register_click(self, action_id: str, rect: pygame.Rect) -> None:
        self.click_regions[action_id] = rect

    def draw_panel(self, rect: pygame.Rect) -> None:
        pygame.draw.rect(self.screen, UIColour.PANEL.value, rect, border_radius=8)
        pygame.draw.rect(self.screen, UIColour.BORDER.value, rect, 1, border_radius=8)

    def draw_button(
        self,
        action_id: str,
        rect: pygame.Rect,
        label: str,
        enabled: bool = True,
        compact: bool = False,
    ) -> None:
        colour = UIColour.ACCENT.value if enabled else UIColour.PANEL_LIGHT.value
        text_colour = UIColour.WHITE.value if enabled else UIColour.DISABLED_TEXT.value
        pygame.draw.rect(self.screen, colour, rect, border_radius=5)
        pygame.draw.rect(self.screen, UIColour.BORDER.value, rect, 1, border_radius=5)
        self.draw_centered_text(
            label,
            rect,
            self.small_font if compact else self.font,
            text_colour,
        )
        if enabled:
            self.register_click(action_id, rect)

    def draw_text(
        self,
        text: str,
        x: int,
        y: int,
        font: pygame.font.Font,
        colour: tuple[int, int, int] = UIColour.TEXT.value,
    ) -> pygame.Rect:
        surface = font.render(str(text), True, colour)
        rect = surface.get_rect(topleft=(x, y))
        self.screen.blit(surface, rect)
        return rect

    def draw_centered_text(
        self,
        text: str,
        rect: pygame.Rect,
        font: pygame.font.Font,
        colour: tuple[int, int, int] = UIColour.TEXT.value,
    ) -> None:
        surface = font.render(str(text), True, colour)
        text_rect = surface.get_rect(center=rect.center)
        self.screen.blit(surface, text_rect)

    def draw_lines(
        self,
        lines: Iterable[str],
        x: int,
        y: int,
        line_height: int,
        colour: tuple[int, int, int] = UIColour.TEXT.value,
    ) -> None:
        for index, line in enumerate(lines):
            self.draw_text(line, x, y + index * line_height, self.font, colour)

    def draw_wrapped_text(
        self,
        text: str,
        x: int,
        y: int,
        max_width: int,
        font: pygame.font.Font,
        colour: tuple[int, int, int] = UIColour.TEXT.value,
    ) -> int:
        words = str(text).split()
        if not words:
            return y

        line = ""
        line_height = font.get_linesize()
        for word in words:
            candidate = word if not line else f"{line} {word}"
            if font.size(candidate)[0] <= max_width:
                line = candidate
                continue

            self.draw_text(line, x, y, font, colour)
            y += line_height
            line = word

        if line:
            self.draw_text(line, x, y, font, colour)
            y += line_height

        return y
