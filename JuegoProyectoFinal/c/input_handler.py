import pygame
from c.commands import (
    Command,
    DetenerCommand,
    MoverDerechaCommand,
    MoverIzquierdaCommand,
    SaltarCommand,
)


class InputHandler:
    """Clase encargada de manejar las entradas del usuario usando el patron Command."""

    def __init__(self):
        self.teclas_movimiento_izquierda = [pygame.K_LEFT, pygame.K_a]
        self.teclas_movimiento_derecha = [pygame.K_RIGHT, pygame.K_d]
        self.teclas_salto = [pygame.K_SPACE, pygame.K_UP, pygame.K_w]

        self.comando_izquierda: Command = MoverIzquierdaCommand()
        self.comando_derecha: Command = MoverDerechaCommand()
        self.comando_detener: Command = DetenerCommand()
        self.comando_salto: Command = SaltarCommand()

    def procesar_eventos(self):
        """Procesa eventos de salida de la app."""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                return False
        return True

    def manejar_movimiento(self, jugador):
        """Ejecuta comandos de movimiento segun teclas presionadas."""
        teclas = pygame.key.get_pressed()
        moviendo_izquierda = any(teclas[tecla] for tecla in self.teclas_movimiento_izquierda)
        moviendo_derecha = any(teclas[tecla] for tecla in self.teclas_movimiento_derecha)

        if moviendo_izquierda:
            self.comando_izquierda.ejecutar(jugador)
        elif moviendo_derecha:
            self.comando_derecha.ejecutar(jugador)
        else:
            self.comando_detener.ejecutar(jugador)

    def manejar_salto(self, jugador):
        """Ejecuta comando de salto si corresponde."""
        teclas = pygame.key.get_pressed()
        if any(teclas[tecla] for tecla in self.teclas_salto):
            self.comando_salto.ejecutar(jugador)
