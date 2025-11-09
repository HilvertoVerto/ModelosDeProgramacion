import pygame
import sys
import random
from abc import ABC, abstractmethod

# Inicializar Pygame
pygame.init()

# Constantes
ANCHO_CUADRICULA = 6  # columnas
ALTO_CUADRICULA = 8   # filas
TAMANO_CELDA = 60
ANCHO_PANEL_LATERAL = 150  # Espacio para mostrar el próximo bloque
ANCHO_VENTANA = ANCHO_CUADRICULA * TAMANO_CELDA + ANCHO_PANEL_LATERAL
ALTO_VENTANA = ALTO_CUADRICULA * TAMANO_CELDA

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (200, 200, 200)
AZUL = (50, 150, 255)
ROJO = (255, 50, 50)
VERDE = (50, 255, 150)
AMARILLO = (255, 255, 50)

# Colores por valor de bloque
COLORES_BLOQUES = {
    2: (173, 216, 230),   # Azul claro
    4: (135, 206, 250),   # Azul cielo
    8: (70, 130, 180),    # Azul acero
    16: (100, 149, 237),  # Azul maíz
    32: (65, 105, 225),   # Azul royal
    64: (0, 0, 255),      # Azul puro
    128: (138, 43, 226),  # Violeta
    256: (75, 0, 130),    # Índigo
}

# Configurar ventana
ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Juego de Bloques")
reloj = pygame.time.Clock()


# ===== PATRÓN STRATEGY =====
class EstrategiaFusion(ABC):
    """Clase abstracta para las estrategias de fusión"""

    @abstractmethod
    def aplicar(self, valor_base):
        """Aplica la estrategia de fusión y retorna el nuevo valor"""
        pass

    @abstractmethod
    def get_nombre(self):
        """Retorna el nombre de la estrategia"""
        pass


class FusionSimple(EstrategiaFusion):
    """Estrategia 1: Un bloque adyacente igual -> multiplicar por 2"""

    def aplicar(self, valor_base):
        return valor_base * 2

    def get_nombre(self):
        return "Fusión Simple (x2)"


class FusionDoble(EstrategiaFusion):
    """Estrategia 2: Dos bloques adyacentes iguales -> multiplicar por 4"""

    def aplicar(self, valor_base):
        return valor_base * 4

    def get_nombre(self):
        return "Fusión Doble (x4)"


class FusionTriple(EstrategiaFusion):
    """Estrategia 3: Tres bloques adyacentes iguales -> multiplicar por 8"""

    def aplicar(self, valor_base):
        return valor_base * 8

    def get_nombre(self):
        return "Fusión Triple (x8)"


# Crear la cuadrícula (0 = vacío, 2/4/8 = bloques con valores)
cuadricula = [[0 for _ in range(ANCHO_CUADRICULA)] for _ in range(ALTO_CUADRICULA)]

# Variables del juego
game_over = False
columna_seleccionada = 0  # Columna donde se colocará el siguiente bloque
puntuacion = 0
proximo_bloque = None  # Almacena el valor del próximo bloque a colocar


def generar_bloque_aleatorio():
    """Genera un valor aleatorio para un nuevo bloque.
    Probabilidades: 2 (70%), 4 (25%), 8 (5%)"""
    rand = random.random()
    if rand < 0.70:
        return 2
    elif rand < 0.95:
        return 4
    else:
        return 8


# Inicializar el primer bloque
proximo_bloque = generar_bloque_aleatorio()


