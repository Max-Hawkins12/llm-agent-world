from __future__ import annotations

import pygame

from src.ui.colours import UIColour
from src.ui.context import RenderContext
from src.ui.menu import StartMenu


class MenuRenderer:
    def __init__(self, context: RenderContext):
        self.context = context

    def render(self, menu: StartMenu) -> None:
        ctx = self.context
        config = menu.build_config()

        ctx.draw_text("LLM Agent Grid World Explorer", 48, 42, ctx.large_font)
        ctx.draw_text(
            "Configure an experiment, then run each attempt live.",
            50,
            88,
            ctx.font,
            UIColour.MUTED_TEXT.value,
        )

        panel = pygame.Rect(48, 132, 570, 500)
        ctx.draw_panel(panel)

        y = panel.y + 28
        for index, option in enumerate(menu.options):
            selected = index == menu.selected_index
            row = pygame.Rect(panel.x + 18, y - 8, panel.width - 36, 44)
            if selected:
                pygame.draw.rect(
                    ctx.screen, UIColour.PANEL_LIGHT.value, row, border_radius=6
                )
            ctx.register_click(f"menu:select:{index}", row)

            ctx.draw_text(option.label, row.x + 12, y + 4, ctx.font)
            ctx.draw_button(
                f"menu:prev:{index}",
                pygame.Rect(row.right - 178, row.y + 6, 34, 30),
                "<",
                compact=True,
            )
            value_rect = pygame.Rect(row.right - 138, row.y + 6, 98, 30)
            pygame.draw.rect(
                ctx.screen, UIColour.PANEL_DARK.value, value_rect, border_radius=5
            )
            ctx.draw_centered_text(option.display_value, value_rect, ctx.small_font)
            ctx.draw_button(
                f"menu:next:{index}",
                pygame.Rect(row.right - 34, row.y + 6, 34, 30),
                ">",
                compact=True,
            )
            y += 58

        ctx.draw_button(
            "start",
            pygame.Rect(panel.x + 18, panel.bottom - 64, 170, 42),
            "Start",
            enabled=config.is_supported(),
        )
        ctx.draw_button(
            "quit",
            pygame.Rect(panel.x + 204, panel.bottom - 64, 130, 42),
            "Quit",
        )

        details = pygame.Rect(660, 132, 410, 500)
        ctx.draw_panel(details)
        ctx.draw_text("Experiment", details.x + 22, details.y + 22, ctx.title_font)
        lines = [
            f"Grid: {config.grid_type.display_name}",
            f"Size: {config.grid_size[0]} x {config.grid_size[1]}",
            f"Agent: {config.agent_type.display_name}",
            f"Runs: {config.run_count}",
            f"Mobs: {config.mob_count}",
            f"Door sections: {config.section_count}",
        ]
        ctx.draw_lines(lines, details.x + 24, details.y + 78, 28)

        status = config.disabled_reason or "Ready to start."
        status_colour = (
            UIColour.ERROR.value if config.disabled_reason else UIColour.SUCCESS.value
        )
        ctx.draw_wrapped_text(
            status,
            details.x + 24,
            details.bottom - 86,
            details.width - 48,
            ctx.font,
            status_colour,
        )

        ctx.draw_text(
            "Keyboard: arrows/WASD change settings, SPACE starts, ESC quits.",
            52,
            ctx.window_height - 54,
            ctx.small_font,
            UIColour.MUTED_TEXT.value,
        )
