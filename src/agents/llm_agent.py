import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from typing import Optional, Tuple
from pygame.event import Event

from src.agents.agent import Agent, AgentResponse
from src.environment.game import Game
from src.game_flow.enums import EndState
from src.logger import RunLogger
from src.actions import GameAction
from src.game_options import AgentType

load_dotenv()


class LLMAgent(Agent):
    def __init__(self, agent_type: AgentType):
        super().__init__()

        if agent_type.requires_memory:
            self.memory: dict

        self.client = LLMClient()
        self.stats = AgentStatistics()

        self.logger = RunLogger(
            model_name=os.getenv("MODEL_NAME"), agent_type=agent_type
        )

    def get_action(self, game: Game, events: list[Event]) -> AgentResponse:
        observation = create_game_observation(game)

        prompt = build_prompt(observation)

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
        self.logger.log_ending(self.stats.turns, self.stats.end_state)


class AgentStatistics:

    TURNS_FOR_TIMEOUT = 25
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

    def query(self, prompt: str) -> str:
        response = self.client.responses.create(model=self.model, input=prompt)

        return response.output_text


def build_prompt(observation) -> str:
    observation_text = json.dumps(observation, indent=4, sort_keys=True)

    return f"""You are an agent in a grid world.
The world contains:
- A weapon
- Mobs
- A locked door

You can defeat mobs by moving into them when you have the weapon.
You cannot move into mobs without the weapon.
You must defeat all mobs to open the door.
A move up is (0, -1), a move down is (0, 1), a move left is (-1, 0), a move right is (1, 0)

Goal:
1. Obtain the weapon.
2. Defeat all mobs.
3. Reach the door.

Available actions:
- move_up
- move_down
- move_left
- move_right

Current observation:
{observation_text}

Important rules:
- Do not invent actions.
- Return valid JSON only.

Response format:
{{
"action": "<action>",
"reasoning": "<breif explanation>"
}}
"""


def parse_response(raw_response: str) -> Tuple[GameAction, str]:
    try:
        data = json.loads(raw_response)

        action = data.get("action")
        reasoning = data.get("reasoning")

        if action is None:
            return (GameAction.INVALID, reasoning)

        return (GameAction(action), reasoning)
    except (json.JSONDecodeError, ValueError):
        return (GameAction.INVALID, reasoning)


def create_game_observation(
    game: Game, agent_type: AgentType = AgentType.LLM_FULL
) -> dict:
    """
    Creates an observation of the game world for use by the LLM agent.
    With a full observation level the LLM can 'see' the entire game.
    With a local observation level the LLM can only 'see' things that are within 2 cells of its location.
    """

    if agent_type == AgentType.HUMAN:
        return None

    agent_pos = game.agent.position()
    weapon_pos = game.weapon.position() if game.weapon.alive else None
    goal_pos = game.goal.position()
    mob_pos = [m.position() for m in game.mobs if m.alive]

    observation = {
        "agent_type": agent_type.display_name,
        "position": agent_pos,
        "has_weapon": game.agent.has_weapon,
        "alive_mobs": game.total_alive_mobs(),
    }  # The agent will always knows where it is, if it has the weapon, how many mobs are left, and how much of the world its seeing

    if agent_type >= AgentType.LLM_LOCAL:
        if is_within_viewing_dist(agent_pos, goal_pos):
            observation["goal_position"] = goal_pos

        nearby_mobs = [p for p in mob_pos if is_within_viewing_dist(agent_pos, p)]
        if nearby_mobs:
            observation["mob_positions"] = nearby_mobs

        if weapon_pos and is_within_viewing_dist(agent_pos, weapon_pos):
            observation["weapon_position"] = weapon_pos
    else:
        observation["goal_position"] = goal_pos
        observation["mob_positions"] = mob_pos

        if weapon_pos:
            observation["weapon_position"] = weapon_pos

    return observation


def is_within_viewing_dist(
    agent_pos: tuple[int, int], obj_pos: tuple[int, int]
) -> bool:
    x, y = agent_pos
    ox, oy = obj_pos

    if abs(x - ox) + abs(y - oy) <= 2:
        return True

    return False
