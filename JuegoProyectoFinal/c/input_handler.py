import pygame

class InputHandler:
    """Clase encargada de manejar las entradas del usuario"""

    def __init__(self):
        self.teclas_movimiento_izquierda = [pygame.K_LEFT, pygame.K_a]
        self.teclas_movimiento_derecha = [pygame.K_RIGHT, pygame.K_d]
        self.teclas_salto = [pygame.K_SPACE, pygame.K_UP, pygame.K_w]

    def procesar_eventos(self):
        """Procesa los eventos de pygame y retorna si debe continuar el juego"""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False

            # Permitir cerrar con ESC
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return False

        return True

    def obtener_salto(self):
        """Verifica si se presionó una tecla de salto"""
        teclas = pygame.key.get_pressed()
        for tecla in self.teclas_salto:
            if teclas[tecla]:
                return True
        return False

    def obtener_movimiento(self, jugador):
        """Procesa el movimiento del jugador según las teclas presionadas"""
        teclas = pygame.key.get_pressed()

        # Verificar movimiento izquierda
        moviendo_izquierda = any(teclas[tecla] for tecla in self.teclas_movimiento_izquierda)

        # Verificar movimiento derecha
        moviendo_derecha = any(teclas[tecla] for tecla in self.teclas_movimiento_derecha)

        if moviendo_izquierda:
            jugador.mover_izquierda()
        elif moviendo_derecha:
            jugador.mover_derecha()
        else:
            jugador.detener()

    def obtener_input_salto_evento(self):
        """Verifica si se presionó salto en el evento actual (para saltos precisos)"""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False, False

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return False, False
                if evento.key in self.teclas_salto:
                    return True, True

        return True, False
