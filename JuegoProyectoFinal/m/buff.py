import pygame


class Buff:
    """Item coleccionable de poder."""

    def __init__(self, x, y, w, h, tipo):
        self.rect = pygame.Rect(x, y, w, h)
        self.tipo = tipo

    @classmethod
    def desde_dict(cls, data):
        return cls(
            data.get("x", 0),
            data.get("y", 0),
            data.get("w", 32),
            data.get("h", 32),
            data.get("tipo", "velocidad"),
        )
