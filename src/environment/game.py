from .entities import Player
from .grids import Grid

from src.actions import GameAction


class Game:
    def __init__(self, grid: Grid):
        self.grid = grid

        self.player = Player(self.grid.player_pos)
        self.entities = self.grid.entities

    def process_action(self, action: GameAction):
        """
        if action == Movement action
            try_move_in_direction
        if action == other
            try_do_action

        other_entities.action

        """
