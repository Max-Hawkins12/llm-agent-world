from pathlib import Path
from datetime import datetime

from src.game_flow.enums import EndState
from src.game_options import AgentType
from src.actions import GameAction


class RunLogger:
    def __init__(self, model_name: str, agent_type: AgentType):
        Path(f"logs/{agent_type.display_name}").mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

        filename = f"{model_name}-{agent_type.display_name}-{timestamp}.log"
        self.log_path = Path(f"logs/{agent_type.display_name}") / filename

        self.make_log_file(model_name, agent_type, timestamp)

    def make_log_file(
        self, model_name: str, agent_type: AgentType, timestamp: str
    ) -> None:
        header = f"""
========================================
MODEL: {model_name}
OBSERVATION LEVEL: {agent_type.display_name}
STARTED AT: {timestamp}
========================================

"""
        self.write(header, mode="w")

    def log_turn(
        self,
        turn: int,
        observation: str,
        prompt: str,
        raw_response: str,
        action: GameAction,
        reasoning: str,
    ) -> None:
        turn_log = f"""
========================================
TURN {turn}
========================================

OBSERVATION

{observation}

PROMPT

{prompt}

RAW RESPONSE

{raw_response}

ACTION

{action.value}

REASONING

{reasoning}

"""
        self.write(turn_log, mode="a")

    def log_ending(self, total_turns: int, end_state: EndState) -> None:
        end_log = f"""
========================================
TOTAL TURNS: {total_turns}
END STATE: {end_state.value}
========================================
"""
        self.write(end_log, mode="a")

    def write(self, text, mode="a") -> None:
        with open(self.log_path, mode, encoding="utf-8") as file:
            file.write(text)
