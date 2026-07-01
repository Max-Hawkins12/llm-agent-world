from __future__ import annotations

import pygame

from src.environment.game import Game
from src.app.experiment import ExperimentResult, RunResult, TurnRecord
from src.ui.context import RenderContext
from src.ui.end_renderer import EndScreenRenderer
from src.ui.experiment_renderer import ExperimentRenderer
from src.ui.grid_renderer import GridRenderer
from src.ui.menu import StartMenu
from src.ui.menu_renderer import MenuRenderer
from src.ui.results_renderer import ResultsRenderer


class Renderer:
    """Facade that owns the Pygame surface and delegates screen rendering."""

    def __init__(self, window_width: int = 1120, window_height: int = 760):
        self.screen = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption("LLM Agent Grid World Explorer")
        self.clock = pygame.time.Clock()

        self.context = RenderContext(self.screen, window_width, window_height)
        self.grid_renderer = GridRenderer(self.context)
        self.menu_renderer = MenuRenderer(self.context)
        self.experiment_renderer = ExperimentRenderer(
            self.context,
            self.grid_renderer,
        )
        self.end_renderer = EndScreenRenderer(self.context)
        self.results_renderer = ResultsRenderer(self.context)

    def present(self, fps: int) -> None:
        pygame.display.flip()
        self.clock.tick(fps)

    def hit_test(self, pos: tuple[int, int]) -> str | None:
        return self.context.hit_test(pos)

    def render_menu(self, menu: StartMenu) -> None:
        self.context.begin_frame()
        self.menu_renderer.render(menu)

    def render_game(
        self,
        game: Game,
        turns: list[TurnRecord],
        run_index: int,
        run_count: int,
    ) -> None:
        self.context.begin_frame()
        self.experiment_renderer.render(game, turns, run_index, run_count)

    def render_end_screen(self, result: ExperimentResult | None) -> None:
        self.context.begin_frame()
        self.end_renderer.render(result)

    def render_results(
        self,
        current_result: ExperimentResult | None,
        historical_results: list[RunResult],
        scroll_offset: int = 0,
    ) -> None:
        self.context.begin_frame()
        self.results_renderer.render(
            current_result,
            historical_results,
            scroll_offset,
        )
