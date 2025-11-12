import random
import pygame
from typing import List, Optional

from constants import (
    FILAS, COLUMNAS, TAMANO_CELDA, ANCHO, ALTO,
    BLANCO, NEGRO, GRIS, GRIS_OSCURO, ROJO,
    COLOR_2, COLOR_4, COLOR_8, COLOR_16, COLOR_32, COLOR_64,
    COLOR_128, COLOR_256, COLOR_512, COLOR_1024, COLOR_2048,
    pantalla, fuente, fuente_pequena
)
from memento import Memento, Caretaker
from strategy import ContextoMultiplicacion
from observer import Bloque_Observer


class Juego:
    def __init__(self):
        self.cuadricula: List[List[Optional[Bloque_Observer]]] = [[None for _ in range(COLUMNAS)] for _ in range(FILAS)]
        self.cayendo = False
        self.proximo_numero = self.generar_numero()  # Número que se colocará
        self.caretaker = Caretaker()  # Maneja el historial de estados
        self.contexto_multiplicacion = ContextoMultiplicacion()  # Patrón Estrategia para multiplicación

    def generar_numero(self):
        """Genera un número aleatorio: 2, 4 u 8"""
        return random.choice([2, 4, 8])

    def crear_memento(self) -> Memento:
        """Crea un memento con el estado actual del juego"""
        # Hacer una copia profunda de la cuadrícula
        cuadricula_copia = []
        for fila in self.cuadricula:
            fila_copia = []
            for bloque in fila:
                if bloque is None:
                    fila_copia.append(None)
                else:
                    # Crear una copia del bloque
                    bloque_copia = Bloque_Observer(bloque.valor, bloque.fila, bloque.columna, self, bloque.es_nuevo)
                    fila_copia.append(bloque_copia)
            cuadricula_copia.append(fila_copia)

        return Memento(cuadricula_copia, self.proximo_numero)

    def restaurar_memento(self, memento: Memento):
        """Restaura el estado del juego desde un memento"""
        if memento is None:
            return

        cuadricula_estado, proximo_numero = memento.obtener_estado()

        # Restaurar la cuadrícula
        self.cuadricula = cuadricula_estado
        # Actualizar la referencia al juego en todos los bloques
        for fila in self.cuadricula:
            for bloque in fila:
                if bloque is not None:
                    bloque.juego = self

        # Restaurar el próximo número
        self.proximo_numero = proximo_numero

    def obtener_bloque(self, fila: int, columna: int) -> Optional[Bloque_Observer]:
        """Obtiene el bloque en la posición especificada"""
        if 0 <= fila < FILAS and 0 <= columna < COLUMNAS:
            return self.cuadricula[fila][columna]
        return None

    def obtener_bloques_contiguos(self, bloque: Bloque_Observer) -> List[Bloque_Observer]:
        """Obtiene todos los bloques contiguos a un bloque dado"""
        contiguos = []
        posiciones = [
            (bloque.fila - 1, bloque.columna),  # Arriba
            (bloque.fila + 1, bloque.columna),  # Abajo
            (bloque.fila, bloque.columna - 1),  # Izquierda
            (bloque.fila, bloque.columna + 1),  # Derecha
        ]

        for fila, col in posiciones:
            vecino = self.obtener_bloque(fila, col)
            if vecino is not None:
                contiguos.append(vecino)

        return contiguos

    def eliminar_bloque(self, bloque: Bloque_Observer):
        """Elimina un bloque de la cuadrícula"""
        if 0 <= bloque.fila < FILAS and 0 <= bloque.columna < COLUMNAS:
            self.cuadricula[bloque.fila][bloque.columna] = None

    def configurar_observers(self, nuevo_bloque: Bloque_Observer):
        """
        Configura las relaciones de observer entre el nuevo bloque y sus vecinos contiguos.
        Los bloques se observan mutuamente si tienen el mismo valor.
        Si el nuevo bloque tiene vecinos con el mismo valor, usa el patrón Estrategia para
        calcular su nuevo valor (×2 con 1 vecino, ×4 con 2 vecinos, ×8 con 3 vecinos).
        Este proceso se repite recursivamente hasta que no haya más fusiones.
        """
        bloques_contiguos = self.obtener_bloques_contiguos(nuevo_bloque)
        vecinos_iguales = []

        # Encontrar todos los vecinos con el mismo valor
        for vecino in bloques_contiguos:
            if nuevo_bloque.tiene_valor_igual(vecino):
                vecinos_iguales.append(vecino)

        # Si hay vecinos con el mismo valor, usar el patrón Estrategia para calcular el nuevo valor
        if len(vecinos_iguales) > 0:
            # Usar el contexto de multiplicación con la estrategia apropiada
            nuevo_bloque.valor = self.contexto_multiplicacion.calcular_nuevo_valor(
                nuevo_bloque.valor,
                len(vecinos_iguales)
            )

        # Ahora establecer las relaciones de observación
        for vecino in vecinos_iguales:
            # El nuevo bloque observa al vecino
            vecino.agregar_observer(nuevo_bloque)
            # El vecino observa al nuevo bloque
            nuevo_bloque.agregar_observer(vecino)

            # Notificar al vecino que hay un nuevo bloque contiguo con el mismo valor
            # El vecino NO es nuevo (es_nuevo=False), por lo que se eliminará
            vecino.actualizar(nuevo_bloque, es_nuevo=False)

        # Después de eliminar los bloques viejos, aplicar gravedad
        if len(vecinos_iguales) > 0:
            self.aplicar_gravedad()

            # Re-evaluar si el bloque con su nuevo valor tiene más vecinos iguales
            # Esto permite fusiones en cadena
            self.configurar_observers(nuevo_bloque)
        else:
            # Solo notificar cuando ya no hay más fusiones posibles
            # El nuevo bloque notifica que ha sido colocado
            # Este bloque SÍ es nuevo (es_nuevo=True)
            nuevo_bloque.notificar_observers(es_nuevo=True)

    def deshacer_jugada(self):
        """Deshace la última jugada restaurando el estado anterior"""
        memento = self.caretaker.deshacer()
        self.restaurar_memento(memento)

    def colocar_bloque(self, columna):
        """Coloca un bloque en la columna especificada"""
        if self.cayendo:
            return

        # Verificar si la columna está llena
        if self.cuadricula[0][columna] is not None:
            return

        # Guardar el estado actual antes de hacer cambios (Patrón Memento)
        memento = self.crear_memento()
        self.caretaker.guardar(memento)

        # Usar el número precalculado
        numero = self.proximo_numero

        # Crear el nuevo bloque marcándolo como recién colocado
        nuevo_bloque = Bloque_Observer(numero, 0, columna, juego=self, es_nuevo=True)

        # Colocar en la primera fila
        self.cuadricula[0][columna] = nuevo_bloque

        # Aplicar gravedad
        self.aplicar_gravedad()

        # Después de aplicar gravedad, configurar los observers
        # (el bloque ya estará en su posición final)
        self.configurar_observers(nuevo_bloque)

        # Generar el próximo número
        self.proximo_numero = self.generar_numero()

    def aplicar_gravedad(self):
        """Hace que los bloques caigan hacia abajo"""
        movimiento = True
        while movimiento:
            movimiento = False
            # Recorrer de abajo hacia arriba
            for fila in range(FILAS - 2, -1, -1):
                for col in range(COLUMNAS):
                    # Si hay un bloque y el espacio debajo está vacío
                    if self.cuadricula[fila][col] is not None and self.cuadricula[fila + 1][col] is None:
                        # Mover el bloque hacia abajo
                        bloque = self.cuadricula[fila][col]
                        self.cuadricula[fila + 1][col] = bloque
                        self.cuadricula[fila][col] = None
                        # Actualizar la posición interna del bloque
                        bloque.actualizar_posicion(fila + 1, col)
                        movimiento = True

    def obtener_color(self, numero):
        """Retorna el color según el número"""
        colores = {
            2: COLOR_2,
            4: COLOR_4,
            8: COLOR_8,
            16: COLOR_16,
            32: COLOR_32,
            64: COLOR_64,
            128: COLOR_128,
            256: COLOR_256,
            512: COLOR_512,
            1024: COLOR_1024,
            2048: COLOR_2048
        }
        return colores.get(numero, BLANCO)

    def dibujar(self, columna_destacada=None):
        """Dibuja el juego en la pantalla

        Args:
            columna_destacada: Columna a resaltar con borde rojo (None si no hay)
        """
        pantalla.fill(BLANCO)

        # Dibujar cuadrícula
        for fila in range(FILAS):
            for col in range(COLUMNAS):
                x = col * TAMANO_CELDA
                y = fila * TAMANO_CELDA + 60

                # Dibujar celda (con borde rojo si es la columna destacada)
                color_borde = ROJO if col == columna_destacada else GRIS
                grosor_borde = 3 if col == columna_destacada else 2
                pygame.draw.rect(pantalla, color_borde, (x, y, TAMANO_CELDA, TAMANO_CELDA), grosor_borde)

                # Dibujar número si existe
                bloque = self.cuadricula[fila][col]
                if bloque is not None:
                    color = self.obtener_color(bloque.valor)
                    pygame.draw.rect(pantalla, color, (x + 2, y + 2, TAMANO_CELDA - 4, TAMANO_CELDA - 4))

                    # Dibujar número (con contraste según el valor)
                    color_texto = BLANCO if bloque.valor >= 8 else NEGRO
                    texto = fuente.render(str(bloque.valor), True, color_texto)
                    texto_rect = texto.get_rect(center=(x + TAMANO_CELDA // 2, y + TAMANO_CELDA // 2))
                    pantalla.blit(texto, texto_rect)

        # Dibujar instrucciones
        instrucciones = fuente_pequena.render("Haz clic en una columna para colocar un bloque", True, NEGRO)
        pantalla.blit(instrucciones, (10, 10))

        # Dibujar vista previa del próximo bloque
        texto_proximo = fuente_pequena.render("Próximo:", True, NEGRO)
        pantalla.blit(texto_proximo, (10, 30))

        # Dibujar el bloque próximo
        x_preview = 100
        y_preview = 25
        tamano_preview = 40
        color_preview = self.obtener_color(self.proximo_numero)
        pygame.draw.rect(pantalla, color_preview, (x_preview, y_preview, tamano_preview, tamano_preview))
        pygame.draw.rect(pantalla, GRIS_OSCURO, (x_preview, y_preview, tamano_preview, tamano_preview), 2)

        # Dibujar el número del próximo bloque (con contraste)
        color_texto_preview = BLANCO if self.proximo_numero >= 8 else NEGRO
        texto_num = fuente_pequena.render(str(self.proximo_numero), True, color_texto_preview)
        texto_num_rect = texto_num.get_rect(center=(x_preview + tamano_preview // 2, y_preview + tamano_preview // 2))
        pantalla.blit(texto_num, texto_num_rect)

        # Dibujar botón de deshacer
        boton_x = ANCHO - 120
        boton_y = 10
        boton_ancho = 110
        boton_alto = 50

        # Color del botón depende de si hay historial
        if self.caretaker.tiene_historial():
            color_boton = (100, 200, 100)  # Verde si se puede deshacer
        else:
            color_boton = GRIS  # Gris si no hay historial

        pygame.draw.rect(pantalla, color_boton, (boton_x, boton_y, boton_ancho, boton_alto))
        pygame.draw.rect(pantalla, NEGRO, (boton_x, boton_y, boton_ancho, boton_alto), 2)

        # Texto del botón
        texto_boton = fuente_pequena.render("Deshacer (Z)", True, NEGRO)
        texto_boton_rect = texto_boton.get_rect(center=(boton_x + boton_ancho // 2, boton_y + boton_alto // 2))
        pantalla.blit(texto_boton, texto_boton_rect)

        pygame.display.flip()

    def obtener_rect_boton_deshacer(self):
        """Retorna el rectángulo del botón de deshacer"""
        boton_x = ANCHO - 120
        boton_y = 10
        boton_ancho = 110
        boton_alto = 50
        return pygame.Rect(boton_x, boton_y, boton_ancho, boton_alto)
