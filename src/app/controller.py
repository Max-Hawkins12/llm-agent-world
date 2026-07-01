from __future__ import annotations

import pygame

from src.actions import GameAction, MenuAction
from src.agents.agent import Agent, AgentResponse
from src.environment.game import Game
from src.agents.factory import AgentBuilder
from src.app.states import EndState, GameState
from src.app.experiment import (
    ExperimentConfig,
    ExperimentResult,
    RunResult,
    TurnRecord,
    load_historical_results,
)
from src.input_mapper import get_menu_action
from src.ui.menu import StartMenu
from src.ui.renderer import Renderer

FPS = 60


class AppController:
    def __init__(self):
        pygame.init()
        pygame.key.set_repeat(0)

        self.renderer = Renderer()
        self.menu = StartMenu()

        self.state: GameState = GameState.START_MENU
        self.config: ExperimentConfig | None = None
        self.result: ExperimentResult | None = None
        self.historical_results = load_historical_results()

        self.game: Game | None = None
        self.agent: Agent | None = None
        self.current_run_index = 0
        self.current_run_turns: list[TurnRecord] = []
        self.all_turns: list[TurnRecord] = []
        self.results_scroll = 0

    def run(self) -> None:
        while self.state != GameState.QUIT:
            if self.state == GameState.START_MENU:
                self.update_menu()
            elif self.state == GameState.RUNNING:
                self.update_game()
            elif self.state == GameState.END_SCREEN:
                self.update_end_screen()
            elif self.state == GameState.RESULTS:
                self.update_results()

            self.renderer.present(FPS)

        pygame.quit()

    def update_menu(self) -> None:
        events = self.poll_events()
        if self.state == GameState.QUIT:
            return

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                action_id = self.renderer.hit_test(event.pos)
                if action_id == "start":
                    self.start_experiment()
                elif action_id == "quit":
                    self.state = GameState.QUIT
                elif action_id:
                    self.menu.process_click(action_id)

        action = get_menu_action(events)
        if action == MenuAction.QUIT:
            self.state = GameState.QUIT
        elif action == MenuAction.START:
            self.start_experiment()
        else:
            self.menu.process_action(action)

        self.renderer.render_menu(self.menu)

    def update_game(self) -> None:
        events = self.poll_events()
        if self.state == GameState.QUIT:
            return

        assert self.game is not None
        assert self.agent is not None
        assert self.config is not None

        response: AgentResponse = self.agent.get_action(events=events, game=self.game)

        if response.action == GameAction.QUIT:
            self.state = GameState.QUIT
            return

        if response.action != GameAction.WAIT:
            if response.failure is None:
                self.game.process_action(response.action)
            else:
                self.game.action_outcome.action_name = response.action.value
                self.game.action_outcome.outcome = response.failure.value

            self.record_turn(response)

        if response.failure:
            self.finish_run(response.failure)
        elif self.game.has_finished():
            self.finish_run(EndState.WIN)

        if self.state == GameState.RUNNING and self.game is not None:
            self.renderer.render_game(
                self.game,
                self.all_turns,
                self.current_run_index,
                self.config.run_count,
            )

    def update_end_screen(self) -> None:
        events = self.poll_events()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = GameState.QUIT
                elif event.key == pygame.K_r:
                    self.reset_to_menu()
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self.state = GameState.RESULTS
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                action_id = self.renderer.hit_test(event.pos)
                if action_id == "restart":
                    self.reset_to_menu()
                elif action_id == "results":
                    self.historical_results = load_historical_results()
                    self.state = GameState.RESULTS
                elif action_id == "quit":
                    self.state = GameState.QUIT

        self.renderer.render_end_screen(self.result)

    def update_results(self) -> None:
        events = self.poll_events()
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.state = GameState.END_SCREEN
            elif event.type == pygame.MOUSEWHEEL:
                self.results_scroll = max(0, self.results_scroll - event.y * 28)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                action_id = self.renderer.hit_test(event.pos)
                if action_id == "back_to_end":
                    self.state = GameState.END_SCREEN
                elif action_id == "restart":
                    self.reset_to_menu()

        self.renderer.render_results(
            self.result,
            self.historical_results,
            self.results_scroll,
        )

    def start_experiment(self) -> None:
        config = self.menu.build_config()
        if not config.is_supported():
            return

        self.config = config
        self.result = ExperimentResult(config=config)
        self.current_run_index = 0
        self.current_run_turns = []
        self.all_turns = []
        self.start_next_run()

    def start_next_run(self) -> None:
        assert self.config is not None

        self.current_run_index += 1
        self.game = self.config.build_game(self.current_run_index)
        self.agent = AgentBuilder(self.config.agent_type).build_agent()
        self.current_run_turns = []
        self.state = GameState.RUNNING

    def record_turn(self, response: AgentResponse) -> None:
        assert self.game is not None
        assert self.agent is not None

        input_tokens, output_tokens = self.agent.token_totals()
        turn_number = len(self.current_run_turns) + 1
        record = TurnRecord(
            run_index=self.current_run_index,
            turn_number=turn_number,
            action=response.action,
            reasoning=response.reasoning,
            outcome=self.game.action_outcome.outcome,
            failure=response.failure,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
        )
        self.current_run_turns.append(record)
        self.all_turns.append(record)

    def finish_run(self, end_state: EndState) -> None:
        assert self.config is not None
        assert self.result is not None
        assert self.agent is not None

        self.agent.game_ended_clean_up()
        input_tokens, output_tokens = self.agent.token_totals()
        invalid_inputs = self.agent.invalid_count()
        if invalid_inputs == 0:
            invalid_inputs = sum(
                1 for turn in self.current_run_turns if turn.is_invalid
            )

        run_result = RunResult(
            run_index=self.current_run_index,
            end_state=end_state,
            turns=len(self.current_run_turns),
            invalid_inputs=invalid_inputs,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            log_path=self.agent.log_path(),
            turns_detail=list(self.current_run_turns),
        )
        self.result.add_run(run_result)

        if self.current_run_index < self.config.run_count:
            self.start_next_run()
        else:
            self.historical_results = load_historical_results()
            self.state = GameState.END_SCREEN

    def reset_to_menu(self) -> None:
        self.game = None
        self.agent = None
        self.config = None
        self.current_run_index = 0
        self.current_run_turns = []
        self.all_turns = []
        self.results_scroll = 0
        self.state = GameState.START_MENU

    def poll_events(self) -> list[pygame.event.Event]:
        events = pygame.event.get()
        if any(event.type == pygame.QUIT for event in events):
            self.state = GameState.QUIT
        return events
