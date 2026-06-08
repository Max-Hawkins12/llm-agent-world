from pathlib import Path
from datetime import datetime

from src.game_flow.enums import EndState
from src.actions import GameAction


class RunLogger:
    def __init__(self, model_name: str):
        Path(f"logs").mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

        filename = f"{model_name}-{timestamp}.log"
        self.log_path = Path(f"logs") / filename

        self.make_log_file(model_name, timestamp)

    def make_log_file(self, model_name: str, timestamp: str) -> None:
        header = f"""
========================================
MODEL: {model_name}
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

    def log_ending(
        self,
        total_turns: int,
        end_state: EndState,
        total_input_tokens: int,
        total_output_tokens: int,
        # total_invalid_responses: int,
        # total_invalid_moves: int,
    ) -> None:
        # TOTAL INVALID RESPONSES: {total_invalid_responses} TOTAL INVALID MOVES: {total_invalid_moves}
        end_log = f"""
========================================
TOTAL TURNS: {total_turns}
END STATE: {end_state.value}
TOTAL INPUT TOKENS: {total_input_tokens}
TOTAL OUTPUT TOKENS: {total_output_tokens}
========================================
"""
        self.write(end_log, mode="a")

    def write(self, text, mode="a") -> None:
        with open(self.log_path, mode, encoding="utf-8") as file:
            file.write(text)
