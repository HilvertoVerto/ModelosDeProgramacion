import pygame
import os


class SpriteLoader:
    """Clase encargada de cargar y gestionar los sprites del juego"""

    def __init__(self, base_path="graficos/Sprites"):
        self.base_path = base_path
        self.sprite_derecha = None
        self.sprite_izquierda = None
        self.tamano_sprite = (64, 64)

    def cargar_sprites(self):
        """Carga el sprite del jugador"""
        sprite_path = os.path.join(self.base_path, "Jugador.png")

        if os.path.exists(sprite_path):
            # Cargar sprite del jugador
            sprite = pygame.image.load(sprite_path).convert_alpha()
            sprite = pygame.transform.scale(sprite, self.tamano_sprite)
            self.sprite_derecha = sprite
            self.sprite_izquierda = pygame.transform.flip(sprite, True, False)
        else:
            # Fallback: círculo blanco
            circle = pygame.Surface(self.tamano_sprite, pygame.SRCALPHA)
            pygame.draw.circle(
                circle,
                (255, 255, 255),
                (self.tamano_sprite[0] // 2, self.tamano_sprite[1] // 2),
                self.tamano_sprite[0] // 2,
            )
            self.sprite_derecha = circle
            self.sprite_izquierda = pygame.transform.flip(circle, True, False)

    def get_sprite(self, mirando_derecha, moviendo, frame):
        """Obtiene el sprite apropiado según la dirección del jugador"""
        if mirando_derecha:
            return self.sprite_derecha
        else:
            return self.sprite_izquierda

    def get_num_frames(self):
        """Retorna el número de frames de animación disponibles (1 sprite estático)"""
        return 1
