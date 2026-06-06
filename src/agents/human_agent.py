import pygame

from src.agents.agent import Agent
from src.actions import GameAction


class HumanAgent(Agent):
    """Controller for a human player, which processes keyboard input to determine actions."""

    def get_action(self, context) -> GameAction:
        events = context["events"]

        for event in events:
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_ESCAPE:
                return GameAction.QUIT
            if event.key in (pygame.K_UP, pygame.K_w):
                return GameAction.MOVE_UP
            if event.key in (pygame.K_DOWN, pygame.K_s):
                return GameAction.MOVE_DOWN
            if event.key in (pygame.K_LEFT, pygame.K_a):
                return GameAction.MOVE_LEFT
            if event.key in (pygame.K_RIGHT, pygame.K_d):
                return GameAction.MOVE_RIGHT

        return GameAction.WAIT
