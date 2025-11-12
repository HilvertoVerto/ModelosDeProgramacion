import pygame
import random
import sys

# Inicializar pygame
pygame.init()

# Constantes
FILAS = 6
COLUMNAS = 7
TAMANO_CELDA = 80
ANCHO = COLUMNAS * TAMANO_CELDA
ALTO = FILAS * TAMANO_CELDA + 100  # Espacio extra para instrucciones
FPS = 60

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (200, 200, 200)
GRIS_OSCURO = (100, 100, 100)
COLOR_2 = (238, 228, 218)
COLOR_4 = (237, 224, 200)
COLOR_8 = (242, 177, 121)

# Configurar ventana
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego de Bloques")
reloj = pygame.time.Clock()

# Fuente
fuente = pygame.font.Font(None, 48)
fuente_pequena = pygame.font.Font(None, 24)


class Juego:
    def __init__(self):
        self.cuadricula = [[0 for _ in range(COLUMNAS)] for _ in range(FILAS)]
        self.cayendo = False

    def colocar_bloque(self, columna):
        """Coloca un bloque en la columna especificada"""
        if self.cayendo:
            return

        # Verificar si la columna está llena
        if self.cuadricula[0][columna] != 0:
            return

        # Generar número aleatorio: 2, 4 u 8
        numero = random.choice([2, 4, 8])

        # Colocar en la primera fila
        self.cuadricula[0][columna] = numero

        # Aplicar gravedad
        self.aplicar_gravedad()

    def aplicar_gravedad(self):
        """Hace que los bloques caigan hacia abajo"""
        movimiento = True
        while movimiento:
            movimiento = False
            # Recorrer de abajo hacia arriba
            for fila in range(FILAS - 2, -1, -1):
                for col in range(COLUMNAS):
                    # Si hay un bloque y el espacio debajo está vacío
                    if self.cuadricula[fila][col] != 0 and self.cuadricula[fila + 1][col] == 0:
                        # Mover el bloque hacia abajo
                        self.cuadricula[fila + 1][col] = self.cuadricula[fila][col]
                        self.cuadricula[fila][col] = 0
                        movimiento = True

    def obtener_color(self, numero):
        """Retorna el color según el número"""
        if numero == 2:
            return COLOR_2
        elif numero == 4:
            return COLOR_4
        elif numero == 8:
            return COLOR_8
        return BLANCO

    def dibujar(self):
        """Dibuja el juego en la pantalla"""
        pantalla.fill(BLANCO)

        # Dibujar cuadrícula
        for fila in range(FILAS):
            for col in range(COLUMNAS):
                x = col * TAMANO_CELDA
                y = fila * TAMANO_CELDA + 60

                # Dibujar celda
                pygame.draw.rect(pantalla, GRIS, (x, y, TAMANO_CELDA, TAMANO_CELDA), 2)

                # Dibujar número si existe
                if self.cuadricula[fila][col] != 0:
                    color = self.obtener_color(self.cuadricula[fila][col])
                    pygame.draw.rect(pantalla, color, (x + 2, y + 2, TAMANO_CELDA - 4, TAMANO_CELDA - 4))

                    # Dibujar número
                    texto = fuente.render(str(self.cuadricula[fila][col]), True, NEGRO)
                    texto_rect = texto.get_rect(center=(x + TAMANO_CELDA // 2, y + TAMANO_CELDA // 2))
                    pantalla.blit(texto, texto_rect)

        # Dibujar instrucciones
        instrucciones = fuente_pequena.render("Haz clic en una columna para colocar un bloque", True, NEGRO)
        pantalla.blit(instrucciones, (10, 10))

        pygame.display.flip()


def main():
    juego = Juego()
    ejecutando = True

    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False

            if evento.type == pygame.MOUSEBUTTONDOWN:
                # Obtener posición del mouse
                x, y = pygame.mouse.get_pos()

                # Verificar si el clic está en el área de la cuadrícula
                if y >= 60 and y < ALTO:
                    # Calcular columna
                    columna = x // TAMANO_CELDA
                    if 0 <= columna < COLUMNAS:
                        juego.colocar_bloque(columna)

        juego.dibujar()
        reloj.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
