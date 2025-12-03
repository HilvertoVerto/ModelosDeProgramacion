class MovimientoStrategy:
    """Interfaz del patron Strategy para movimiento horizontal de enemigos."""

    def mover(self, enemigo):
        raise NotImplementedError


class PatrullaStrategy(MovimientoStrategy):
    """Estrategia de patrulla entre dos limites."""

    def mover(self, enemigo):
        enemigo.rect.x += enemigo.velocidad_x
        if enemigo.rect.left <= enemigo.limite_izq:
            enemigo.rect.left = enemigo.limite_izq
            enemigo.velocidad_x *= -1
        elif enemigo.rect.right >= enemigo.limite_der:
            enemigo.rect.right = enemigo.limite_der
            enemigo.velocidad_x *= -1
