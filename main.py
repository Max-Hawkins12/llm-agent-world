# from src.game_flow.game_runner import GameRunner

from src.environment.grids.maze import Maze
from src.environment.grids.locked_doors import LockedDoors

if __name__ == "__main__":
    # GameRunner().run()

    m = Maze(20, 20)
    print(m.render_to_text())
    d = LockedDoors(20, 20)
    print("\n")
    print(d.render_to_text())
