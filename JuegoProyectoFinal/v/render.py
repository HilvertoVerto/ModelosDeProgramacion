import pygame
import os

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

        # Cargar imagen de fondo
        self.fondo_imagen = None
        self.fondo_ancho = 0
        self.fondo_x = 0  # Posición x del fondo para scrolling
        self.cargar_fondo()

    def cargar_fondo(self):
        """Carga la imagen de fondo"""
        fondo_path = os.path.join("graficos", "Fondo", "Fondo.png")
        if os.path.exists(fondo_path):
            self.fondo_imagen = pygame.image.load(fondo_path).convert()
            # Escalar el fondo a la altura de la ventana manteniendo proporción
            self.fondo_imagen = pygame.transform.scale(
                self.fondo_imagen,
                (int(self.fondo_imagen.get_width() * self.alto / self.fondo_imagen.get_height()), self.alto)
            )
            self.fondo_ancho = self.fondo_imagen.get_width()

    def limpiar_pantalla(self):
        """Limpia la pantalla con el color de fondo"""
        if self.fondo_imagen:
            # Dibujar fondo con scrolling infinito
            # Normalizar la posición x para que esté siempre entre 0 y fondo_ancho
            self.fondo_x = self.fondo_x % self.fondo_ancho

            # Dibujar dos copias del fondo para crear efecto infinito
            self.ventana.blit(self.fondo_imagen, (-self.fondo_x, 0))
            self.ventana.blit(self.fondo_imagen, (self.fondo_ancho - self.fondo_x, 0))
        else:
            # Fallback al color azul si no hay imagen
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

    def mover_fondo(self, desplazamiento_x):
        """Mueve el fondo en la dirección especificada

        Args:
            desplazamiento_x: Cantidad de píxeles a mover el fondo (positivo = derecha, negativo = izquierda)
        """
        self.fondo_x += desplazamiento_x
