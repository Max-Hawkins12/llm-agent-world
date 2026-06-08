from enum import Enum


class UIColour(Enum):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    GRID_GREY = (128, 128, 128)
    AGENT_BLUE = (0, 0, 255)
    MOB_RED = (255, 0, 0)
    WEAPON_YELLOW = (255, 255, 0)
    GOAL_GREEN = (0, 255, 0)

    # Menu / UI themed colours
    MENU_BG = (30, 30, 40)
    MENU_TEXT = (230, 230, 235)
    MENU_HIGHLIGHT = (90, 160, 255)
    SIDEBAR_BG = (28, 28, 34)
    TAB_BG = (45, 45, 55)
    GRID_BG = (18, 18, 24)
