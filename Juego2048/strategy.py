from abc import ABC, abstractmethod


# Patrón Estrategia - Para calcular multiplicación de bloques
class EstrategiaMultiplicacion(ABC):
    """Interfaz para estrategias de multiplicación de bloques"""

    @abstractmethod
    def calcular_multiplicador(self, cantidad_vecinos: int) -> int:
        """
        Calcula el multiplicador según la cantidad de vecinos iguales

        Args:
            cantidad_vecinos: Cantidad de bloques adyacentes iguales

        Returns:
            El multiplicador a aplicar al valor del bloque
        """
        pass


class EstrategiaUnVecino(EstrategiaMultiplicacion):
    """Estrategia cuando hay 1 vecino igual: multiplica por 2"""

    def calcular_multiplicador(self, cantidad_vecinos: int) -> int:
        return 2


class EstrategiaDosVecinos(EstrategiaMultiplicacion):
    """Estrategia cuando hay 2 vecinos iguales: multiplica por 4"""

    def calcular_multiplicador(self, cantidad_vecinos: int) -> int:
        return 4


class EstrategiaTresVecinos(EstrategiaMultiplicacion):
    """Estrategia cuando hay 3 vecinos iguales: multiplica por 8"""

    def calcular_multiplicador(self, cantidad_vecinos: int) -> int:
        return 8


class ContextoMultiplicacion:
    """Contexto que usa las estrategias de multiplicación"""

    def __init__(self):
        # Mapeo de cantidad de vecinos a estrategia
        self._estrategias = {
            1: EstrategiaUnVecino(),
            2: EstrategiaDosVecinos(),
            3: EstrategiaTresVecinos()
        }

    def calcular_nuevo_valor(self, valor_actual: int, cantidad_vecinos: int) -> int:
        """
        Calcula el nuevo valor del bloque según la cantidad de vecinos

        Args:
            valor_actual: Valor actual del bloque
            cantidad_vecinos: Cantidad de vecinos iguales adyacentes

        Returns:
            El nuevo valor multiplicado
        """
        if cantidad_vecinos == 0:
            return valor_actual

        estrategia = self._estrategias.get(cantidad_vecinos)
        if estrategia:
            multiplicador = estrategia.calcular_multiplicador(cantidad_vecinos)
            return valor_actual * multiplicador

        return valor_actual
