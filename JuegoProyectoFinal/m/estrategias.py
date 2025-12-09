class MovimientoStrategy:
    """Interfaz del patron Strategy para movimiento horizontal de enemigos."""

    def mover(self, enemigo):
        raise NotImplementedError

    def puede_atacar(self):
        """Indica si la estrategia permite atacar."""
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

    def puede_atacar(self):
        return True


class PatrullaPasivaStrategy(MovimientoStrategy):
    """Estrategia de patrulla pasiva: movimiento lento y sin atacar."""

    def __init__(self, factor_velocidad=0.4):
        self.factor_velocidad = factor_velocidad

    def mover(self, enemigo):
        velocidad_reducida = enemigo.velocidad_base * self.factor_velocidad
        enemigo.rect.x += velocidad_reducida * (1 if enemigo.velocidad_x > 0 else -1)

        if enemigo.rect.left <= enemigo.limite_izq:
            enemigo.rect.left = enemigo.limite_izq
            enemigo.velocidad_x = abs(enemigo.velocidad_x)
        elif enemigo.rect.right >= enemigo.limite_der:
            enemigo.rect.right = enemigo.limite_der
            enemigo.velocidad_x = -abs(enemigo.velocidad_x)

    def puede_atacar(self):
        return False


class PatrullaAgresivaStrategy(MovimientoStrategy):
    """Estrategia de patrulla agresiva: movimiento normal y puede atacar."""

    def mover(self, enemigo):
        enemigo.rect.x += enemigo.velocidad_x
        if enemigo.rect.left <= enemigo.limite_izq:
            enemigo.rect.left = enemigo.limite_izq
            enemigo.velocidad_x *= -1
        elif enemigo.rect.right >= enemigo.limite_der:
            enemigo.rect.right = enemigo.limite_der
            enemigo.velocidad_x *= -1

    def puede_atacar(self):
        return True
