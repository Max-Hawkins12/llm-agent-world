import pygame

from src.actions import GameAction, MenuAction

GAME_KEYMAP = {
    pygame.K_w: GameAction.MOVE_UP,
    pygame.K_UP: GameAction.MOVE_UP,
    pygame.K_s: GameAction.MOVE_DOWN,
    pygame.K_DOWN: GameAction.MOVE_DOWN,
    pygame.K_a: GameAction.MOVE_LEFT,
    pygame.K_LEFT: GameAction.MOVE_LEFT,
    pygame.K_d: GameAction.MOVE_RIGHT,
    pygame.K_RIGHT: GameAction.MOVE_RIGHT,
    pygame.K_ESCAPE: GameAction.QUIT,
}

MENU_KEYMAP = {
    pygame.K_w: MenuAction.OPTION_UP,
    pygame.K_UP: MenuAction.OPTION_UP,
    pygame.K_s: MenuAction.OPTION_DOWN,
    pygame.K_DOWN: MenuAction.OPTION_DOWN,
    pygame.K_a: MenuAction.PREV_OPTION,
    pygame.K_LEFT: MenuAction.PREV_OPTION,
    pygame.K_d: MenuAction.NEXT_OPTION,
    pygame.K_RIGHT: MenuAction.NEXT_OPTION,
    pygame.K_SPACE: MenuAction.START,
    pygame.K_ESCAPE: MenuAction.QUIT,
}


def get_game_action(events: list[pygame.event.Event]) -> GameAction:
    for event in events:
        if event.type == pygame.KEYDOWN:
            try:
                return GAME_KEYMAP[event.key]
            except KeyError:
                pass
    return GameAction.WAIT


def get_menu_action(events: list[pygame.event.Event]) -> MenuAction:
    for event in events:
        if event.type == pygame.KEYDOWN:
            try:
                return MENU_KEYMAP[event.key]
            except KeyError:
                pass
    return MenuAction.WAIT
