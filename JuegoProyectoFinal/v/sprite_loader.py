import pygame
import os


class SpriteLoader:
    """Clase encargada de cargar y gestionar los sprites del juego"""

    def __init__(self, base_path="graficos/Sprites/traje"):
        self.base_path = base_path
        self.sprites_derecha = []
        self.sprites_izquierda = []
        self.sprite_quieto_derecha = None
        self.sprite_quieto_izquierda = None
        self.tamano_sprite = (64, 64)

    def cargar_sprites(self):
        """Carga todos los sprites del personaje"""
        sprites_movimiento = []

        sprite_path = os.path.join(self.base_path, "frente0", "traje_quieto_f0.png")
        if os.path.exists(sprite_path):
            base_sprite = pygame.image.load(sprite_path).convert_alpha()
            base_sprite = pygame.transform.scale(base_sprite, self.tamano_sprite)
            self.sprite_quieto_derecha = base_sprite
            sprites_movimiento.append(base_sprite)

        sprite_path = os.path.join(self.base_path, "frente0", "traje_mov_f0.png")
        if os.path.exists(sprite_path):
            sprite = pygame.image.load(sprite_path).convert_alpha()
            sprite = pygame.transform.scale(sprite, self.tamano_sprite)
            sprites_movimiento.append(sprite)

        self.sprites_derecha = sprites_movimiento

        if self.sprite_quieto_derecha:
            self.sprite_quieto_izquierda = pygame.transform.flip(
                self.sprite_quieto_derecha, True, False
            )

        for sprite in self.sprites_derecha:
            self.sprites_izquierda.append(
                pygame.transform.flip(sprite, True, False)
            )

        # Sprite circular para apariencia (override)
        circle = pygame.Surface(self.tamano_sprite, pygame.SRCALPHA)
        pygame.draw.circle(
            circle,
            (255, 255, 255),
            (self.tamano_sprite[0] // 2, self.tamano_sprite[1] // 2),
            self.tamano_sprite[0] // 2,
        )
        self.sprite_quieto_derecha = circle
        self.sprite_quieto_izquierda = pygame.transform.flip(circle, True, False)
        self.sprites_derecha = [circle]
        self.sprites_izquierda = [self.sprite_quieto_izquierda]

    def get_sprite(self, mirando_derecha, moviendo, frame):
        """Obtiene el sprite apropiado segun el estado del jugador"""
        if moviendo and len(self.sprites_derecha) > 0:
            if mirando_derecha:
                return self.sprites_derecha[frame % len(self.sprites_derecha)]
            else:
                return self.sprites_izquierda[frame % len(self.sprites_izquierda)]
        else:
            if mirando_derecha:
                return self.sprite_quieto_derecha
            else:
                return self.sprite_quieto_izquierda

    def get_num_frames(self):
        """Retorna el numero de frames de animacion disponibles"""
        return len(self.sprites_derecha)
