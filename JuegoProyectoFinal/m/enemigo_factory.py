from m.armas import Arco, Baston, Espada
from m.enemigo import Enemigo
from m.estrategias import PatrullaStrategy


class EnemigoFactory:
    """Abstract Factory para crear enemigos con arma segun tipo."""

    @staticmethod
    def crear(tipo, data):
        tipo = (tipo or "").lower()
        if tipo == "arquero":
            return EnemigoFactory._crear_arquero(data)
        if tipo == "mago":
            return EnemigoFactory._crear_mago(data)
        # Default guerrero/espada
        return EnemigoFactory._crear_guerrero(data)

    @staticmethod
    def _base_enemigo(data, arma):
        return Enemigo(
            x=data.get("x", 0),
            y=data.get("y", 0),
            ancho=data.get("ancho", 48),
            alto=data.get("alto", 48),
            velocidad=data.get("velocidad", 2),
            limite_izq=data.get("limite_izq", 0),
            limite_der=data.get("limite_der", 200),
            estrategia=PatrullaStrategy(),
            arma=arma,
        )

    @staticmethod
    def _crear_guerrero(data):
        return EnemigoFactory._base_enemigo(data, Espada())

    @staticmethod
    def _crear_arquero(data):
        return EnemigoFactory._base_enemigo(data, Arco())

    @staticmethod
    def _crear_mago(data):
        return EnemigoFactory._base_enemigo(data, Baston())
