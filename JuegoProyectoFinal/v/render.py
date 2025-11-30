import pygame

class Render:
    """Clase encargada de renderizar los elementos del juego"""

    def __init__(self, ventana, ancho, alto):
        self.ventana = ventana
        self.ancho = ancho
        self.alto = alto

        # Colores
        self.AZUL_CIELO = (135, 206, 235)
        self.VERDE = (34, 139, 34)
        self.MARRON = (139, 69, 19)

        # Altura del suelo
        self.altura_suelo = 50

    def limpiar_pantalla(self):
        """Limpia la pantalla con el color de fondo"""
        self.ventana.fill(self.AZUL_CIELO)

    def dibujar_suelo(self):
        """Dibuja el suelo del juego"""
        # Suelo verde
        pygame.draw.rect(
            self.ventana,
            self.VERDE,
            (0, self.alto - self.altura_suelo, self.ancho, self.altura_suelo)
        )

        # Línea de tierra
        pygame.draw.line(
            self.ventana,
            self.MARRON,
            (0, self.alto - self.altura_suelo),
            (self.ancho, self.alto - self.altura_suelo),
            3
        )

    def dibujar_jugador(self, jugador_rect, sprite):
        """Dibuja el sprite del jugador en su posición"""
        self.ventana.blit(sprite, jugador_rect)

    def actualizar_pantalla(self):
        """Actualiza la pantalla para mostrar los cambios"""
        pygame.display.flip()

    def get_altura_suelo(self):
        """Retorna la altura del suelo"""
        return self.altura_suelo
