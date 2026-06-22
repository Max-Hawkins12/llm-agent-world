# from src.game_flow.game_runner import GameRunner

from src.environment.grids.maze import Maze

if __name__ == "__main__":
    # GameRunner().run()

    m = Maze(20, 20)
    print(m.render_to_text())
