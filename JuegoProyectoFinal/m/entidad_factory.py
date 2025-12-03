from m.enemigo_factory import EnemigoFactory
from m.buff import Buff


class EntidadFactory:
    """Factory Method para instanciar entidades desde datos simples."""

    @staticmethod
    def crear_enemigos(datos_enemigos):
        enemigos = []
        for data in datos_enemigos:
            enemigo = EnemigoFactory.crear(data.get("tipo", "guerrero"), data)
            enemigos.append(enemigo)
        return enemigos

    @staticmethod
    def crear_buffos(datos_buffos):
        return [Buff.desde_dict(data) for data in datos_buffos]
