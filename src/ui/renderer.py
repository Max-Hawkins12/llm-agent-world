from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import pygame

from src.environment.entities import Door, Goal, Key, Mob, Player, Wall, Weapon
from src.environment.game import Game
from src.game_flow.experiment import ExperimentResult, RunResult, TurnRecord
from src.ui.colours import UIColour
from src.ui.menu import StartMenu


@dataclass(frozen=True)
class GridLayout:
    offset_x: int
    offset_y: int
    cell_size: int
    width: int
    height: int


class Renderer:
    def __init__(self, window_width: int = 1120, window_height: int = 760):
        self.screen = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption("LLM Agent Grid World Explorer")
        self.clock = pygame.time.Clock()

        self.window_width = window_width
        self.window_height = window_height
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 20)
        self.large_font = pygame.font.Font(None, 42)
        self.title_font = pygame.font.Font(None, 34)

        self.click_regions: dict[str, pygame.Rect] = {}

    def present(self, fps: int) -> None:
        pygame.display.flip()
        self.clock.tick(fps)

    def hit_test(self, pos: tuple[int, int]) -> str | None:
        for action_id, rect in reversed(self.click_regions.items()):
            if rect.collidepoint(pos):
                return action_id
        return None

    def render_menu(self, menu: StartMenu) -> None:
        self._begin_frame()
        config = menu.build_config()

        self._draw_text("LLM Agent Grid World Explorer", 48, 42, self.large_font)
        self._draw_text(
            "Configure an experiment, then run each attempt live.",
            50,
            88,
            self.font,
            UIColour.MUTED_TEXT.value,
        )

        panel = pygame.Rect(48, 132, 570, 500)
        self._draw_panel(panel)

        y = panel.y + 28
        for index, option in enumerate(menu.options):
            selected = index == menu.selected_index
            row = pygame.Rect(panel.x + 18, y - 8, panel.width - 36, 44)
            if selected:
                pygame.draw.rect(self.screen, UIColour.PANEL_LIGHT.value, row, border_radius=6)
            self.click_regions[f"menu:select:{index}"] = row

            self._draw_text(option.label, row.x + 12, y + 4, self.font)
            self._draw_button(
                f"menu:prev:{index}",
                pygame.Rect(row.right - 178, row.y + 6, 34, 30),
                "<",
                compact=True,
            )
            value_rect = pygame.Rect(row.right - 138, row.y + 6, 98, 30)
            pygame.draw.rect(self.screen, UIColour.PANEL_DARK.value, value_rect, border_radius=5)
            self._draw_centered_text(option.display_value, value_rect, self.small_font)
            self._draw_button(
                f"menu:next:{index}",
                pygame.Rect(row.right - 34, row.y + 6, 34, 30),
                ">",
                compact=True,
            )
            y += 58

        start_enabled = config.is_supported()
        self._draw_button(
            "start",
            pygame.Rect(panel.x + 18, panel.bottom - 64, 170, 42),
            "Start",
            enabled=start_enabled,
        )
        self._draw_button(
            "quit",
            pygame.Rect(panel.x + 204, panel.bottom - 64, 130, 42),
            "Quit",
        )

        details = pygame.Rect(660, 132, 410, 500)
        self._draw_panel(details)
        self._draw_text("Experiment", details.x + 22, details.y + 22, self.title_font)
        lines = [
            f"Grid: {config.grid_type.display_name}",
            f"Size: {config.grid_size[0]} x {config.grid_size[1]}",
            f"Agent: {config.agent_type.display_name}",
            f"Runs: {config.run_count}",
            f"Mobs: {config.mob_count}",
            f"Door sections: {config.section_count}",
        ]
        self._draw_lines(lines, details.x + 24, details.y + 78, 28)

        status = config.disabled_reason or "Ready to start."
        status_colour = UIColour.ERROR.value if config.disabled_reason else UIColour.SUCCESS.value
        self._draw_wrapped_text(status, details.x + 24, details.bottom - 86, details.width - 48, self.font, status_colour)

        self._draw_text(
            "Keyboard: arrows/WASD change settings, SPACE starts, ESC quits.",
            52,
            self.window_height - 54,
            self.small_font,
            UIColour.MUTED_TEXT.value,
        )

    def render_game(
        self,
        game: Game,
        turns: list[TurnRecord],
        run_index: int,
        run_count: int,
    ) -> None:
        self._begin_frame()

        sidebar = pygame.Rect(20, 20, 330, self.window_height - 40)
        self._draw_panel(sidebar)
        self._draw_text("LLM Responses", sidebar.x + 18, sidebar.y + 18, self.title_font)

        if turns:
            y = sidebar.y + 62
            for turn in list(reversed(turns))[:9]:
                colour = UIColour.ERROR.value if turn.is_invalid or turn.failure else UIColour.TEXT.value
                header = f"Run {turn.run_index} Turn {turn.turn_number}: {turn.action.value}"
                y = self._draw_wrapped_text(header, sidebar.x + 18, y, sidebar.width - 36, self.small_font, colour)
                if turn.reasoning:
                    y = self._draw_wrapped_text(turn.reasoning, sidebar.x + 18, y + 4, sidebar.width - 36, self.small_font, UIColour.MUTED_TEXT.value)
                if turn.outcome:
                    y = self._draw_wrapped_text(f"Outcome: {turn.outcome}", sidebar.x + 18, y + 4, sidebar.width - 36, self.small_font, UIColour.MUTED_TEXT.value)
                y += 16
                if y > sidebar.bottom - 32:
                    break
        else:
            self._draw_wrapped_text("Waiting for the first action.", sidebar.x + 18, sidebar.y + 64, sidebar.width - 36, self.font, UIColour.MUTED_TEXT.value)

        header = pygame.Rect(380, 20, self.window_width - 410, 58)
        self._draw_panel(header)
        active_turns = sum(1 for turn in turns if turn.run_index == run_index)
        status = f"Run {run_index} / {run_count}    Turn {active_turns}    Grid {game.grid_width} x {game.grid_height}"
        self._draw_text(status, header.x + 18, header.y + 19, self.font)

        grid_area = pygame.Rect(380, 102, self.window_width - 410, self.window_height - 122)
        layout = self._grid_layout(game, grid_area)
        self._draw_grid(game, layout)
        for entity in game.get_alive_entities():
            self._draw_entity(entity, layout)

    def render_end_screen(self, result: ExperimentResult | None) -> None:
        self._begin_frame()
        panel = pygame.Rect(250, 120, 620, 460)
        self._draw_panel(panel)

        self._draw_text("Experiment Complete", panel.x + 36, panel.y + 34, self.large_font)

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

        self._draw_lines(lines, panel.x + 40, panel.y + 110, 30)
        self._draw_button("restart", pygame.Rect(panel.x + 40, panel.bottom - 76, 140, 44), "Restart")
        self._draw_button("results", pygame.Rect(panel.x + 198, panel.bottom - 76, 170, 44), "View Results")
        self._draw_button("quit", pygame.Rect(panel.x + 386, panel.bottom - 76, 120, 44), "Exit")

    def render_results(
        self,
        current_result: ExperimentResult | None,
        historical_results: list[RunResult],
        scroll_offset: int = 0,
    ) -> None:
        self._begin_frame()
        self._draw_text("Results", 42, 32, self.large_font)
        self._draw_button("back_to_end", pygame.Rect(self.window_width - 250, 36, 90, 38), "Back")
        self._draw_button("restart", pygame.Rect(self.window_width - 148, 36, 106, 38), "Restart")

        left = pygame.Rect(38, 96, 500, self.window_height - 126)
        right = pygame.Rect(568, 96, self.window_width - 606, self.window_height - 126)
        self._draw_panel(left)
        self._draw_panel(right)

        self._draw_text("Current Experiment", left.x + 20, left.y + 18, self.title_font)
        y = left.y + 62
        if current_result and current_result.runs:
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
            self._draw_lines(summary, left.x + 20, y, 27)
            y += len(summary) * 27 + 16
            for run in current_result.runs:
                text = f"Run {run.run_index}: {run.end_state.value}, {run.turns} turns, {run.invalid_inputs} invalid"
                y = self._draw_wrapped_text(text, left.x + 20, y, left.width - 40, self.small_font)
                y += 8
        else:
            self._draw_text("No current results.", left.x + 20, y, self.font, UIColour.MUTED_TEXT.value)

        self._draw_text("Historical Logs", right.x + 20, right.y + 18, self.title_font)
        y = right.y + 62 - scroll_offset
        if historical_results:
            for run in historical_results[:80]:
                if y > right.y + 48 and y < right.bottom - 18:
                    name = run.log_path.name if isinstance(run.log_path, Path) else "log"
                    text = f"{name}: {run.end_state.value}, {run.turns} turns, {run.invalid_inputs} invalid"
                    self._draw_wrapped_text(text, right.x + 20, y, right.width - 40, self.small_font)
                y += 46
        else:
            self._draw_text("No parseable logs found.", right.x + 20, y, self.font, UIColour.MUTED_TEXT.value)

    def _begin_frame(self) -> None:
        self.click_regions = {}
        self.screen.fill(UIColour.BG.value)

    def _grid_layout(self, game: Game, area: pygame.Rect) -> GridLayout:
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
                entity = game.grid.grid[y][x]
                colour = UIColour.WALL.value if isinstance(entity, Wall) else UIColour.TILE.value
                if isinstance(entity, Goal):
                    colour = UIColour.GOAL.value
                elif isinstance(entity, Door):
                    colour = UIColour.DOOR.value
                pygame.draw.rect(self.screen, colour, rect)
                pygame.draw.rect(self.screen, UIColour.GRID_LINE.value, rect, 1)

    def _draw_entity(self, entity, layout: GridLayout) -> None:
        x = entity.position.x
        y = entity.position.y
        rect = self._cell_rect(layout, x, y).inflate(-8, -8)

        if isinstance(entity, Player):
            pygame.draw.circle(self.screen, UIColour.PLAYER.value, rect.center, max(5, rect.width // 2))
            if getattr(entity, "held_item", None) is not None:
                pygame.draw.circle(self.screen, UIColour.KEY.value, rect.center, max(7, rect.width // 2), 3)
        elif isinstance(entity, Mob):
            pygame.draw.circle(self.screen, UIColour.MOB.value, rect.center, max(5, rect.width // 2))
        elif isinstance(entity, Key):
            pygame.draw.rect(self.screen, UIColour.KEY.value, rect, border_radius=4)
            self._draw_centered_text("K", rect, self.small_font, UIColour.BLACK.value)
        elif isinstance(entity, Weapon):
            pygame.draw.rect(self.screen, UIColour.WEAPON.value, rect, border_radius=4)
            self._draw_centered_text("W", rect, self.small_font, UIColour.BLACK.value)

    def _cell_rect(self, layout: GridLayout, x: int, y: int) -> pygame.Rect:
        return pygame.Rect(
            layout.offset_x + x * layout.cell_size,
            layout.offset_y + y * layout.cell_size,
            layout.cell_size,
            layout.cell_size,
        )

    def _draw_panel(self, rect: pygame.Rect) -> None:
        pygame.draw.rect(self.screen, UIColour.PANEL.value, rect, border_radius=8)
        pygame.draw.rect(self.screen, UIColour.BORDER.value, rect, 1, border_radius=8)

    def _draw_button(
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
        self._draw_centered_text(label, rect, self.small_font if compact else self.font, text_colour)
        if enabled:
            self.click_regions[action_id] = rect

    def _draw_text(
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

    def _draw_centered_text(
        self,
        text: str,
        rect: pygame.Rect,
        font: pygame.font.Font,
        colour: tuple[int, int, int] = UIColour.TEXT.value,
    ) -> None:
        surface = font.render(str(text), True, colour)
        text_rect = surface.get_rect(center=rect.center)
        self.screen.blit(surface, text_rect)

    def _draw_lines(
        self,
        lines: Iterable[str],
        x: int,
        y: int,
        line_height: int,
        colour: tuple[int, int, int] = UIColour.TEXT.value,
    ) -> None:
        for index, line in enumerate(lines):
            self._draw_text(line, x, y + index * line_height, self.font, colour)

    def _draw_wrapped_text(
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

            self._draw_text(line, x, y, font, colour)
            y += line_height
            line = word

        if line:
            self._draw_text(line, x, y, font, colour)
            y += line_height

        return y
