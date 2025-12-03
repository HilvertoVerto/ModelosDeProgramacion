from m.proyectil import Proyectil


class Arma:
    """Arma base para enemigos."""

    def __init__(self, nombre, dano, alcance, color, cooldown_ms, velocidad_proj):
        self.nombre = nombre
        self.dano = dano
        self.alcance = alcance
        self.color = color
        self.cooldown_ms = cooldown_ms
        self.velocidad_proj = velocidad_proj

    def crear_proyectil(self, origen_rect, direccion):
        """Crea un proyectil dirigido segun la arma. direccion: -1 izq, 1 der."""
        vx = self.velocidad_proj * direccion
        vy = 0
        x = origen_rect.centerx + (origen_rect.width // 2) * direccion
        y = origen_rect.centery
        return Proyectil(x, y, vx, vy, color=self.color, dano=self.dano)


class Espada(Arma):
    """Arma de contacto: no dispara proyectiles."""

    def __init__(self):
        super().__init__("Espada", dano=15, alcance=1, color=(200, 80, 80), cooldown_ms=800, velocidad_proj=0)

    def crear_proyectil(self, origen_rect, direccion):
        return None


class Arco(Arma):
    def __init__(self):
        super().__init__("Arco", dano=10, alcance=5, color=(80, 120, 200), cooldown_ms=1200, velocidad_proj=6)


class Baston(Arma):
    def __init__(self):
        super().__init__("Baston", dano=12, alcance=4, color=(180, 60, 200), cooldown_ms=1500, velocidad_proj=4)
