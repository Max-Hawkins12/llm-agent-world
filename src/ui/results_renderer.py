from __future__ import annotations

from pathlib import Path

import pygame

from src.app.experiment import ExperimentResult, RunResult
from src.ui.colours import UIColour
from src.ui.context import RenderContext


class ResultsRenderer:
    def __init__(self, context: RenderContext):
        self.context = context

    def render(
        self,
        current_result: ExperimentResult | None,
        historical_results: list[RunResult],
        scroll_offset: int = 0,
    ) -> None:
        ctx = self.context
        ctx.draw_text("Results", 42, 32, ctx.large_font)
        ctx.draw_button(
            "back_to_end", pygame.Rect(ctx.window_width - 250, 36, 90, 38), "Back"
        )
        ctx.draw_button(
            "restart", pygame.Rect(ctx.window_width - 148, 36, 106, 38), "Restart"
        )

        left = pygame.Rect(38, 96, 500, ctx.window_height - 126)
        right = pygame.Rect(568, 96, ctx.window_width - 606, ctx.window_height - 126)
        ctx.draw_panel(left)
        ctx.draw_panel(right)

        self._draw_current_results(left, current_result)
        self._draw_historical_results(right, historical_results, scroll_offset)

    def _draw_current_results(
        self,
        panel: pygame.Rect,
        current_result: ExperimentResult | None,
    ) -> None:
        ctx = self.context
        ctx.draw_text("Current Experiment", panel.x + 20, panel.y + 18, ctx.title_font)
        y = panel.y + 62

        if not current_result or not current_result.runs:
            ctx.draw_text(
                "No current results.",
                panel.x + 20,
                y,
                ctx.font,
                UIColour.MUTED_TEXT.value,
            )
            return

        summary = [
            f"Grid: {current_result.config.grid_type.display_name}",
            f"Agent: {current_result.config.agent_type.display_name}",
            f"Runs: {current_result.total_runs}",
            f"Successes: {current_result.successes}",
            f"Failures: {current_result.failures}",
            f"Average turns: {current_result.average_turns:.1f}",
            f"Invalid inputs: {current_result.total_invalid_inputs}",
            f"Tokens: {current_result.total_input_tokens} in / {current_result.total_output_tokens} out",
        ]
        ctx.draw_lines(summary, panel.x + 20, y, 27)
        y += len(summary) * 27 + 16

        for run in current_result.runs:
            text = (
                f"Run {run.run_index}: {run.end_state.value}, "
                f"{run.turns} turns, {run.invalid_inputs} invalid"
            )
            y = ctx.draw_wrapped_text(
                text, panel.x + 20, y, panel.width - 40, ctx.small_font
            )
            y += 8

    def _draw_historical_results(
        self,
        panel: pygame.Rect,
        historical_results: list[RunResult],
        scroll_offset: int,
    ) -> None:
        ctx = self.context
        ctx.draw_text("Historical Logs", panel.x + 20, panel.y + 18, ctx.title_font)
        y = panel.y + 62 - scroll_offset

        if not historical_results:
            ctx.draw_text(
                "No parseable logs found.",
                panel.x + 20,
                y,
                ctx.font,
                UIColour.MUTED_TEXT.value,
            )
            return

        for run in historical_results[:80]:
            if y > panel.y + 48 and y < panel.bottom - 18:
                name = run.log_path.name if isinstance(run.log_path, Path) else "log"
                text = (
                    f"{name}: {run.end_state.value}, "
                    f"{run.turns} turns, {run.invalid_inputs} invalid"
                )
                ctx.draw_wrapped_text(
                    text, panel.x + 20, y, panel.width - 40, ctx.small_font
                )
            y += 46
