from .entities.actors import PlayerEntity
from .grids.grid import Grid


class Game:
    def __init__(self, grid: Grid):
        self.grid = grid

        x, y = self.grid.start

        self.agent = Agent(x, y)

    def process_action(self, action: AgentAction):
        """
        if movement action -> ask grid if new cell is valid then move
        elif -> ask grid if action is valid child classes will override a do_action(pos, action) in Grid

        Then call a grid.perform moves method -> will move mobs or anything the specific grid may do
        """
