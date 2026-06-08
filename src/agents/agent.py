from pygame.event import Event
from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.environment.game import Game
from src.game_flow.enums import EndState
from src.actions import GameAction


@dataclass
class AgentResponse:
    action: GameAction
    reasoning: str | None = None
    failure: EndState | None = None

    def __str__(self):
        output = f"The agent performed: {self.action.value}"

        if self.reasoning:
            output += f"\nThis reasoning was given: {self.reasoning}"
        if self.failure:
            output += f"\nIt resulted in this game result: {self.result.value}"

        return output


class Agent(ABC):
    @abstractmethod
    def get_action(self, game: Game, events: list[Event]) -> AgentResponse:
        raise NotImplementedError

    @abstractmethod
    def game_ended_clean_up(self) -> None:
        raise NotImplementedError
