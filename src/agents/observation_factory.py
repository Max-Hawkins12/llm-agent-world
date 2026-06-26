from src.environment.game_old import Game
from src.environment.utils import Position
from src.game_options import AgentType


def build_game_observation(
    game: Game, agent_type: AgentType = AgentType.LLM_OBJECTIVE
) -> dict:
    if agent_type == AgentType.HUMAN:
        return None

    agent_pos = game.agent.position
    weapon_pos = game.weapon.position if game.weapon.alive else None
    goal_pos = game.goal.position
    mob_pos = [m.position for m in game.mobs if m.alive]

    closest_mob_pos = None

    if mob_pos:
        closest_mob_pos = min(mob_pos, key=lambda p: manhattan_distance(agent_pos, p))

    observation = {
        "current_objective": (
            "GET_WEAPON"
            if not game.agent.has_weapon
            else "HUNT_MOBS" if game.total_alive_mobs() > 0 else "REACH_GOAL"
        ),
        "has_weapon": game.agent.has_weapon,
        "alive_mobs": game.total_alive_mobs(),
    }

    if not game.agent.has_weapon:
        observation = add_direction_and_distance(
            dict=observation,
            obj_name="weapon",
            obj_pos=weapon_pos,
            agent_pos=agent_pos,
        )
    elif game.goal.locked:
        observation = add_direction_and_distance(
            dict=observation,
            obj_name="closest_mob",
            obj_pos=closest_mob_pos,
            agent_pos=agent_pos,
        )
    else:
        observation = add_direction_and_distance(
            dict=observation,
            obj_name="goal",
            obj_pos=goal_pos,
            agent_pos=agent_pos,
        )

    return observation


def add_direction_and_distance(
    dict: dict, obj_name: str, obj_pos: Position, agent_pos: Position
) -> dict:
    dict[f"{obj_name}_direction"] = get_direction(agent_pos, obj_pos)
    dict[f"{obj_name}_distance"] = manhattan_distance(agent_pos, obj_pos)
    return dict


def get_direction(agent_pos: Position, obj_pos: Position) -> str:
    horizontal = ""
    vertical = ""

    if obj_pos.x > agent_pos.x:
        horizontal = "RIGHT"
    elif obj_pos.x < agent_pos.x:
        horizontal = "LEFT"

    if obj_pos.y > agent_pos.y:
        vertical = "DOWN"
    elif obj_pos.y < agent_pos.y:
        vertical = "UP"

    if vertical and horizontal:
        return f"{vertical}_{horizontal}"

    return vertical or horizontal or "HERE"


def manhattan_distance(pos_one: Position, pos_two: Position) -> int:
    return abs(pos_one.x - pos_two.x) + abs(pos_one.y - pos_two.y)
