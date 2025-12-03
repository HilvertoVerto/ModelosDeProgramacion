class Command:
    """Interfaz del patron Command para entradas de usuario."""

    def ejecutar(self, jugador):
        raise NotImplementedError


class MoverIzquierdaCommand(Command):
    def ejecutar(self, jugador):
        jugador.mover_izquierda()


class MoverDerechaCommand(Command):
    def ejecutar(self, jugador):
        jugador.mover_derecha()


class DetenerCommand(Command):
    def ejecutar(self, jugador):
        jugador.detener()


class SaltarCommand(Command):
    def ejecutar(self, jugador):
        jugador.saltar()
