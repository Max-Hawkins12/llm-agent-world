from __future__ import annotations

import pygame

from src.environment.game import Game
from src.app.experiment import TurnRecord
from src.ui.colours import UIColour
from src.ui.context import RenderContext
from src.ui.grid_renderer import GridRenderer


class ExperimentRenderer:
    def __init__(self, context: RenderContext, grid_renderer: GridRenderer):
        self.context = context
        self.grid_renderer = grid_renderer

    def render(
        self,
        game: Game,
        turns: list[TurnRecord],
        run_index: int,
        run_count: int,
    ) -> None:
        ctx = self.context
        sidebar = pygame.Rect(20, 20, 330, ctx.window_height - 40)
        ctx.draw_panel(sidebar)
        ctx.draw_text("LLM Responses", sidebar.x + 18, sidebar.y + 18, ctx.title_font)
        self._draw_response_history(sidebar, turns)

        header = pygame.Rect(380, 20, ctx.window_width - 410, 58)
        ctx.draw_panel(header)
        active_turns = sum(1 for turn in turns if turn.run_index == run_index)
        status = (
            f"Run {run_index} / {run_count}    "
            f"Turn {active_turns}    "
            f"Grid {game.grid_width} x {game.grid_height}"
        )
        ctx.draw_text(status, header.x + 18, header.y + 19, ctx.font)

        grid_area = pygame.Rect(
            380, 102, ctx.window_width - 410, ctx.window_height - 122
        )
        self.grid_renderer.render(game, grid_area)

    def _draw_response_history(
        self,
        sidebar: pygame.Rect,
        turns: list[TurnRecord],
    ) -> None:
        ctx = self.context
        if not turns:
            ctx.draw_wrapped_text(
                "Waiting for the first action.",
                sidebar.x + 18,
                sidebar.y + 64,
                sidebar.width - 36,
                ctx.font,
                UIColour.MUTED_TEXT.value,
            )
            return

        y = sidebar.y + 62
        for turn in list(reversed(turns))[:9]:
            colour = (
                UIColour.ERROR.value
                if turn.is_invalid or turn.failure
                else UIColour.TEXT.value
            )
            header = (
                f"Run {turn.run_index} Turn {turn.turn_number}: {turn.action.value}"
            )
            y = ctx.draw_wrapped_text(
                header,
                sidebar.x + 18,
                y,
                sidebar.width - 36,
                ctx.small_font,
                colour,
            )
            if turn.reasoning:
                y = ctx.draw_wrapped_text(
                    turn.reasoning,
                    sidebar.x + 18,
                    y + 4,
                    sidebar.width - 36,
                    ctx.small_font,
                    UIColour.MUTED_TEXT.value,
                )
            if turn.outcome:
                y = ctx.draw_wrapped_text(
                    f"Outcome: {turn.outcome}",
                    sidebar.x + 18,
                    y + 4,
                    sidebar.width - 36,
                    ctx.small_font,
                    UIColour.MUTED_TEXT.value,
                )
            y += 16
            if y > sidebar.bottom - 32:
                break
