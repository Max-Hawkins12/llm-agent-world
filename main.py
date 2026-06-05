import pygame

from src.actions import Action
from src.agents.human_controller import HumanController
from src.environment.game import Game, GameState
from src.ui.renderer import Renderer
from src.constants import FPS

if __name__ == "__main__":
    pygame.init()
    pygame.key.set_repeat(0)
    game = Game()
    renderer = Renderer()
    controller = HumanController()

    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        controller.process_events(events)
        action = controller.get_action()

        if action == Action.QUIT:
            running = False
        elif game.state == GameState.RUNNING and action != Action.WAIT:
            game.handle_action(action)

        renderer.draw(game, end_screen=(game.state != GameState.RUNNING))
        pygame.display.flip()
        renderer.clock.tick(FPS)

    pygame.quit()
