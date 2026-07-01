from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from src.actions import GameAction
from src.environment.game import Game
from src.environment.grids import DefeatMobs, Grid, LockedDoors, Maze
from src.game_flow.enums import EndState
from src.game_options import AgentType, GridType


@dataclass
class ExperimentConfig:
    grid_type: GridType = GridType.DEFEAT_MOBS
    grid_size: tuple[int, int] = (8, 8)
    agent_type: AgentType = AgentType.HUMAN
    run_count: int = 1
    mob_count: int = 3
    section_count: int = 3
    seed: int | None = None

    def is_supported(self) -> bool:
        if self.agent_type == AgentType.HUMAN:
            return True
        return self.grid_type == GridType.DEFEAT_MOBS

    @property
    def disabled_reason(self) -> str | None:
        if self.is_supported():
            return None
        return "LLM agents currently support Defeat Mobs only."

    def build_grid(self, run_index: int = 1) -> Grid:
        width, height = self.grid_size
        seed = None if self.seed is None else self.seed + run_index - 1

        if self.grid_type == GridType.DEFEAT_MOBS:
            return DefeatMobs(width, height, seed=seed, mob_count=self.mob_count)
        if self.grid_type == GridType.MAZE:
            return Maze(width, height, seed=seed)
        if self.grid_type == GridType.LOCKED_DOORS:
            return LockedDoors(
                width,
                height,
                seed=seed,
                section_count=min(self.section_count, (width + 1) // 3),
            )

        raise ValueError(f"Unsupported grid type: {self.grid_type}")

    def build_game(self, run_index: int = 1) -> Game:
        return Game(self.build_grid(run_index))


@dataclass
class TurnRecord:
    run_index: int
    turn_number: int
    action: GameAction
    reasoning: str | None = None
    outcome: str = ""
    failure: EndState | None = None
    input_tokens: int = 0
    output_tokens: int = 0

    @property
    def is_invalid(self) -> bool:
        return self.action == GameAction.INVALID


@dataclass
class RunResult:
    run_index: int
    end_state: EndState
    turns: int
    invalid_inputs: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    log_path: Path | None = None
    turns_detail: list[TurnRecord] = field(default_factory=list)

    @property
    def succeeded(self) -> bool:
        return self.end_state == EndState.WIN


@dataclass
class ExperimentResult:
    config: ExperimentConfig
    runs: list[RunResult] = field(default_factory=list)

    @property
    def total_runs(self) -> int:
        return len(self.runs)

    @property
    def successes(self) -> int:
        return sum(1 for run in self.runs if run.succeeded)

    @property
    def failures(self) -> int:
        return self.total_runs - self.successes

    @property
    def total_turns(self) -> int:
        return sum(run.turns for run in self.runs)

    @property
    def total_invalid_inputs(self) -> int:
        return sum(run.invalid_inputs for run in self.runs)

    @property
    def total_input_tokens(self) -> int:
        return sum(run.input_tokens for run in self.runs)

    @property
    def total_output_tokens(self) -> int:
        return sum(run.output_tokens for run in self.runs)

    @property
    def average_turns(self) -> float:
        if not self.runs:
            return 0.0
        return self.total_turns / len(self.runs)

    def add_run(self, run: RunResult) -> None:
        self.runs.append(run)


def parse_run_log(path: Path) -> RunResult | None:
    text = path.read_text(encoding="utf-8")

    turns = _match_int(text, r"TOTAL TURNS:\s*(\d+)")
    invalids = _match_int(text, r"TOTAL INVALID RESPONSES:\s*(\d+)")
    input_tokens = _match_int(text, r"TOTAL INPUT TOKENS:\s*(\d+)")
    output_tokens = _match_int(text, r"TOTAL OUTPUT TOKENS:\s*(\d+)")
    end_state_value = _match_text(text, r"END STATE:\s*([a-z_]+)")

    if turns is None or end_state_value is None:
        return None

    try:
        end_state = EndState(end_state_value)
    except ValueError:
        return None

    return RunResult(
        run_index=1,
        end_state=end_state,
        turns=turns,
        invalid_inputs=invalids or 0,
        input_tokens=input_tokens or 0,
        output_tokens=output_tokens or 0,
        log_path=path,
    )


def load_historical_results(log_dir: Path = Path("logs")) -> list[RunResult]:
    if not log_dir.exists():
        return []

    results: list[RunResult] = []
    for path in sorted(log_dir.rglob("*.log"), reverse=True):
        result = parse_run_log(path)
        if result is not None:
            result.run_index = len(results) + 1
            results.append(result)
    return results


def _match_int(text: str, pattern: str) -> int | None:
    match = re.search(pattern, text)
    return int(match.group(1)) if match else None


def _match_text(text: str, pattern: str) -> str | None:
    match = re.search(pattern, text)
    return match.group(1) if match else None
