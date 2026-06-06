from abc import ABC, abstractmethod

from src.actions import GameAction


class Agent(ABC):
    @abstractmethod
    def get_action(self, context) -> GameAction:
        raise NotImplementedError
