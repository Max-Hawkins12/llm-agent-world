from enum import Enum
from typing import Any, List, Tuple
import pygame

from src.actions import MenuAction
from src.game_options import GameOptions, GameSettings


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

        if isinstance(value, Enum):
            return value.name.capitalize()

        return str(value).capitalize()

    def move_next(self) -> None:
        self.current_index = (self.current_index + 1) % len(self.values)

    def move_previous(self) -> None:
        self.current_index = (self.current_index - 1) % len(self.values)


class StartMenu:
    def __init__(self):
        self.options = {
            # TODO: Agent Type option
            "grid_size": MenuOption("Grid Size", GameOptions.GRID_SIZE_OPTIONS, 1),
            "entity_placement": MenuOption(
                "Entity Placement", GameOptions.ENTITY_PLACEMENT_OPTIONS, 0
            ),
            "has_weapon": MenuOption(
                "Agent Starts with Weapon", GameOptions.AGENT_START_WITH_WEAPON, 0
            ),
            "mob_count": MenuOption("Mob Count", GameOptions.MOB_COUNT_OPTIONS, 2),
            "mob_move_pattern": MenuOption(
                "Mob Behaviour", GameOptions.MOB_MOVE_PATTERNS, 0
            ),
        }
        self.option_keys = list(self.options)
        self.selected_index = 0
        self.message = "Use arrow keys to customize options. Press SPACE to start."

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
            grid_size=self.options["grid_size"].selected_value,
            entity_placement=self.options["entity_placement"].selected_value,
            has_weapon=self.options["has_weapon"].selected_value,
            mob_count=self.options["mob_count"].selected_value,
            mob_move_pattern=self.options["mob_move_pattern"].selected_value,
        )

    def option_lines(self) -> List[Tuple[str, str, bool]]:
        return [
            (
                self.options[key].label,
                self.options[key].display_value,
                i == self.selected_index,
            )
            for i, key in enumerate(self.option_keys)
        ]


def parse_menu_action(events: list[pygame.event.Event]) -> MenuAction:
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return MenuAction.QUIT
            if event.key in (pygame.K_UP, pygame.K_w):
                return MenuAction.OPTION_UP
            if event.key in (pygame.K_DOWN, pygame.K_s):
                return MenuAction.OPTION_DOWN
            if event.key in (pygame.K_LEFT, pygame.K_a):
                return MenuAction.PREV_OPTION
            if event.key in (pygame.K_RIGHT, pygame.K_d):
                return MenuAction.NEXT_OPTION
            if event.key == pygame.K_SPACE:
                return MenuAction.START
    return MenuAction.WAIT
