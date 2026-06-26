from src.environment.utils import Position


class Entity:
    def __init__(self, position: Position):
        self.position = position


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
