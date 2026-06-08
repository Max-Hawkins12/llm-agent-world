import pygame

from src.agents.agent import Agent, AgentResponse
from src.game_flow.enums import GameState
from src.game_flow.agent_factory import AgentBuilder
from src.environment.game import Game
from src.ui.menu import StartMenu
from src.ui.renderer import Renderer
from src.actions import GameAction, MenuAction
from src.input_mapper import get_menu_action

FPS = 60
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 640
CELL_SIZE = 64


class GameRunner:
    def __init__(self):
        pygame.init()
        pygame.key.set_repeat(0)

        max_game_height = max(WINDOW_HEIGHT, 10 * CELL_SIZE + 80)

        self.renderer = Renderer(WINDOW_WIDTH, max_game_height, 10, 10, CELL_SIZE)
        self.menu = StartMenu()
        self.game: Game | None = None
        self.agent: Agent | None = None

        self.state: GameState = GameState.MENU

    def run(self):
        while self.state != GameState.QUIT:

            if self.state == GameState.MENU:
                self.update_menu()
            elif self.state == GameState.RUNNING:
                self.update_game()
            elif self.state == GameState.END_SCREEN:
                self.update_end_screen()

            self.renderer.present(FPS)

        pygame.quit()

    def update_menu(self) -> None:
        events = self.poll_events()
        if self.state == GameState.QUIT:
            return

        action = get_menu_action(events)

        if action == MenuAction.QUIT:
            self.state = GameState.QUIT
            return
        elif action == MenuAction.START:
            self.start_game()
            self.state = GameState.RUNNING
        else:
            self.menu.process_action(action)

        self.renderer.render_menu(self.menu)

    def update_game(self) -> None:
        events = self.poll_events()
        if self.state == GameState.QUIT:
            return

        agent_response: AgentResponse = self.agent.get_action(
            events=events,
            game=self.game,
        )

        if agent_response.action.value != GameAction.WAIT.value:
            print("-------------------")
            print(agent_response)

        if agent_response.action == GameAction.QUIT:
            self.state = GameState.QUIT
            return
        elif agent_response.failure:
            self.state = GameState.END_SCREEN
            self.agent.game_ended_clean_up()
        else:
            self.game.process_action(agent_response.action)

        if self.game.has_finished():
            self.state = GameState.END_SCREEN
            self.agent.game_ended_clean_up()

        self.renderer.render_game(self.game)

    def update_end_screen(self) -> None:

        events = self.poll_events()

        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.state = GameState.QUIT

        self.renderer.render_end_screen(self.game)

    def start_game(self) -> None:
        self.game = Game(self.menu.build_game_settings())

        builder = AgentBuilder(self.menu.agent_type)
        self.agent = builder.build_agent()

        self.renderer.set_grid_size(self.game.grid_width, self.game.grid_height)

    def poll_events(self) -> list[pygame.event.Event]:
        events = pygame.event.get()

        if any(event.type == pygame.QUIT for event in events):
            self.state = GameState.QUIT

        return events
