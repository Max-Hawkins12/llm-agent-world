from enum import Enum


class UIColour(Enum):
    WHITE = (245, 247, 250)
    BLACK = (12, 14, 18)
    TEXT = (228, 232, 238)
    MUTED_TEXT = (145, 154, 166)
    DISABLED_TEXT = (93, 101, 112)

    BG = (20, 23, 28)
    PANEL = (30, 35, 42)
    PANEL_DARK = (24, 28, 34)
    PANEL_LIGHT = (42, 49, 58)
    BORDER = (74, 84, 98)
    ACCENT = (77, 166, 255)
    ACCENT_DARK = (41, 116, 190)
    WARNING = (230, 166, 64)
    ERROR = (224, 86, 86)
    SUCCESS = (91, 183, 111)

    TILE = (38, 43, 50)
    WALL = (89, 96, 106)
    GRID_LINE = (64, 72, 84)
    PLAYER = (75, 154, 255)
    MOB = (224, 86, 86)
    WEAPON = (232, 190, 72)
    KEY = (236, 211, 111)
    DOOR = (157, 104, 67)
    GOAL = (91, 183, 111)
