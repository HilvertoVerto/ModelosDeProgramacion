import pygame


class BuffManager:
    """
    Administra buffos activos: aplica decoradores al jugador, controla expiracion
    y expone datos para HUD.
    """

    DURACIONES_MS = {"velocidad": 6000, "salto": 6000, "invencible": 5000}

    def __init__(self, buff_classes):
        self.buff_classes = buff_classes
        self.activos = {}  # tipo -> {"decorator": obj, "expira": ms, "inicio": ms, "duracion": ms}

    def reset(self):
        self.activos = {}

    def activar(self, tipo, ahora):
        duracion = self.DURACIONES_MS.get(tipo, 5000)
        if tipo in self.activos:
            entry = self.activos[tipo]
            entry["decorator"].add_stack()
            entry["expira"] = ahora + duracion
            entry["inicio"] = ahora
            entry["duracion"] = duracion
        else:
            clase = self.buff_classes.get(tipo)
            if not clase:
                return
            decorador = clase()
            self.activos[tipo] = {
                "decorator": decorador,
                "expira": ahora + duracion,
                "inicio": ahora,
                "duracion": duracion,
            }

    def aplicar(self, jugador, ahora=None):
        """Purga expirados, aplica efectos y retorna timers para HUD."""
        if ahora is None:
            ahora = pygame.time.get_ticks()

        expirados = [tipo for tipo, data in self.activos.items() if ahora > data["expira"]]
        for tipo in expirados:
            del self.activos[tipo]

        jugador.reset_estadisticas()
        escala_total = 1.0
        auras = []
        timers = {}

        for tipo, entry in self.activos.items():
            decorador = entry["decorator"]
            visual = decorador.aplicar(jugador)
            escala_total *= visual.get("escala_extra", 1.0)

            size = visual.get("aura_size", 0)
            color = visual.get("aura_color")
            if color and size > 0:
                auras.append({"color": color, "size": size})

            restante = max(0.0, (entry["expira"] - ahora) / 1000.0)
            duracion = max(0.1, entry.get("duracion", self.DURACIONES_MS.get(tipo, 5000)) / 1000.0)
            timers[tipo] = {"restante": restante, "duracion": duracion}

        jugador.set_visual(escala=escala_total, auras=auras)
        return timers
