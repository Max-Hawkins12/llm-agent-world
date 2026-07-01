from enum import Enum
from typing import Any

from src.actions import MenuAction
from src.game_flow.experiment import ExperimentConfig
from src.game_options import AgentType, GameOptions, GridType


class MenuOption:
    def __init__(
        self,
        key: str,
        label: str,
        values: list[Any],
        current_index: int = 0,
    ):
        self.key = key
        self.label = label
        self.values = values
        self.current_index = current_index

    @property
    def selected_value(self) -> Any:
        return self.values[self.current_index]

    @property
    def display_value(self) -> str:
        value = self.selected_value

        if isinstance(value, tuple):
            return f"{value[0]} x {value[1]}"

        if hasattr(value, "display_name"):
            return value.display_name

        if isinstance(value, Enum):
            return value.name.replace("_", " ").title()

        return str(value).title()

    def move_next(self) -> None:
        self.current_index = (self.current_index + 1) % len(self.values)

    def move_previous(self) -> None:
        self.current_index = (self.current_index - 1) % len(self.values)

    def set_value(self, value: Any) -> None:
        self.current_index = self.values.index(value)


class StartMenu:
    def __init__(self):
        self.options = [
            MenuOption("grid_type", "Grid Type", GameOptions.GRID_TYPE),
            MenuOption("grid_size", "Grid Size", GameOptions.GRID_SIZE_OPTIONS),
            MenuOption("agent_type", "Agent Type", GameOptions.AGENT_TYPE),
            MenuOption("run_count", "Runs", GameOptions.RUN_COUNT_OPTIONS),
            MenuOption("mob_count", "Mobs", GameOptions.MOB_COUNT_OPTIONS, 2),
            MenuOption(
                "section_count", "Door Sections", GameOptions.SECTION_COUNT_OPTIONS, 1
            ),
        ]
        self.selected_index = 0

    @property
    def selected_option(self) -> MenuOption:
        return self.options[self.selected_index]

    def process_action(self, action: MenuAction) -> None:
        match action:
            case MenuAction.OPTION_UP:
                self.selected_index = (self.selected_index - 1) % len(self.options)
            case MenuAction.OPTION_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.options)
            case MenuAction.PREV_OPTION:
                self.selected_option.move_previous()
            case MenuAction.NEXT_OPTION:
                self.selected_option.move_next()

    def process_click(self, action_id: str) -> None:
        if action_id.startswith("menu:select:"):
            self.selected_index = int(action_id.rsplit(":", 1)[1])
            return

        if action_id.startswith("menu:prev:"):
            self.options[int(action_id.rsplit(":", 1)[1])].move_previous()
            return

        if action_id.startswith("menu:next:"):
            self.options[int(action_id.rsplit(":", 1)[1])].move_next()

    def build_config(self) -> ExperimentConfig:
        values = {option.key: option.selected_value for option in self.options}
        return ExperimentConfig(
            grid_type=values["grid_type"],
            grid_size=values["grid_size"],
            agent_type=values["agent_type"],
            run_count=values["run_count"],
            mob_count=values["mob_count"],
            section_count=values["section_count"],
        )

    @property
    def agent_type(self) -> AgentType:
        return self.build_config().agent_type

    @property
    def grid_type(self) -> GridType:
        return self.build_config().grid_type
