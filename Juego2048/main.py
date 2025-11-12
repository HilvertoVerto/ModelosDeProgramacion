import pygame
import sys

from constants import ALTO, FILAS, COLUMNAS, TAMANO_CELDA, reloj, FPS
from game import Juego


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

                # Verificar si el clic está en el botón de deshacer
                rect_boton = juego.obtener_rect_boton_deshacer()
                if rect_boton.collidepoint(x, y):
                    if juego.caretaker.tiene_historial():
                        juego.deshacer_jugada()
                # Verificar si el clic está en el área de la cuadrícula
                elif y >= 60 and y < ALTO:
                    # Calcular columna
                    columna = x // TAMANO_CELDA
                    if 0 <= columna < COLUMNAS:
                        juego.colocar_bloque(columna)

            # Manejar tecla Z para deshacer
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_z:
                    if juego.caretaker.tiene_historial():
                        juego.deshacer_jugada()

        # Detectar posición del mouse para resaltar columna
        mouse_x, mouse_y = pygame.mouse.get_pos()
        columna_destacada = None
        if mouse_y >= 60 and mouse_y < ALTO:
            columna = mouse_x // TAMANO_CELDA
            if 0 <= columna < COLUMNAS:
                columna_destacada = columna

        juego.dibujar(columna_destacada)
        reloj.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
