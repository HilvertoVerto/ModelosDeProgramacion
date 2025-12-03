from m.jugador import Jugador


class BuffDecorator:
    """Decorador base para efectos de buffo."""

    def __init__(self):
        self.stacks = 1

    def add_stack(self):
        self.stacks = min(self.stacks + 1, 5)

    def aplicar(self, jugador: Jugador):
        """Aplica efecto al jugador. Devuelve dict con apariencia opcional."""
        raise NotImplementedError

    def get_visual(self):
        """Retorna tinte/aura para mezclar en render."""
        return {}


class VelocidadBuff(BuffDecorator):
    def __init__(self):
        super().__init__()
        self.aura_color = (255, 230, 150)
        self.aura_base = 10
        self.aura_inc = 6

    def aplicar(self, jugador: Jugador):
        factor = 1 + 0.3 * self.stacks
        jugador.aplicar_multiplicador_velocidad(factor)
        return {
            "aura_color": self.aura_color,
            "aura_size": self.aura_base + self.aura_inc * (self.stacks - 1),
            "escala_extra": 1 + 0.03 * self.stacks,
        }


class SaltoBuff(BuffDecorator):
    def __init__(self):
        super().__init__()
        self.aura_color = (180, 60, 200)
        self.aura_base = 8
        self.aura_inc = 5

    def aplicar(self, jugador: Jugador):
        factor = 1 + 0.2 * self.stacks
        jugador.aplicar_impulso_salto(factor)
        return {
            "aura_color": self.aura_color,
            "aura_size": self.aura_base + self.aura_inc * (self.stacks - 1),
            "escala_extra": 1 + 0.02 * self.stacks,
        }


class InvencibleBuff(BuffDecorator):
    def __init__(self):
        super().__init__()
        self.aura_color = (120, 220, 180)
        self.aura_base = 12
        self.aura_inc = 6

    def aplicar(self, jugador: Jugador):
        jugador.set_invencible(True)
        return {
            "aura_color": self.aura_color,
            "aura_size": self.aura_base + self.aura_inc * (self.stacks - 1),
            "escala_extra": 1 + 0.04 * self.stacks,
        }