def dibujar_cuadricula():
    """Dibuja la cuadrícula y los bloques"""
    ventana.fill(BLANCO)

    # Dibujar las celdas
    for fila in range(ALTO_CUADRICULA):
        for col in range(ANCHO_CUADRICULA):
            x = col * TAMANO_CELDA
            y = fila * TAMANO_CELDA

            # Dibujar bloque si está ocupado
            if cuadricula[fila][col] != 0:
                valor = cuadricula[fila][col]
                color = COLORES_BLOQUES.get(valor, AZUL)
                pygame.draw.rect(ventana, color, (x, y, TAMANO_CELDA, TAMANO_CELDA))
                pygame.draw.rect(ventana, NEGRO, (x, y, TAMANO_CELDA, TAMANO_CELDA), 2)

                # Dibujar el número en el centro del bloque
                fuente = pygame.font.Font(None, 32)
                texto = fuente.render(str(valor), True, NEGRO)
                rect_texto = texto.get_rect(center=(x + TAMANO_CELDA // 2, y + TAMANO_CELDA // 2))
                ventana.blit(texto, rect_texto)
            else:
                # Dibujar borde de celda vacía
                pygame.draw.rect(ventana, GRIS, (x, y, TAMANO_CELDA, TAMANO_CELDA), 1)

    # Destacar columna seleccionada
    if not game_over:
        x = columna_seleccionada * TAMANO_CELDA
        pygame.draw.rect(ventana, ROJO, (x, 0, TAMANO_CELDA, ALTO_VENTANA), 3)

    # Mostrar puntuación
    fuente = pygame.font.Font(None, 28)
    texto_puntos = fuente.render(f"Puntos: {puntuacion}", True, NEGRO)
    ventana.blit(texto_puntos, (10, 10))

    # Mostrar próximo bloque en el panel lateral
    if not game_over and proximo_bloque is not None:
        panel_x = ANCHO_CUADRICULA * TAMANO_CELDA + 20
        panel_y = 100

        # Dibujar etiqueta "Próximo:"
        fuente_label = pygame.font.Font(None, 24)
        texto_proximo = fuente_label.render("Proximo:", True, NEGRO)
        ventana.blit(texto_proximo, (panel_x, panel_y - 30))

        # Dibujar el bloque próximo
        color = COLORES_BLOQUES.get(proximo_bloque, AZUL)
        tamano_preview = 50
        pygame.draw.rect(ventana, color, (panel_x, panel_y, tamano_preview, tamano_preview))
        pygame.draw.rect(ventana, NEGRO, (panel_x, panel_y, tamano_preview, tamano_preview), 2)

        # Dibujar el número en el centro del bloque
        fuente_numero = pygame.font.Font(None, 28)
        texto_numero = fuente_numero.render(str(proximo_bloque), True, NEGRO)
        rect_numero = texto_numero.get_rect(center=(panel_x + tamano_preview // 2, panel_y + tamano_preview // 2))
        ventana.blit(texto_numero, rect_numero)


def colocar_bloque(columna):
    """Coloca un bloque en la columna especificada (empieza desde arriba)"""
    global proximo_bloque

    # Verificar si la columna está llena (game over)
    if cuadricula[0][columna] != 0:
        return False

    # Colocar el bloque en la primera fila usando el próximo bloque predefinido
    cuadricula[0][columna] = proximo_bloque

    # Generar el siguiente bloque
    proximo_bloque = generar_bloque_aleatorio()

    return True


def aplicar_gravedad():
    """Hace que los bloques caigan hasta apilarse"""
    # Recorrer de abajo hacia arriba
    for fila in range(ALTO_CUADRICULA - 2, -1, -1):
        for col in range(ANCHO_CUADRICULA):
            if cuadricula[fila][col] != 0:
                # Buscar hasta dónde puede caer el bloque
                fila_destino = fila
                while fila_destino + 1 < ALTO_CUADRICULA and cuadricula[fila_destino + 1][col] == 0:
                    fila_destino += 1

                # Mover el bloque
                if fila_destino != fila:
                    cuadricula[fila_destino][col] = cuadricula[fila][col]
                    cuadricula[fila][col] = 0


def contar_adyacentes_iguales(fila, col):
    """Cuenta cuántos bloques adyacentes (arriba, abajo, izquierda, derecha)
    tienen el mismo valor que el bloque en (fila, col)"""
    valor = cuadricula[fila][col]
    if valor == 0:
        return 0, []

    adyacentes = []
    # Verificar las 4 direcciones (arriba, abajo, izquierda, derecha)
    direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for df, dc in direcciones:
        nueva_fila = fila + df
        nueva_col = col + dc

        # Verificar que esté dentro de los límites
        if 0 <= nueva_fila < ALTO_CUADRICULA and 0 <= nueva_col < ANCHO_CUADRICULA:
            if cuadricula[nueva_fila][nueva_col] == valor:
                adyacentes.append((nueva_fila, nueva_col))

    return len(adyacentes), adyacentes


def aplicar_fusiones():
    """Detecta y aplica las fusiones de bloques adyacentes usando el patrón Strategy.
    Estrategia 1: 1 adyacente igual -> x2
    Estrategia 2: 2 adyacentes iguales -> x4
    Estrategia 3: 3 adyacentes iguales -> x8"""
    global puntuacion

    # Crear las instancias de las estrategias
    estrategia_simple = FusionSimple()
    estrategia_doble = FusionDoble()
    estrategia_triple = FusionTriple()

    # Marcar bloques ya procesados en esta ronda de fusiones
    procesados = set()
    fusiones_realizadas = False

    # Recorrer toda la cuadrícula buscando fusiones
    for fila in range(ALTO_CUADRICULA):
        for col in range(ANCHO_CUADRICULA):
            if cuadricula[fila][col] != 0 and (fila, col) not in procesados:
                valor = cuadricula[fila][col]
                num_adyacentes, posiciones_adyacentes = contar_adyacentes_iguales(fila, col)

                if num_adyacentes >= 1:
                    # Determinar qué estrategia usar según el número de adyacentes
                    estrategia = None
                    bloques_a_eliminar = posiciones_adyacentes.copy()

                    if num_adyacentes >= 3:
                        # Estrategia 3: Tres bloques adyacentes -> multiplicar por 8
                        estrategia = estrategia_triple
                        # Solo tomar los primeros 3 adyacentes
                        bloques_a_eliminar = posiciones_adyacentes[:3]
                    elif num_adyacentes == 2:
                        # Estrategia 2: Dos bloques adyacentes -> multiplicar por 4
                        estrategia = estrategia_doble
                    elif num_adyacentes == 1:
                        # Estrategia 1: Un bloque adyacente -> multiplicar por 2
                        estrategia = estrategia_simple

                    if estrategia:
                        # Aplicar la estrategia
                        nuevo_valor = estrategia.aplicar(valor)

                        # Actualizar el bloque principal
                        cuadricula[fila][col] = nuevo_valor
                        puntuacion += nuevo_valor

                        # Eliminar los bloques adyacentes que se fusionaron
                        for f, c in bloques_a_eliminar:
                            cuadricula[f][c] = 0
                            procesados.add((f, c))

                        procesados.add((fila, col))
                        fusiones_realizadas = True

    return fusiones_realizadas


def verificar_game_over():
    """Verifica si hay bloques en la primera fila"""
    for col in range(ANCHO_CUADRICULA):
        if cuadricula[0][col] != 0:
            return True
    return False


def mostrar_game_over():
    """Muestra el mensaje de game over"""
    fuente = pygame.font.Font(None, 48)
    texto = fuente.render("GAME OVER", True, ROJO)
    rect_texto = texto.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2))
    ventana.blit(texto, rect_texto)

    fuente_small = pygame.font.Font(None, 24)
    texto_reinicio = fuente_small.render("Presiona R para reiniciar", True, NEGRO)
    rect_reinicio = texto_reinicio.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 + 50))
    ventana.blit(texto_reinicio, rect_reinicio)


