from pygame.event import Event

from src.agents.agent import Agent, AgentResponse
from src.environment.game import Game
from src.actions import GameAction
from src.input_mapper import get_game_action


class HumanAgent(Agent):
    """Controller for a human player, which processes keyboard input to determine actions."""

    def get_action(self, game: Game, events: list[Event]) -> GameAction:
        return AgentResponse(get_game_action(events))

    def game_ended_clean_up(self):
        pass
