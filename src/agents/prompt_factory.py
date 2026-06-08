import json
from typing import Tuple

from src.actions import GameAction


def build_prompt(observation: dict, previous_action: dict) -> str:
    previous_action_text = json.dumps(previous_action, indent=4)
    observation_text = json.dumps(observation, indent=4)

    return f"""You are an agent in a grid world.

World rules:
- You can defeat mobs by moving into them when you have the weapon.
- You cannot move into mobs without the weapon.
- The goal remains locked until all mobs are defeated.
- Mobs move one cell after every action.

Available actions:
- move_up
- move_down
- move_left
- move_right

Previous action:
{previous_action_text}

Current observation:
{observation_text}

Objective rules:

GET_WEAPON:
- Move toward the weapon.

HUNT_MOBS:
- Move toward the closest visible mob.
- Ignore the goal while any mobs remain alive.

REACH_GOAL:
- Move toward the goal.

Important rules:
- Choose exactly one action.
- Do not invent actions.
- Respond with valid JSON only.

Response format:
{{
    "action": "<action>",
    "reasoning": "<brief explanation>"
}}
"""


def parse_response(raw_response: str) -> Tuple[GameAction, str]:
    try:
        data = json.loads(raw_response)
    except json.JSONDecodeError:
        return (GameAction.INVALID, "ERROR: INVALID JSON")

    action = data.get("action")
    reasoning = data.get("reasoning")

    if action is None:
        return (GameAction.INVALID, "ERROR: NO ACTION")

    try:
        return (GameAction(action), reasoning)
    except ValueError:
        return (GameAction.INVALID, "ERROR: UNKOWN ACTION")
