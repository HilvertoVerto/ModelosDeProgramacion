import pygame
from m.estrategias import MovimientoStrategy, PatrullaStrategy


class Enemigo(pygame.sprite.Sprite):
    """Enemigo con estrategia de movimiento (Strategy) y arma."""

    def __init__(
        self,
        x,
        y,
        ancho=48,
        alto=48,
        velocidad=2,
        limite_izq=0,
        limite_der=200,
        estrategia=None,
        arma=None,
    ):
        super().__init__()
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.velocidad_x = velocidad
        self.velocidad_y = 0
        self.limite_izq = limite_izq
        self.limite_der = limite_der
        self.en_suelo = False
        self.GRAVEDAD = 0.8
        self.estrategia: MovimientoStrategy = estrategia or PatrullaStrategy()
        self.arma = arma
        self.color = getattr(arma, "color", (200, 60, 60))
        self.ultimo_disparo = 0

    @classmethod
    def desde_dict(cls, data):
        return cls(
            x=data.get("x", 0),
            y=data.get("y", 0),
            ancho=data.get("ancho", 48),
            alto=data.get("alto", 48),
            velocidad=data.get("velocidad", 2),
            limite_izq=data.get("limite_izq", 0),
            limite_der=data.get("limite_der", 200),
        )

    def aplicar_gravedad(self):
        self.velocidad_y += self.GRAVEDAD
        self.rect.y += self.velocidad_y

    def mover(self):
        self.estrategia.mover(self)

    def resolver_colisiones_vertical(self, plataformas):
        self.en_suelo = False
        for plataforma in plataformas:
            if self.rect.colliderect(plataforma):
                if self.GRAVEDAD > 0 and self.rect.bottom <= plataforma.bottom:
                    self.rect.bottom = plataforma.top
                    self.velocidad_y = 0
                    self.en_suelo = True

    def update(self, plataformas):
        self.mover()
        self.aplicar_gravedad()
        self.resolver_colisiones_vertical(plataformas)
