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
        self.tamaño_sprite = (64, 64)

    def cargar_sprites(self):
        """Carga todos los sprites del personaje"""
        # Sprite quieto derecha (frente0) - se usa cuando está parado
        sprite_path = os.path.join(self.base_path, "frente0", "traje_quieto_f0.png")
        if os.path.exists(sprite_path):
            self.sprite_quieto_derecha = pygame.image.load(sprite_path).convert_alpha()
            self.sprite_quieto_derecha = pygame.transform.scale(
                self.sprite_quieto_derecha,
                self.tamaño_sprite
            )

        # Sprites de movimiento para animación
        # La animación alterna entre traje_quieto_f0 y traje_mov_f0
        sprites_movimiento = []

        # Frame 0 de animación: traje_quieto_f0
        sprite_path = os.path.join(self.base_path, "frente0", "traje_quieto_f0.png")
        if os.path.exists(sprite_path):
            sprite = pygame.image.load(sprite_path).convert_alpha()
            sprite = pygame.transform.scale(sprite, self.tamaño_sprite)
            sprites_movimiento.append(sprite)

        # Frame 1 de animación: traje_mov_f0
        sprite_path = os.path.join(self.base_path, "frente0", "traje_mov_f0.png")
        if os.path.exists(sprite_path):
            sprite = pygame.image.load(sprite_path).convert_alpha()
            sprite = pygame.transform.scale(sprite, self.tamaño_sprite)
            sprites_movimiento.append(sprite)

        self.sprites_derecha = sprites_movimiento

        # Crear sprites para la izquierda (flip horizontal)
        if self.sprite_quieto_derecha:
            self.sprite_quieto_izquierda = pygame.transform.flip(
                self.sprite_quieto_derecha, True, False
            )

        for sprite in self.sprites_derecha:
            self.sprites_izquierda.append(
                pygame.transform.flip(sprite, True, False)
            )

        # Crear sprite de emergencia si no se cargó nada
        if not self.sprite_quieto_derecha:
            self.sprite_quieto_derecha = pygame.Surface(self.tamaño_sprite)
            self.sprite_quieto_derecha.fill((255, 0, 0))
            self.sprite_quieto_izquierda = self.sprite_quieto_derecha.copy()

    def get_sprite(self, mirando_derecha, moviendo, frame):
        """Obtiene el sprite apropiado según el estado del jugador"""
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
        """Retorna el número de frames de animación disponibles"""
        return len(self.sprites_derecha)
