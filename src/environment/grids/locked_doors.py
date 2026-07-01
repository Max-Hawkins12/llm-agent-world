import random
from dataclasses import dataclass

from src.environment.entities import Door, Key
from src.environment.utils import Position

from .grid import Grid


@dataclass(frozen=True)
class Section:
    """Inclusive horizontal bounds for one locked-door section."""

    left: int
    right: int

    @property
    def width(self) -> int:
        return self.right - self.left + 1


class LockedDoors(Grid):
    """A grid split into random-width sections by locked doors.

    Sections are arranged from left to right. Each section except the final
    goal section contains a key for the door that leads into the next section.
    """

    def __init__(
        self,
        width: int,
        height: int,
        seed: int | None = None,
        section_count: int | None = None,
    ):

        self._validate_grid_size(width, height)
        self._random = random.Random(seed)

        self.section_count = section_count or self._random.randint(
            2, max(2, min(5, (width + 1) // 3))
        )
        self._validate_section_count(width)

        super().__init__(width, height)

        self.sections: list[Section] = []
        self.doors: list[Door] = []

        self._generate_grid()

    def _validate_grid_size(self, width: int, height: int) -> None:
        if height < 3:
            raise ValueError("LockedDoors height must be at least 3")
        if width < 5:
            raise ValueError("LockedDoors width must be at least 5")

    def _validate_section_count(self, width: int) -> None:
        max_sections = (width + 1) // 3
        if self.section_count < 2:
            raise ValueError("LockedDoors must have at least 2 sections")
        if self.section_count > max_sections:
            raise ValueError(
                f"LockedDoors width {width} can fit at most {max_sections} sections"
            )

    def _generate_grid(self) -> None:
        self.sections = self._create_sections()
        self._add_section_dividers()

        self.player_pos = self._random_position_in_section(self.sections[0], avoid=[])
        self._place_goal(
            pos=self._random_position_in_section(self.sections[-1], avoid=[]),
            is_locked=False,
        )
        self._place_keys()

    def _create_sections(self) -> list[Section]:
        divider_count = self.section_count - 1
        available_section_width = self.grid_width - divider_count
        min_section_width = 2
        extra_width = available_section_width - (self.section_count * min_section_width)

        widths = [min_section_width] * self.section_count
        for _ in range(extra_width):
            widths[self._random.randrange(self.section_count)] += 1
        self._random.shuffle(widths)

        sections: list[Section] = []
        left = 0
        for section_width in widths:
            right = left + section_width - 1
            sections.append(Section(left, right))
            left = right + 2

        return sections

    def _add_section_dividers(self) -> None:
        for door_id, section in enumerate(self.sections[:-1], start=1):
            divider_x = section.right + 1
            door_y = self._random.randrange(self.grid_height)

            for y in range(self.grid_height):
                pos = Position(divider_x, y)
                if y == door_y:
                    door = Door(pos, name=str(door_id))
                    self._set_background_entity(door)
                    self.doors.append(door)
                else:
                    self._place_wall(pos)

    def _place_keys(self) -> None:
        occupied = [self.player_pos, self.goal_pos]
        for section, door in zip(self.sections, self.doors):
            key_pos = self._random_position_in_section(section, occupied)

            self._add_static_entity(
                Key(
                    pos=key_pos,
                    name=door.name.removeprefix("Door_"),
                    unlocks=door,
                )
            )

            occupied.append(key_pos)

    def _random_position_in_section(
        self, section: Section, avoid: list[Position]
    ) -> Position:
        candidates = [
            Position(x, y)
            for x in range(section.left, section.right + 1)
            for y in range(self.grid_height)
            if Position(x, y) not in avoid
        ]
        return self._random.choice(candidates)
