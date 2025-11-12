from abc import ABC, abstractmethod
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from game import Juego


# Patrón Observer - Interfaces
class ObserverPatron(ABC):
    """Interfaz para objetos que observan cambios"""
    @abstractmethod
    def actualizar(self, subject, es_nuevo: bool):
        """
        Método que se llama cuando hay un cambio en el subject

        Args:
            subject: El objeto que notifica el cambio (otro Bloque_Observer)
            es_nuevo: True si este observer es el bloque recién colocado, False si ya existía
        """
        pass


class SubjectPatron(ABC):
    """Interfaz para objetos que pueden ser observados"""
    def __init__(self):
        self._observers: List[ObserverPatron] = []

    def agregar_observer(self, observer: ObserverPatron):
        """Agrega un observer a la lista"""
        if observer not in self._observers:
            self._observers.append(observer)

    def remover_observer(self, observer: ObserverPatron):
        """Remueve un observer de la lista"""
        if observer in self._observers:
            self._observers.remove(observer)

    def notificar_observers(self, es_nuevo: bool = False):
        """Notifica a todos los observers sobre un cambio"""
        for observer in self._observers:
            observer.actualizar(self, es_nuevo)


class Bloque_Observer(ObserverPatron, SubjectPatron):
    """Representa un bloque en el juego que puede observar y ser observado"""

    def __init__(self, valor: int, fila: int, columna: int, juego: 'Juego' = None, es_nuevo: bool = False):
        SubjectPatron.__init__(self)
        self.valor = valor
        self.fila = fila
        self.columna = columna
        self.juego = juego  # Referencia al juego para poder eliminarse
        self.es_nuevo = es_nuevo  # True si acaba de ser colocado, False si ya existía

    def actualizar(self, subject, es_nuevo: bool):
        """
        Se llama cuando un bloque vecino notifica un cambio

        Args:
            subject: El bloque vecino que notifica
            es_nuevo: True si este bloque es el recién colocado, False si ya existía
        """
        # Si este bloque NO es nuevo (es un bloque viejo) y tiene un vecino igual
        # entonces debe eliminarse (para simular la fusión)
        if not es_nuevo and self.juego is not None:
            # El bloque viejo se elimina cuando detecta un vecino igual
            self.juego.eliminar_bloque(self)

    def es_contiguo(self, otro_bloque: 'Bloque_Observer') -> bool:
        """Verifica si otro bloque es contiguo (adyacente) a este"""
        diff_fila = abs(self.fila - otro_bloque.fila)
        diff_col = abs(self.columna - otro_bloque.columna)

        # Es contiguo si está en la misma fila y columna adyacente,
        # o en la misma columna y fila adyacente
        return (diff_fila == 0 and diff_col == 1) or (diff_fila == 1 and diff_col == 0)

    def tiene_valor_igual(self, otro_bloque: 'Bloque_Observer') -> bool:
        """Verifica si otro bloque tiene el mismo valor"""
        return self.valor == otro_bloque.valor

    def actualizar_posicion(self, fila: int, columna: int):
        """Actualiza la posición del bloque (útil para la gravedad)"""
        self.fila = fila
        self.columna = columna
