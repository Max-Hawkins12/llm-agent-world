import pygame

from src.environment.game import Game, GameState
from src.environment.entities import GameEntity
from src.constants import (
    CELL_SIZE,
    GRID_HEIGHT,
    GRID_WIDTH,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)
from src.ui.colours import UIColour


class Renderer:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.large_font = pygame.font.Font(None, 40)

    def draw(self, game: Game, end_screen: bool = False) -> None:
        self.screen.fill(UIColour.BLACK.value)
        self.draw_grid()
        self.draw_entity(game.goal, outline=not game.goal.locked)

        if not game.agent.has_weapon:
            self.draw_entity(game.weapon)
        for mob in game.mobs:
            if mob.alive:
                self.draw_entity(mob)

        self.draw_entity(game.agent)
        self.draw_hud(game)
        if end_screen:
            self.draw_end_screen(game)

    def draw_grid(self) -> None:
        for x in range(GRID_WIDTH + 1):
            pygame.draw.line(
                self.screen,
                UIColour.GRID_GREY.value,
                (x * CELL_SIZE, 0),
                (x * CELL_SIZE, GRID_HEIGHT * CELL_SIZE),
            )
        for y in range(GRID_HEIGHT + 1):
            pygame.draw.line(
                self.screen,
                UIColour.GRID_GREY.value,
                (0, y * CELL_SIZE),
                (GRID_WIDTH * CELL_SIZE, y * CELL_SIZE),
            )

    def draw_entity(self, entity: GameEntity, outline: bool = False) -> None:
        rect = pygame.Rect(
            entity.x * CELL_SIZE + 4,
            entity.y * CELL_SIZE + 4,
            CELL_SIZE - 8,
            CELL_SIZE - 8,
        )
        pygame.draw.rect(self.screen, entity.color.value, rect)
        if outline:
            pygame.draw.rect(self.screen, UIColour.WHITE.value, rect, 3)

    def draw_hud(self, game: Game) -> None:
        status = f"Weapon: {'Yes' if game.agent.has_weapon else 'No'} | Mobs remaining: {sum(1 for mob in game.mobs if mob.alive)}"
        self.draw_text(status, 10, WINDOW_HEIGHT - 70)
        self.draw_text(game.message, 10, WINDOW_HEIGHT - 40)
        self.draw_text(
            "Controls: Arrow/WASD to move, SPACE to attack nearby mob",
            10,
            WINDOW_HEIGHT - 20,
        )

    def draw_text(self, text: str, x: int, y: int) -> None:
        surface = self.font.render(text, True, (240, 240, 240))
        self.screen.blit(surface, (x, y))

    def draw_end_screen(self, game: Game) -> None:
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))
        title = "You Win!" if game.state == GameState.WON else "Game Over"
        subtitle = (
            "Press ESC to quit."
            if game.state == GameState.WON
            else "Press ESC to quit and try again."
        )
        self.draw_centered_text(title, WINDOW_HEIGHT // 2 - 40, self.large_font)
        self.draw_centered_text(game.message, WINDOW_HEIGHT // 2 + 10, self.font)
        self.draw_centered_text(subtitle, WINDOW_HEIGHT // 2 + 40, self.font)

    def draw_centered_text(self, text: str, y: int, font: pygame.font.Font) -> None:
        surface = font.render(text, True, UIColour.WHITE.value)
        rect = surface.get_rect(center=(WINDOW_WIDTH // 2, y))
        self.screen.blit(surface, rect)
