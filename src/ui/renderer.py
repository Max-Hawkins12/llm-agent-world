import pygame

from src.environment.game import Game
from src.environment.entities import GameEntity, Goal, Agent
from src.ui.colours import UIColour
from src.ui.menu import StartMenu


class Renderer:
    def __init__(
        self,
        width: int,
        height: int,
        grid_width: int,
        grid_height: int,
        cell_size: int = 64,
    ):
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.large_font = pygame.font.Font(None, 40)
        self.cell_size = cell_size
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.window_width = width
        self.window_height = height

    def set_grid_size(self, grid_width: int, grid_height: int) -> None:
        self.grid_width = grid_width
        self.grid_height = grid_height

    def grid_offset(self) -> tuple[int, int]:
        grid_pixel_width = self.grid_width * self.cell_size
        grid_pixel_height = self.grid_height * self.cell_size
        offset_x = max(0, (self.window_width - grid_pixel_width) // 2)
        offset_y = max(0, (self.window_height - grid_pixel_height - 80) // 2)
        return offset_x, offset_y

    def draw_game(self, game: Game, end_screen: bool = False) -> None:
        self.screen.fill(UIColour.BLACK.value)
        self.draw_grid()

        for entity in game.get_alive_entities():
            outline = False
            if isinstance(entity, Goal):
                outline = not entity.locked
            elif isinstance(entity, Agent):
                outline = entity.has_weapon
            self.draw_entity(entity, outline)

        self.draw_hud(game)

        if end_screen:
            self.draw_end_screen(game)

    def draw_grid(self) -> None:
        offset_x, offset_y = self.grid_offset()
        for x in range(self.grid_width + 1):
            pygame.draw.line(
                self.screen,
                UIColour.GRID_GREY.value,
                (offset_x + x * self.cell_size, offset_y),
                (
                    offset_x + x * self.cell_size,
                    offset_y + self.grid_height * self.cell_size,
                ),
            )
        for y in range(self.grid_height + 1):
            pygame.draw.line(
                self.screen,
                UIColour.GRID_GREY.value,
                (offset_x, offset_y + y * self.cell_size),
                (
                    offset_x + self.grid_width * self.cell_size,
                    offset_y + y * self.cell_size,
                ),
            )

    def draw_entity(self, entity: GameEntity, outline: bool = False) -> None:
        offset_x, offset_y = self.grid_offset()
        rect = pygame.Rect(
            offset_x + entity.x * self.cell_size + 4,
            offset_y + entity.y * self.cell_size + 4,
            self.cell_size - 8,
            self.cell_size - 8,
        )
        pygame.draw.rect(self.screen, entity.colour.value, rect)
        if outline:
            pygame.draw.rect(self.screen, entity.outline_colour.value, rect, 3)

    def draw_hud(self, game: Game) -> None:
        status = f"Weapon: {'Yes' if game.agent.has_weapon else 'No'} | Mobs remaining: {sum(1 for mob in game.mobs if mob.alive)}"
        self.draw_text(status, 10, self.window_height - 70)
        self.draw_text(game.message, 10, self.window_height - 40)
        self.draw_text(
            "Controls: Arrow/WASD to move, ESC to quit",
            10,
            self.window_height - 20,
        )

    def draw_text(
        self, text: str, x: int, y: int, colour: tuple[int, int, int] = (240, 240, 240)
    ) -> None:
        surface = self.font.render(text, True, colour)
        self.screen.blit(surface, (x, y))

    def draw_menu(self, menu: StartMenu) -> None:
        self.screen.fill(UIColour.BLACK.value)
        self.draw_centered_text("2D Grid Adventure", 80, self.large_font)
        self.draw_text(
            "Use arrow keys to configure settings, SPACE to start.",
            20,
            130,
            UIColour.WHITE.value,
        )

        y_offset = 180
        for label, value, selected in menu.option_lines():
            prefix = "▶" if selected else " "
            colour = UIColour.WHITE.value if selected else UIColour.GRID_GREY.value
            self.draw_text(f"{prefix} {label}: {value}", 60, y_offset, colour)
            y_offset += 40

        self.draw_text(menu.message, 20, self.window_height - 40, UIColour.WHITE.value)

    def draw_end_screen(self, game: Game) -> None:
        overlay = pygame.Surface(
            (self.window_width, self.window_height), pygame.SRCALPHA
        )
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))

        self.draw_centered_text(
            "Game Finished!", self.window_height // 2 - 40, self.large_font
        )
        self.draw_centered_text(game.message, self.window_height // 2 + 10, self.font)
        self.draw_centered_text(
            "Press ESC to quit.", self.window_height // 2 + 40, self.font
        )

    def draw_centered_text(self, text: str, y: int, font: pygame.font.Font) -> None:
        surface = font.render(text, True, UIColour.WHITE.value)
        rect = surface.get_rect(center=(self.window_width // 2, y))
        self.screen.blit(surface, rect)
