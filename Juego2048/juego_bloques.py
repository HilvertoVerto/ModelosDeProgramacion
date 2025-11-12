import pygame
import random
import sys
import copy
from abc import ABC, abstractmethod
from typing import List, Optional

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

# Paleta de colores para bloques (estilo 2048)
COLOR_2 = (238, 228, 218)
COLOR_4 = (237, 224, 200)
COLOR_8 = (242, 177, 121)
COLOR_16 = (245, 149, 99)
COLOR_32 = (246, 124, 95)
COLOR_64 = (246, 94, 59)
COLOR_128 = (237, 207, 114)
COLOR_256 = (237, 204, 97)
COLOR_512 = (237, 200, 80)
COLOR_1024 = (237, 197, 63)
COLOR_2048 = (237, 194, 46)

# Configurar ventana
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego de Bloques")
reloj = pygame.time.Clock()

# Fuente
fuente = pygame.font.Font(None, 48)
fuente_pequena = pygame.font.Font(None, 24)


# Patrón Memento - Para deshacer jugadas
class Memento:
    """Guarda el estado del juego en un momento dado"""

    def __init__(self, cuadricula_estado, proximo_numero):
        """
        Args:
            cuadricula_estado: Copia profunda de la cuadrícula del juego
            proximo_numero: El próximo número que se colocará
        """
        self._cuadricula_estado = cuadricula_estado
        self._proximo_numero = proximo_numero

    def obtener_estado(self):
        """Retorna el estado guardado"""
        return self._cuadricula_estado, self._proximo_numero


class Caretaker:
    """Maneja el historial de estados del juego"""

    def __init__(self, max_historial=20):
        """
        Args:
            max_historial: Cantidad máxima de estados a guardar
        """
        self._historial: List[Memento] = []
        self._max_historial = max_historial

    def guardar(self, memento: Memento):
        """Guarda un estado en el historial"""
        self._historial.append(memento)

        # Limitar el tamaño del historial
        if len(self._historial) > self._max_historial:
            self._historial.pop(0)

    def deshacer(self) -> Optional[Memento]:
        """Retorna el último estado guardado y lo elimina del historial"""
        if len(self._historial) > 0:
            return self._historial.pop()
        return None

    def tiene_historial(self) -> bool:
        """Verifica si hay estados guardados"""
        return len(self._historial) > 0


# Patrón Observer - Interfaces
class ObserverPatron(ABC):
    """Interfaz para objetos que observan cambios"""
    @abstractmethod
    def actualizar(self, subject, es_nuevo: bool):
        """
        Método que se llama cuando hay un cambio en el subject

        Args:
            subject: El objeto que notifica el cambio (otro Bloque_Observer)
            es_nuevo: True si este observer es el bloque recién colocado, False si ya existía
        """
        pass


class SubjectPatron(ABC):
    """Interfaz para objetos que pueden ser observados"""
    def __init__(self):
        self._observers: List[ObserverPatron] = []

    def agregar_observer(self, observer: ObserverPatron):
        """Agrega un observer a la lista"""
        if observer not in self._observers:
            self._observers.append(observer)

    def remover_observer(self, observer: ObserverPatron):
        """Remueve un observer de la lista"""
        if observer in self._observers:
            self._observers.remove(observer)

    def notificar_observers(self, es_nuevo: bool = False):
        """Notifica a todos los observers sobre un cambio"""
        for observer in self._observers:
            observer.actualizar(self, es_nuevo)


class Bloque_Observer(ObserverPatron, SubjectPatron):
    """Representa un bloque en el juego que puede observar y ser observado"""

    def __init__(self, valor: int, fila: int, columna: int, juego: 'Juego' = None, es_nuevo: bool = False):
        SubjectPatron.__init__(self)
        self.valor = valor
        self.fila = fila
        self.columna = columna
        self.juego = juego  # Referencia al juego para poder eliminarse
        self.es_nuevo = es_nuevo  # True si acaba de ser colocado, False si ya existía

    def actualizar(self, subject, es_nuevo: bool):
        """
        Se llama cuando un bloque vecino notifica un cambio

        Args:
            subject: El bloque vecino que notifica
            es_nuevo: True si este bloque es el recién colocado, False si ya existía
        """
        # Si este bloque NO es nuevo (es un bloque viejo) y tiene un vecino igual
        # entonces debe eliminarse (para simular la fusión)
        if not es_nuevo and self.juego is not None:
            # El bloque viejo se elimina cuando detecta un vecino igual
            self.juego.eliminar_bloque(self)

    def es_contiguo(self, otro_bloque: 'Bloque_Observer') -> bool:
        """Verifica si otro bloque es contiguo (adyacente) a este"""
        diff_fila = abs(self.fila - otro_bloque.fila)
        diff_col = abs(self.columna - otro_bloque.columna)

        # Es contiguo si está en la misma fila y columna adyacente,
        # o en la misma columna y fila adyacente
        return (diff_fila == 0 and diff_col == 1) or (diff_fila == 1 and diff_col == 0)

    def tiene_valor_igual(self, otro_bloque: 'Bloque_Observer') -> bool:
        """Verifica si otro bloque tiene el mismo valor"""
        return self.valor == otro_bloque.valor

    def actualizar_posicion(self, fila: int, columna: int):
        """Actualiza la posición del bloque (útil para la gravedad)"""
        self.fila = fila
        self.columna = columna


class Juego:
    def __init__(self):
        self.cuadricula: List[List[Optional[Bloque_Observer]]] = [[None for _ in range(COLUMNAS)] for _ in range(FILAS)]
        self.cayendo = False
        self.proximo_numero = self.generar_numero()  # Número que se colocará
        self.caretaker = Caretaker()  # Maneja el historial de estados

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
        Si el nuevo bloque tiene vecinos con el mismo valor, se multiplica por 2^n donde n es la cantidad de vecinos.
        Este proceso se repite recursivamente hasta que no haya más fusiones.
        """
        bloques_contiguos = self.obtener_bloques_contiguos(nuevo_bloque)
        vecinos_iguales = []

        # Encontrar todos los vecinos con el mismo valor
        for vecino in bloques_contiguos:
            if nuevo_bloque.tiene_valor_igual(vecino):
                vecinos_iguales.append(vecino)

        # Si hay vecinos con el mismo valor, multiplicar el valor del nuevo bloque
        if len(vecinos_iguales) > 0:
            # Multiplicar por 2^n donde n es la cantidad de vecinos iguales
            multiplicador = 2 ** len(vecinos_iguales)
            nuevo_bloque.valor *= multiplicador

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

        juego.dibujar()
        reloj.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
