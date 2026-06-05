from abc import ABC, abstractmethod
import pygame

from src.actions import Action


class AgentController(ABC):
    @abstractmethod
    def process_events(self, events: list[pygame.event.Event]) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_action(self) -> Action:
        raise NotImplementedError


class HumanController(AgentController):
    def __init__(self):
        self._action = Action.WAIT

    def process_events(self, events: list[pygame.event.Event]) -> None:
        self._action = Action.WAIT
        for event in events:
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_ESCAPE:
                self._action = Action.QUIT
                break
            if event.key in (pygame.K_UP, pygame.K_w):
                self._action = Action.MOVE_UP
                break
            if event.key in (pygame.K_DOWN, pygame.K_s):
                self._action = Action.MOVE_DOWN
                break
            if event.key in (pygame.K_LEFT, pygame.K_a):
                self._action = Action.MOVE_LEFT
                break
            if event.key in (pygame.K_RIGHT, pygame.K_d):
                self._action = Action.MOVE_RIGHT
                break

    def get_action(self) -> Action:
        action = self._action
        self._action = Action.WAIT
        return action
