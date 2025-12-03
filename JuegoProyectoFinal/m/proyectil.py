import pygame


class Proyectil:
    """Proyectil simple disparado por enemigos."""

    def __init__(self, x, y, vx, vy, ancho=12, alto=6, color=(255, 200, 50), dano=10, ttl_ms=3000):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.vx = vx
        self.vy = vy
        self.color = color
        self.dano = dano
        self.ttl_ms = ttl_ms
        self.creado_ms = pygame.time.get_ticks()
        self.vivo = True

    def update(self):
        """Mueve el proyectil y verifica tiempo de vida."""
        if not self.vivo:
            return
        self.rect.x += self.vx
        self.rect.y += self.vy

        ahora = pygame.time.get_ticks()
        if ahora - self.creado_ms > self.ttl_ms:
            self.vivo = False
