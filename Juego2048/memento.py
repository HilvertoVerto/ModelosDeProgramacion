from typing import List, Optional


# Patrón Memento - Para deshacer jugadas
class Memento:
    """Guarda el estado del juego en un momento dado"""

    def __init__(self, cuadricula_estado, proximo_numero):
        """
        Args:
            cuadricula_estado: Copia profunda de la cuadrícula del juego
            proximo_numero: El próximo número que se colocará
        """
        self._cuadricula_estado = cuadricula_estado
        self._proximo_numero = proximo_numero

    def obtener_estado(self):
        """Retorna el estado guardado"""
        return self._cuadricula_estado, self._proximo_numero


class Caretaker:
    """Maneja el historial de estados del juego"""

    def __init__(self, max_historial=20):
        """
        Args:
            max_historial: Cantidad máxima de estados a guardar
        """
        self._historial: List[Memento] = []
        self._max_historial = max_historial

    def guardar(self, memento: Memento):
        """Guarda un estado en el historial"""
        self._historial.append(memento)

        # Limitar el tamaño del historial
        if len(self._historial) > self._max_historial:
            self._historial.pop(0)

    def deshacer(self) -> Optional[Memento]:
        """Retorna el último estado guardado y lo elimina del historial"""
        if len(self._historial) > 0:
            return self._historial.pop()
        return None

    def tiene_historial(self) -> bool:
        """Verifica si hay estados guardados"""
        return len(self._historial) > 0
