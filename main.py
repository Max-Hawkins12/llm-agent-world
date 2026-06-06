from enum import Enum
import pygame

from src.actions import GameAction, MenuAction
from src.agents.human_agent import HumanAgent
from src.environment.game import Game
from src.ui.menu import StartMenu, parse_menu_action
from src.ui.renderer import Renderer


class GameState(Enum):
    MENU = "menu"
    RUNNING = "running"
    FINISHED = "finished"
    QUIT = "quit"


FPS = 60
MENU_WIDTH = 800
MENU_HEIGHT = 640
CELL_SIZE = 64


def _check_for_quit(
    events: list[pygame.event.Event], game_state: GameState
) -> GameState:
    """Check the list of events for a quit event. If found, return GameState.QUIT to indicate the game should exit."""
    for event in events:
        if event.type == pygame.QUIT:
            return GameState.QUIT
    return game_state


def _refresh_screen(renderer: Renderer) -> None:
    pygame.display.flip()
    renderer.clock.tick(FPS)


if __name__ == "__main__":
    pygame.init()
    pygame.key.set_repeat(0)

    max_game_height = max(MENU_HEIGHT, 10 * CELL_SIZE + 80)
    renderer = Renderer(MENU_WIDTH, max_game_height, 10, 10, CELL_SIZE)
    game_state = GameState.MENU
    menu = StartMenu()

    while game_state != GameState.QUIT:
        while game_state == GameState.MENU:
            events = pygame.event.get()
            game_state = _check_for_quit(events, game_state)

            action = parse_menu_action(events)
            if action == MenuAction.QUIT:
                game_state = GameState.QUIT
                break
            elif action == MenuAction.START:
                game_state = GameState.RUNNING
            else:
                menu.process_action(action)

            renderer.draw_menu(menu)
            _refresh_screen(renderer)

        game = Game(menu.build_game_settings())
        agent = HumanAgent()  # TODO NOT IMPLEMENTED: different agent types
        renderer.set_grid_size(game.grid_width, game.grid_height)
        renderer.draw_game(game)

        while game_state == GameState.RUNNING:
            events = pygame.event.get()
            game_state = _check_for_quit(events, game_state)

            action = agent.get_action({"events": events, "game_state": game})

            if action == GameAction.QUIT:
                game_state = GameState.QUIT
                break
            elif action != GameAction.QUIT:
                game.process_action(action)
                game_state = (
                    GameState.FINISHED if game.has_finished() else GameState.RUNNING
                )

            renderer.draw_game(game)
            _refresh_screen(renderer)

        while game_state == GameState.FINISHED:
            events = pygame.event.get()
            game_state = _check_for_quit(events, game_state)

            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_state = GameState.QUIT

            renderer.draw_end_screen(game)
            _refresh_screen(renderer)

    pygame.quit()