def reiniciar_juego():
    """Reinicia el juego"""
    global cuadricula, game_over, columna_seleccionada, puntuacion, proximo_bloque
    cuadricula = [[0 for _ in range(ANCHO_CUADRICULA)] for _ in range(ALTO_CUADRICULA)]
    game_over = False
    columna_seleccionada = 0
    puntuacion = 0
    proximo_bloque = generar_bloque_aleatorio()


# Loop principal del juego
ejecutando = True
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

        if evento.type == pygame.KEYDOWN:
            if game_over:
                # Reiniciar juego
                if evento.key == pygame.K_r:
                    reiniciar_juego()
            else:
                # Cambiar columna seleccionada
                if evento.key == pygame.K_LEFT:
                    columna_seleccionada = max(0, columna_seleccionada - 1)
                elif evento.key == pygame.K_RIGHT:
                    columna_seleccionada = min(ANCHO_CUADRICULA - 1, columna_seleccionada + 1)

                # Colocar bloque con ESPACIO o teclas numéricas
                elif evento.key == pygame.K_SPACE:
                    if colocar_bloque(columna_seleccionada):
                        aplicar_gravedad()
                        # Aplicar fusiones múltiples veces hasta que no haya más fusiones
                        while aplicar_fusiones():
                            aplicar_gravedad()
                        if verificar_game_over():
                            game_over = True

                # Colocar con teclas numéricas (1-6)
                elif pygame.K_1 <= evento.key <= pygame.K_6:
                    col = evento.key - pygame.K_1
                    if col < ANCHO_CUADRICULA:
                        if colocar_bloque(col):
                            aplicar_gravedad()
                            # Aplicar fusiones múltiples veces hasta que no haya más fusiones
                            while aplicar_fusiones():
                                aplicar_gravedad()
                            if verificar_game_over():
                                game_over = True

    # Dibujar
    dibujar_cuadricula()

    if game_over:
        mostrar_game_over()

    pygame.display.flip()
    reloj.tick(60)

pygame.quit()
sys.exit()
