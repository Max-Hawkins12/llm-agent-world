from __future__ import annotations

import pygame

from src.app.experiment import ExperimentResult
from src.ui.context import RenderContext


class EndScreenRenderer:
    def __init__(self, context: RenderContext):
        self.context = context

    def render(self, result: ExperimentResult | None) -> None:
        ctx = self.context
        panel = pygame.Rect(250, 120, 620, 460)
        ctx.draw_panel(panel)

        ctx.draw_text("Experiment Complete", panel.x + 36, panel.y + 34, ctx.large_font)

        if result and result.runs:
            lines = [
                f"Runs: {result.total_runs}",
                f"Successes: {result.successes}",
                f"Failures: {result.failures}",
                f"Total turns: {result.total_turns}",
                f"Average turns: {result.average_turns:.1f}",
                f"Invalid inputs: {result.total_invalid_inputs}",
                f"Input tokens: {result.total_input_tokens}",
                f"Output tokens: {result.total_output_tokens}",
            ]
        else:
            lines = ["No completed runs yet."]

        ctx.draw_lines(lines, panel.x + 40, panel.y + 110, 30)
        ctx.draw_button(
            "restart", pygame.Rect(panel.x + 40, panel.bottom - 76, 140, 44), "Restart"
        )
        ctx.draw_button(
            "results",
            pygame.Rect(panel.x + 198, panel.bottom - 76, 170, 44),
            "View Results",
        )
        ctx.draw_button(
            "quit", pygame.Rect(panel.x + 386, panel.bottom - 76, 120, 44), "Exit"
        )
