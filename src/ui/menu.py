from enum import Enum
from typing import Any, List, Tuple

from src.actions import MenuAction
from src.game_options import GameOptions, GameSettings, AgentType


class MenuOption:
    def __init__(self, label: str, values: List[Any], current_index: int = 0):
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

        if isinstance(value, AgentType):
            return value.display_name

        if isinstance(value, Enum):
            return value.name.title()

        return str(value).title()

    def move_next(self) -> None:
        self.current_index = (self.current_index + 1) % len(self.values)

    def move_previous(self) -> None:
        self.current_index = (self.current_index - 1) % len(self.values)


class StartMenu:
    def __init__(self):
        self.options = {
            "agent_type": MenuOption("Agent Type", GameOptions.AGENT_TYPE, 1),
            "mob_placement": MenuOption(
                "Mob & Weapon Placement", GameOptions.MOB_PLACEMENT_OPTIONS
            ),
            "mob_count": MenuOption("Mob Count", GameOptions.MOB_COUNT_OPTIONS, 2),
            "mob_move_pattern": MenuOption(
                "Mob Behaviour", GameOptions.MOB_MOVE_PATTERNS
            ),
        }
        self.option_keys = list(self.options)
        self.selected_index = 0

    def process_action(self, action: MenuAction) -> None:
        match action:
            case MenuAction.OPTION_UP:
                self.selected_index = (self.selected_index - 1) % len(self.option_keys)
            case MenuAction.OPTION_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.option_keys)
            case MenuAction.PREV_OPTION:
                current_key = self.option_keys[self.selected_index]
                self.options[current_key].move_previous()
            case MenuAction.NEXT_OPTION:
                current_key = self.option_keys[self.selected_index]
                self.options[current_key].move_next()

    def build_game_settings(self) -> GameSettings:
        return GameSettings(
            mob_placement=self.options["mob_placement"].selected_value,
            mob_count=self.options["mob_count"].selected_value,
            mob_move_pattern=self.options["mob_move_pattern"].selected_value,
        )

    @property
    def agent_type(self) -> AgentType:
        return self.options["agent_type"].selected_value

    def option_lines(self) -> List[Tuple[str, str, bool]]:
        return [
            (
                self.options[key].label,
                self.options[key].display_value,
                i == self.selected_index,
            )
            for i, key in enumerate(self.option_keys)
        ]
