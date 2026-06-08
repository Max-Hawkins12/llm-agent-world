import os
from dotenv import load_dotenv
from openai import OpenAI
from typing import Optional
from pygame.event import Event

from src.agents.agent import Agent, AgentResponse
from src.agents.logger import RunLogger
from src.agents.observation_factory import build_game_observation
from src.agents.prompt_factory import build_prompt, parse_response
from src.environment.game import Game
from src.game_flow.enums import EndState
from src.actions import GameAction

load_dotenv()


class LLMAgent(Agent):
    def __init__(self):
        super().__init__()

        self.client = LLMClient()
        self.stats = AgentStatistics()

        self.logger = RunLogger(model_name=os.getenv("MODEL_NAME"))

    def get_action(self, game: Game, events: list[Event]) -> AgentResponse:
        observation = build_game_observation(game)

        prompt = build_prompt(
            observation=observation,
            previous_action=game.return_previous_action_outcome(),
        )

        raw_response = self.client.query(prompt)

        action, resoning = parse_response(raw_response)

        self.logger.log_turn(
            self.stats.turns,
            observation,
            prompt,
            raw_response,
            action,
            resoning,
        )

        outcome = self.stats.check_invalids(action)

        if not outcome:
            outcome = AgentResponse(action, reasoning=resoning)

        return outcome

    def game_ended_clean_up(self):
        self.logger.log_ending(
            self.stats.turns,
            self.stats.end_state,
            self.client.total_input_tokens,
            self.client.total_output_tokens,
        )


class AgentStatistics:
    TURNS_FOR_TIMEOUT = 100
    TOTAL_ALLOWED_INVALIDS = 10
    TOTAL_ALLOWED_CONSECUTIVE_INVALIDS = 3

    def __init__(self):
        self.turns = 0
        self.total_invalids = 0
        self.consecutive_invalids = 0
        self.end_state: EndState = EndState.WIN

    def check_invalids(self, action: GameAction) -> Optional[AgentResponse]:
        self.turns += 1

        if action == GameAction.INVALID:
            self.total_invalids += 1
            self.consecutive_invalids += 1
        else:
            self.consecutive_invalids = 0

        if self.total_invalids >= self.TOTAL_ALLOWED_INVALIDS:
            self.end_state = EndState.TOO_MANY_INVALIDS
            return AgentResponse(action, failure=EndState.TOO_MANY_INVALIDS)
        elif self.consecutive_invalids >= self.TOTAL_ALLOWED_CONSECUTIVE_INVALIDS:
            self.end_state = EndState.TOO_MANY_CONSECUTIVE_INVALIDS
            return AgentResponse(action, failure=EndState.TOO_MANY_CONSECUTIVE_INVALIDS)
        elif self.turns >= self.TURNS_FOR_TIMEOUT:
            self.end_state = EndState.TIMEOUT
            return AgentResponse(action, failure=EndState.TIMEOUT)
        else:
            return None


class LLMClient:
    def __init__(self):
        self.client = OpenAI()
        self.model = os.getenv("MODEL_NAME")

        self.total_input_tokens = 0
        self.total_output_tokens = 0

    def query(self, prompt: str) -> str:
        response = self.client.responses.create(model=self.model, input=prompt)

        self.total_input_tokens += response.usage.input_tokens
        self.total_output_tokens += response.usage.output_tokens

        return response.output_text
