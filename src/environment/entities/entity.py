from src.environment.utils import Position


class Entity:
    def __init__(self, pos: Position, name: str):
        self.pos = pos
        self.name = name


class InteractableMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.interacted = False

    def interact_with(self):
        self.interacted = not self.interacted


class DefeatableMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.alive = True

    def defeat(self):
        self.alive = False


class LockableMixin:
    def __init__(self, is_locked: bool = False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_locked = is_locked

    def lock(self) -> None:
        self.is_locked = True
        if hasattr(self, "blocks_movement"):
            self.blocks_movement = True

    def unlock(self) -> None:
        self.is_locked = False
        if hasattr(self, "blocks_movement"):
            self.blocks_movement = False
